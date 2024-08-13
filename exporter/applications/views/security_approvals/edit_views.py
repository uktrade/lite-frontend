from datetime import datetime
from http import HTTPStatus

from django.views.generic import FormView
from django.urls import reverse
from django.shortcuts import redirect

from core.auth.views import LoginRequiredMixin
from core.decorators import expect_status

from exporter.applications.views.goods.common.mixins import ApplicationMixin
from exporter.applications.views.goods.common.payloads import get_cleaned_data
from exporter.applications.services import put_application
from core.wizard.views import BaseSessionWizardView

from .forms import (
    F1686DetailsForm,
    F680ReferenceNumberForm,
    SecurityClassifiedDetailsForm,
    SecurityOtherDetailsForm,
    SubjectToITARControlsForm,
)
from .conditionals import (
    is_f680_approval_changed_and_selected,
    is_f1686_approval_changed_and_selected,
    is_other_approval_changed_and_selected,
)
from .payloads import get_f1686_data, SecurityApprovalStepsPayloadBuilder
from .constants import SecurityApprovalSteps
from .initial import (
    get_initial_security_classified_details,
    get_initial_f680_reference_number,
    get_initial_other_security_approval_details,
    get_initial_f1686_details,
    get_initial_subject_to_itar_controls,
)


class BaseApplicationEditView(
    LoginRequiredMixin,
    ApplicationMixin,
    FormView,
):
    template_name = "core/form.html"

    def get_back_link_url(self):
        return self.get_success_url()

    def get_edit_payload(self, form):
        raise NotImplementedError(f"Implement `get_edit_payload` for {self.__class__.__name__}")

    def get_success_url(self):
        return reverse(
            "applications:security_approvals_summary",
            kwargs={"pk": self.application["id"]},
        )

    @expect_status(
        HTTPStatus.OK,
        "Error updating product",
        "Unexpected error updating product",
    )
    def edit_object(self, request, application_id, payload):
        return put_application(request, application_id, payload)

    def form_valid(self, form):
        self.edit_object(self.request, self.application["id"], self.get_edit_payload(form))
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)

        ctx["back_link_url"] = self.get_back_link_url()
        ctx["title"] = self.form_class.Layout.TITLE
        ctx["form_title"] = self.form_class.Layout.TITLE

        return ctx


class BaseApplicationEditWizardView(
    LoginRequiredMixin,
    ApplicationMixin,
    BaseSessionWizardView,
):
    def get_success_url(self):
        return reverse(
            "applications:security_approvals_summary",
            kwargs={"pk": self.application["id"]},
        )

    def get_back_link_url(self):
        return self.get_success_url()

    def get_context_data(self, form, **kwargs):
        ctx = super().get_context_data(form, **kwargs)
        ctx["back_link_url"] = self.get_success_url()
        ctx["title"] = form.Layout.TITLE
        return ctx

    def get_payload(self, form_dict):
        export_details_payload = SecurityApprovalStepsPayloadBuilder().build(form_dict)
        return export_details_payload

    @expect_status(
        HTTPStatus.OK,
        "Error updating product",
        "Unexpected error updating product",
    )
    def edit_object(self, request, application_id, payload):
        return put_application(request, application_id, payload)

    def process_forms(self, form_list, form_dict, **kwargs):
        self.edit_object(self.request, self.application["id"], self.get_payload(form_dict))

    def done(self, form_list, form_dict, **kwargs):
        self.process_forms(form_list, form_dict, **kwargs)

        return redirect(self.get_success_url())


class EditF680ReferenceNumber(BaseApplicationEditView):
    form_class = F680ReferenceNumberForm

    def get_initial(self):
        return {"f680_reference_number": self.application["f680_reference_number"]}

    def get_edit_payload(self, form):
        return get_cleaned_data(form)


class EditSubjectToITARControls(BaseApplicationEditView):
    form_class = SubjectToITARControlsForm

    def get_initial(self):
        return {"subject_to_itar_controls": self.application["subject_to_itar_controls"]}

    def get_edit_payload(self, form):
        return get_cleaned_data(form)


class EditSecurityOtherDetails(BaseApplicationEditView):
    form_class = SecurityOtherDetailsForm

    def get_initial(self):
        return {"other_security_approval_details": self.application["other_security_approval_details"]}

    def get_edit_payload(self, form):
        return get_cleaned_data(form)


class EditF1686Details(BaseApplicationEditView):
    form_class = F1686DetailsForm

    def get_initial(self):
        f1686_approval_date = self.application["f1686_approval_date"]
        if f1686_approval_date:
            f1686_approval_date = datetime.fromisoformat(self.application["f1686_approval_date"]).date()
        return {
            "f1686_contracting_authority": self.application["f1686_contracting_authority"],
            "f1686_reference_number": self.application["f1686_reference_number"],
            "f1686_approval_date": f1686_approval_date,
        }

    def get_edit_payload(self, form):
        return get_f1686_data(form)


class EditSecurityApprovalDetails(
    BaseApplicationEditWizardView,
):
    form_list = [
        (SecurityApprovalSteps.SECURITY_CLASSIFIED, SecurityClassifiedDetailsForm),
        (SecurityApprovalSteps.SUBJECT_TO_ITAR_CONTROLS, SubjectToITARControlsForm),
        (SecurityApprovalSteps.F680_REFERENCE_NUMBER, F680ReferenceNumberForm),
        (SecurityApprovalSteps.F1686_DETAILS, F1686DetailsForm),
        (SecurityApprovalSteps.SECURITY_OTHER_DETAILS, SecurityOtherDetailsForm),
    ]

    condition_dict = {
        SecurityApprovalSteps.SUBJECT_TO_ITAR_CONTROLS: is_f680_approval_changed_and_selected,
        SecurityApprovalSteps.F680_REFERENCE_NUMBER: is_f680_approval_changed_and_selected,
        SecurityApprovalSteps.F1686_DETAILS: is_f1686_approval_changed_and_selected,
        SecurityApprovalSteps.SECURITY_OTHER_DETAILS: is_other_approval_changed_and_selected,
    }

    def get_form_initial(self, step):
        initial = super().get_form_initial(step)
        if step == SecurityApprovalSteps.SECURITY_CLASSIFIED:
            initial.update(get_initial_security_classified_details(self.application))
        if step == SecurityApprovalSteps.SUBJECT_TO_ITAR_CONTROLS:
            initial.update(get_initial_subject_to_itar_controls(self.application))
        if step == SecurityApprovalSteps.F680_REFERENCE_NUMBER:
            initial.update(get_initial_f680_reference_number(self.application))
        if step == SecurityApprovalSteps.F1686_DETAILS:
            initial.update(get_initial_f1686_details(self.application))
        if step == SecurityApprovalSteps.SECURITY_OTHER_DETAILS:
            initial.update(get_initial_other_security_approval_details(self.application))

        return initial

    def get_context_data(self, form, **kwargs):
        ctx = super().get_context_data(form, **kwargs)
        ctx["back_link_url"] = self.get_success_url()
        ctx["title"] = form.Layout.TITLE
        return ctx
