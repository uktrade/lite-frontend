from http import HTTPStatus
from caseworker.advice.conditionals import form_add_licence_conditions, is_desnz_team
from caseworker.advice.forms.approval import (
    FootnotesApprovalAdviceForm,
    LicenceConditionsForm,
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


# class SelectAdviceView(LoginRequiredMixin, CaseContextMixin, FormView):
#     template_name = "advice/select_advice.html"
#     form_class = SelectAdviceForm

#     def get_success_url(self):
#         recommendation = self.request.POST.get("recommendation")
#         if recommendation == "approve_all":
#             return reverse("cases:approve_all", kwargs=self.kwargs)
#         else:
#             return reverse("cases:refuse_all", kwargs=self.kwargs)

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         return {**context, "security_approvals_classified_display": self.security_approvals_classified_display}


class GiveApprovalAdviceView(LoginRequiredMixin, CaseContextMixin, BaseSessionWizardView):

    form_list = [
        (AdviceSteps.RECOMMEND_APPROVAL, RecommendAnApprovalForm),
        (AdviceSteps.LICENCE_CONDITIONS, LicenceConditionsForm),
        (AdviceSteps.LICENCE_FOOTNOTES, FootnotesApprovalAdviceForm),
    ]

    condition_dict = {
        AdviceSteps.RECOMMEND_APPROVAL: C(is_desnz_team),
        AdviceSteps.LICENCE_CONDITIONS: C(form_add_licence_conditions(AdviceSteps.RECOMMEND_APPROVAL)),
        AdviceSteps.LICENCE_FOOTNOTES: C(form_add_licence_conditions(AdviceSteps.RECOMMEND_APPROVAL)),
    }

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
