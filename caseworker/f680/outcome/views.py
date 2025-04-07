from collections import defaultdict
from http import HTTPStatus

from django.contrib import messages
from django.shortcuts import redirect, reverse
from django.utils.datastructures import OrderedSet
from django.views.generic import View

from core.auth.views import LoginRequiredMixin
from core.decorators import expect_status
from core.wizard.views import BaseSessionWizardView

from caseworker.f680.views import F680CaseworkerMixin
from caseworker.f680.outcome import forms
from caseworker.f680.outcome.constants import OutcomeSteps
from caseworker.f680.outcome.payloads import OutcomePayloadBuilder
from caseworker.f680.outcome.services import (
    post_outcome,
    get_outcomes,
    delete_outcome,
    get_releases_with_no_outcome,
)
from caseworker.f680.recommendation.services import get_case_recommendations


def is_approve_selected(wizard):
    cleaned_data = wizard.get_cleaned_data_for_step(OutcomeSteps.SELECT_OUTCOME) or {}
    return cleaned_data.get("outcome") == "approve"


def is_refuse_selected(wizard):
    cleaned_data = wizard.get_cleaned_data_for_step(OutcomeSteps.SELECT_OUTCOME) or {}
    return cleaned_data.get("outcome") == "refuse"


class DecideOutcome(LoginRequiredMixin, F680CaseworkerMixin, BaseSessionWizardView):
    template_name = "f680/case/outcome/form_wizard.html"
    current_tab = "recommendations"

    form_list = [
        (OutcomeSteps.SELECT_OUTCOME, forms.SelectOutcomeForm),
        (OutcomeSteps.APPROVE, forms.ApproveOutcomeForm),
        (OutcomeSteps.REFUSE, forms.RefuseOutcomeForm),
    ]

    condition_dict = {
        OutcomeSteps.APPROVE: is_approve_selected,
        OutcomeSteps.REFUSE: is_refuse_selected,
    }

    def extra_setup(self, request):
        super().extra_setup(request)
        self.existing_outcomes, self.remaining_requests_without_outcome, self.remaining_request_ids_without_outcome = (
            self.get_remaining_outcomes()
        )
        self.case_recommendations = get_case_recommendations(self.request, self.case)

    def get_remaining_outcomes(self):
        existing_outcomes, _ = self.get_existing_outcomes()
        remaining_requests_without_outcome, remaining_request_ids_without_outcome = get_releases_with_no_outcome(
            self.request, existing_outcomes, self.case
        )
        return existing_outcomes, remaining_requests_without_outcome, remaining_request_ids_without_outcome

    def get_success_url(self):
        return reverse("cases:f680:recommendation", kwargs=self.kwargs)

    def get_form_kwargs(self, step=None):
        if step == OutcomeSteps.SELECT_OUTCOME:
            return {"security_release_requests": self.remaining_requests_without_outcome}
        if step == OutcomeSteps.APPROVE:
            # Restrict approval type choices to those requested in the application
            return {"all_approval_types": self.case["data"]["security_release_requests"][0]["approval_types"]}
        return {}

    def get_form_initial(self, step=None):
        if step == OutcomeSteps.APPROVE:
            all_security_release_requests = self.get_all_security_releases()
            selected_security_release_requests = self.get_selected_security_releases(all_security_release_requests)
            return {"conditions": self.get_aggregated_conditions(selected_security_release_requests)}
        return {}

    def get_selected_security_releases(self, all_security_release_requests):
        select_outcome_data = self.storage.get_step_data(OutcomeSteps.SELECT_OUTCOME)
        if not select_outcome_data:
            return []

        selected_security_release_ids = select_outcome_data.getlist("select_outcome-security_release_requests")
        return [
            security_release_request
            for security_release_request in all_security_release_requests
            if security_release_request["id"] in selected_security_release_ids
        ]

    def get_all_security_releases(self):
        recommendations_by_security_release = defaultdict(list)
        for recommendation in self.case_recommendations:
            # Replace security_release_request dict in recommendation with ID - this is redundant in template
            # context as recommendations are already attached to the security releases
            recommendation = recommendation.copy()
            recommendation["security_release_request_id"] = recommendation["security_release_request"]["id"]
            del recommendation["security_release_request"]
            recommendations_by_security_release[recommendation["security_release_request_id"]].append(recommendation)

        all_security_releases = []
        for security_release_request in self.case["data"]["security_release_requests"]:
            security_release_id = security_release_request["id"]
            if security_release_id not in self.remaining_request_ids_without_outcome:
                continue
            security_release_request["recommendations"] = recommendations_by_security_release[security_release_id]
            all_security_releases.append(security_release_request)
        return all_security_releases

    def get_aggregated_conditions(self, security_release_requests):
        conditions = OrderedSet()
        for release_request in security_release_requests:
            for recommendation in release_request["recommendations"]:
                if not recommendation["conditions"]:
                    continue
                conditions.add(recommendation["conditions"])
        return "\r\n\r\n".join(conditions)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["back_link_url"] = reverse("cases:f680:recommendation", kwargs=self.kwargs)
        all_security_release_requests = self.get_all_security_releases()
        context["all_security_release_requests"] = all_security_release_requests
        context["selected_security_release_requests"] = self.get_selected_security_releases(
            all_security_release_requests
        )
        return context

    @expect_status(
        HTTPStatus.CREATED,
        "Error adding outcome",
        "Unexpected error adding outcome",
    )
    def post_outcome(self, data):
        return post_outcome(self.request, self.case.id, data)

    @expect_status(
        HTTPStatus.OK,
        "Error getting existing outcomes",
        "Unexpected error getting existing outcomes",
    )
    def get_existing_outcomes(self):
        return get_outcomes(self.request, self.case.id)

    def get_payload(self, form_dict):
        return OutcomePayloadBuilder().build(form_dict)

    def done(self, form_list, form_dict, **kwargs):
        data = self.get_payload(form_dict)
        security_request_count = len(data["security_release_requests"])
        self.post_outcome(data)
        success_message = f"Outcomes for {security_request_count} security releases saved successfully"
        if security_request_count == 1:
            success_message = "Outcome saved successfully"
        messages.success(self.request, success_message)
        for request_id in data["security_release_requests"]:
            self.remaining_request_ids_without_outcome.remove(request_id)
        if len(self.remaining_request_ids_without_outcome) == 0:
            return redirect(self.get_success_url())
        return redirect(reverse("cases:f680:outcome:decide_outcome", kwargs=self.kwargs))


class ClearOutcome(LoginRequiredMixin, F680CaseworkerMixin, View):

    @expect_status(
        HTTPStatus.NO_CONTENT,
        "Error clearing outcome",
        "Unexpected error clearing outcome",
    )
    def delete_outcome(self, outcome_id):
        return delete_outcome(self.request, self.case.id, outcome_id)

    def post(self, request, **kwargs):
        self.delete_outcome(self.kwargs["outcome_id"])
        success_message = "Outcome cleared successfully"
        messages.success(self.request, success_message, extra_tags="safe")
        outcome_url = reverse(
            "cases:f680:recommendation", kwargs={"queue_pk": self.kwargs["queue_pk"], "pk": self.kwargs["pk"]}
        )
        return redirect(outcome_url)
