from http import HTTPStatus
from caseworker.advice.conditionals import form_add_licence_conditions, is_desnz_team
from caseworker.advice.forms.approval import (
    FootnotesApprovalAdviceForm,
    PicklistLicenceConditionsForm,
    SimpleLicenceConditionsForm,
    RecommendAnApprovalForm,
)
from caseworker.advice.payloads import GiveApprovalAdvicePayloadBuilder
from caseworker.advice.picklist_helpers import approval_picklist, footnote_picklist, proviso_picklist
from core.wizard.views import BaseSessionWizardView
from core.wizard.conditionals import C
from django.shortcuts import redirect
from django.urls import reverse
from caseworker.advice.views.mixins import CaseContextMixin
from caseworker.advice import services

from caseworker.advice.constants import AdviceSteps
from core.auth.views import LoginRequiredMixin
from core.decorators import expect_status


class BaseApprovalAdviceView(LoginRequiredMixin, CaseContextMixin, BaseSessionWizardView):

    condition_dict = {
        AdviceSteps.RECOMMEND_APPROVAL: C(is_desnz_team),
        AdviceSteps.LICENCE_CONDITIONS: C(form_add_licence_conditions(AdviceSteps.RECOMMEND_APPROVAL)),
        AdviceSteps.LICENCE_FOOTNOTES: C(form_add_licence_conditions(AdviceSteps.RECOMMEND_APPROVAL)),
    }

    form_list = [
        (AdviceSteps.RECOMMEND_APPROVAL, RecommendAnApprovalForm),
        (AdviceSteps.LICENCE_CONDITIONS, PicklistLicenceConditionsForm),
        (AdviceSteps.LICENCE_FOOTNOTES, FootnotesApprovalAdviceForm),
    ]

    step_kwargs = {
        AdviceSteps.RECOMMEND_APPROVAL: approval_picklist,
        AdviceSteps.LICENCE_CONDITIONS: proviso_picklist,
        AdviceSteps.LICENCE_FOOTNOTES: footnote_picklist,
    }

    def get_success_url(self):
        return reverse("cases:view_my_advice", kwargs=self.kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["back_link_url"] = reverse("cases:advice_view", kwargs=self.kwargs)
        return context

    @expect_status(
        HTTPStatus.CREATED,
        "Error adding approval advice",
        "Unexpected error adding approval advice",
    )
    def post_approval_advice(self, data):
        return services.post_approval_advice(self.request, self.case, data)

    def get_payload(self, form_dict):
        return GiveApprovalAdvicePayloadBuilder().build(form_dict)

    def done(self, form_list, form_dict, **kwargs):
        data = self.get_payload(form_dict)
        self.post_approval_advice(data)
        return redirect(self.get_success_url())


class GiveApprovalAdviceView(BaseApprovalAdviceView):

    def get_form(self, step=None, data=None, files=None):

        if step == AdviceSteps.LICENCE_CONDITIONS:
            picklist_form_kwargs = self.step_kwargs[AdviceSteps.LICENCE_CONDITIONS](self)
            picklist_options_exist = len(picklist_form_kwargs["proviso"]["results"]) > 0
            if picklist_options_exist:
                return PicklistLicenceConditionsForm(data=data, prefix=step, **picklist_form_kwargs)
            else:
                return SimpleLicenceConditionsForm(data=data, prefix=step)

        return super().get_form(step, data, files)
