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
    # TODO: custom template
    template_name = "f680/case/recommendation/form_wizard.html"
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
        self.existing_outcomes, _ = self.get_existing_outcomes()
        release_requests_with_outcome = set()
        for outcome in self.existing_outcomes:
            release_requests_with_outcome.update(outcome["security_release_requests"])
        self.remaining_requests_without_outcome = []
        for release_request in self.case.data["security_release_requests"]:
            if release_request["id"] in release_requests_with_outcome:
                continue
            self.remaining_requests_without_outcome.append(release_request)

    def get_success_url(self):
        return reverse("cases:f680:recommendation", kwargs=self.kwargs)

    def get_form_kwargs(self, step):
        if step != OutcomeSteps.SELECT_OUTCOME:
            return {}
        return {"security_release_requests": self.remaining_requests_without_outcome}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["back_link_url"] = reverse("cases:f680:recommendation", kwargs=self.kwargs)
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
        return redirect(self.get_success_url())
