from django.shortcuts import redirect, reverse
from http import HTTPStatus

from core.auth.views import LoginRequiredMixin
from core.decorators import expect_status
from core.wizard.views import BaseSessionWizardView

from caseworker.f680.views import F680CaseworkerMixin
from caseworker.f680.outcome import forms
from caseworker.f680.outcome.constants import OutcomeSteps


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

    def get_success_url(self):
        return reverse("cases:f680:recommendation", kwargs=self.kwargs)

    def get_form_kwargs(self, step):
        if step != OutcomeSteps.SELECT_OUTCOME:
            return {}
        # TODO: Restrict this to only security releases where no outcome has been given
        return {"security_release_requests": self.case.data["security_release_requests"]}

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
        # TODO
        pass

    def get_payload(self, form_dict):
        # TODO
        pass

    def done(self, form_list, form_dict, **kwargs):
        data = self.get_payload(form_dict)
        self.post_outcome(data)
        return redirect(self.get_success_url())
