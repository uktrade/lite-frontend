import logging
from http import HTTPStatus

from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import TemplateView

from core.auth.views import LoginRequiredMixin
from core.decorators import expect_status
from core.constants import SecurityClassifiedApprovalsType

from core.wizard.views import BaseSessionWizardView
from exporter.applications.services import put_application
from exporter.applications.views.goods.common.mixins import ApplicationMixin

from .forms import (
    F1686DetailsForm,
    F680ReferenceNumberForm,
    SecurityClassifiedDetailsForm,
    SecurityOtherDetailsForm,
    SubjectToITARControlsForm,
)

from .constants import SecurityApprovalSteps
from .conditionals import is_f680_approval, is_f1686_approval, is_other_approval
from .payloads import SecurityApprovalStepsPayloadBuilder

logger = logging.getLogger(__name__)


class SecurityApprovals(
    LoginRequiredMixin,
    ApplicationMixin,
    BaseSessionWizardView,
):
    form_list = [
        (SecurityApprovalSteps.SECURITY_CLASSIFIED, SecurityClassifiedDetailsForm),
        (SecurityApprovalSteps.SUBJECT_TO_ITAR_CONTROLS, SubjectToITARControlsForm),
        (SecurityApprovalSteps.F680_REFERENCE_NUMBER, F680ReferenceNumberForm),
        (SecurityApprovalSteps.F1686_DETAILS, F1686DetailsForm),
        (SecurityApprovalSteps.SECURITY_OTHER_DETAILS, SecurityOtherDetailsForm),
    ]

    condition_dict = {
        SecurityApprovalSteps.SUBJECT_TO_ITAR_CONTROLS: is_f680_approval,
        SecurityApprovalSteps.F680_REFERENCE_NUMBER: is_f680_approval,
        SecurityApprovalSteps.F1686_DETAILS: is_f1686_approval,
        SecurityApprovalSteps.SECURITY_OTHER_DETAILS: is_other_approval,
    }

    def get_form_kwargs(self, step=None):
        kwargs = super().get_form_kwargs(step)
        return kwargs

    def get_context_data(self, form, **kwargs):
        ctx = super().get_context_data(form, **kwargs)

        ctx["back_link_url"] = reverse(
            "applications:task_list",
            kwargs={
                "pk": self.kwargs["pk"],
            },
        )
        ctx["title"] = form.Layout.TITLE

        return ctx

    def get_payload(self, form_dict):
        export_details_payload = SecurityApprovalStepsPayloadBuilder().build(form_dict)
        return export_details_payload

    def get_success_url(self):
        return reverse(
            "applications:security_approvals_summary",
            kwargs={"pk": self.application["id"]},
        )

    @expect_status(
        HTTPStatus.OK,
        "Error updating export details",
        "Unexpected error updating export details",
    )
    def update_application(self, form_dict):
        payload = self.get_payload(form_dict)
        return put_application(
            self.request,
            self.application["id"],
            payload,
        )

    def done(self, form_list, form_dict, **kwargs):
        self.update_application(form_dict)
        return redirect(self.get_success_url())


class SecurityApprovalsSummaryView(LoginRequiredMixin, ApplicationMixin, TemplateView):
    template_name = "applications/security-approvals/security-approvals-summary.html"

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["application"] = self.application
        context["back_link_url"] = reverse("applications:task_list", kwargs={"pk": self.kwargs["pk"]})
        context["security_classified_approvals_types"] = SecurityClassifiedApprovalsType
        return context
