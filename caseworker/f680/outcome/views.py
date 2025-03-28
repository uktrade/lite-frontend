from django.shortcuts import redirect, reverse
from http import HTTPStatus

from core.auth.views import LoginRequiredMixin
from core.decorators import expect_status
from core.wizard.views import BaseSessionWizardView

from caseworker.f680.views import F680CaseworkerMixin
from caseworker.f680.outcome import forms
from caseworker.f680.outcome.constants import OutcomeSteps
from caseworker.f680.outcome.payloads import OutcomePayloadBuilder
from caseworker.f680.outcome.services import post_outcome, get_outcomes


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
        self.existing_outcomes, self.remaining_requests_without_outcome, self.remaining_request_ids_without_outcome = (
            self.get_remaining_outcomes()
        )

    def get_remaining_outcomes(self):
        existing_outcomes, _ = self.get_existing_outcomes()
        release_requests_with_outcome = set()
        for outcome in existing_outcomes:
            release_requests_with_outcome.update(outcome["security_release_requests"])
        remaining_request_ids_without_outcome = set()
        remaining_requests_without_outcome = []
        for release_request in self.case.data["security_release_requests"]:
            if release_request["id"] in release_requests_with_outcome:
                continue
            remaining_requests_without_outcome.append(release_request)
            remaining_request_ids_without_outcome.add(release_request["id"])
        return existing_outcomes, remaining_requests_without_outcome, remaining_request_ids_without_outcome

    def get_success_url(self):
        return reverse("cases:f680:recommendation", kwargs=self.kwargs)

    def get_form_kwargs(self, step):
        if step == OutcomeSteps.SELECT_OUTCOME:
            return {"security_release_requests": self.remaining_requests_without_outcome}
        if step == OutcomeSteps.APPROVE:
            # Restrict approval type choices to those requested in the application
            return {"all_approval_types": self.case["data"]["security_release_requests"][0]["approval_types"]}
        return {}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["back_link_url"] = reverse("cases:f680:recommendation", kwargs=self.kwargs)
        select_outcome_data = self.storage.get_step_data(OutcomeSteps.SELECT_OUTCOME)
        if select_outcome_data:
            selected_security_release_ids = select_outcome_data.getlist("select_outcome-security_release_requests")
            selected_security_releases = []
            for security_release_request in self.case["data"]["security_release_requests"]:
                if security_release_request["id"] in selected_security_release_ids:
                    selected_security_releases.append(security_release_request)
            context["selected_security_release_requests"] = selected_security_releases
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
        self.post_outcome(data)
        for request_id in data["security_release_requests"]:
            self.remaining_request_ids_without_outcome.remove(request_id)
        if len(self.remaining_request_ids_without_outcome) == 0:
            return redirect(self.get_success_url())
        return redirect(reverse("cases:f680:outcome:decide_outcome", kwargs=self.kwargs))
