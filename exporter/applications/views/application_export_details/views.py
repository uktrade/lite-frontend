import logging
from http import HTTPStatus

from django.http import Http404
from django.conf import settings
from django.shortcuts import redirect
from django.urls import reverse

from core.auth.views import LoginRequiredMixin

from lite_forms.generators import error_page

from exporter.core.wizard.views import BaseSessionWizardView
from exporter.core.common.decorators import expect_status
from exporter.core.common.exceptions import ServiceError
from exporter.applications.views.goods.common.mixins import ApplicationMixin
from exporter.applications.services import put_application, post_additional_document
from exporter.core.helpers import get_document_data

from .forms import SecurityClassifiedDetailsForm, F680ReferenceNumberForm, SecurityOtherDetailsForm, F1686DetailsForm

from .constants import ExportDetailsSteps
from .conditionals import is_f680_approval, is_f1686_approval, is_other_approval
from .payloads import ExportDetailsStepsPayloadBuilder

logger = logging.getLogger(__name__)


class ExportDetails(
    LoginRequiredMixin,
    ApplicationMixin,
    BaseSessionWizardView,
):
    form_list = [
        (ExportDetailsSteps.SECURITY_CLASSIFIED, SecurityClassifiedDetailsForm),
        (ExportDetailsSteps.F680_REFERENCE_NUMBER, F680ReferenceNumberForm),
        (ExportDetailsSteps.F1686_DETAILS, F1686DetailsForm),
        (ExportDetailsSteps.SECURITY_OTHER_DETAILS, SecurityOtherDetailsForm),
    ]

    condition_dict = {
        ExportDetailsSteps.F680_REFERENCE_NUMBER: is_f680_approval,
        ExportDetailsSteps.F1686_DETAILS: is_f1686_approval,
        ExportDetailsSteps.SECURITY_OTHER_DETAILS: is_other_approval,
    }

    def dispatch(self, request, **kwargs):
        if not settings.FEATURE_FLAG_F680_SECURITY_CLASSIFIED_ENABLED:
            raise Http404
        return super().dispatch(request, **kwargs)

    def get_form_kwargs(self, step=None):
        kwargs = super().get_form_kwargs(step)
        return kwargs

    def get_context_data(self, form, **kwargs):
        ctx = super().get_context_data(form, **kwargs)

        ctx["back_link_url"] = reverse(
            "applications:new_good",
            kwargs={
                "pk": self.kwargs["pk"],
            },
        )
        ctx["title"] = form.Layout.TITLE

        return ctx

    def has_f1686_approval_document(self):
        return self.condition_dict[ExportDetailsSteps.F1686_DETAILS](self)

    def get_f1686_approval_document(self):
        data = self.get_cleaned_data_for_step(ExportDetailsSteps.F1686_DETAILS)
        document = data["f1686_approval_document"]
        payload = {
            **get_document_data(document),
            "description": data["description"],
        }
        return payload

    @expect_status(
        HTTPStatus.CREATED,
        "Error with product document when creating component",
        "Unexpected error adding component",
    )
    def post_f1686_approval_document(self, good):
        document_payload = self.get_f1686_approval_document()
        return post_additional_document(
            request=self.request,
            pk=self.application["id"],
            json=document_payload,
        )

    def get_payload(self, form_dict):
        export_details_payload = ExportDetailsStepsPayloadBuilder().build(form_dict)
        return export_details_payload

    def get_success_url(self):
        return reverse(
            "applications:locations_summary",
            kwargs={"pk": self.application["id"]},
        )

    def handle_service_error(self, service_error):
        logger.error(
            service_error.log_message,
            service_error.status_code,
            service_error.response,
            exc_info=True,
        )
        if settings.DEBUG:
            raise service_error
        return error_page(self.request, service_error.user_message)

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
        try:
            _, _ = self.update_application(form_dict)
            if self.has_f1686_approval_document():
                pass
        except ServiceError as e:
            return self.handle_service_error(e)

        return redirect(self.get_success_url())
