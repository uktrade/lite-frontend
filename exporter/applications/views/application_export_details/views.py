import logging

from django.http import Http404
from django.conf import settings
from django.shortcuts import redirect
from django.urls import reverse

from core.auth.views import LoginRequiredMixin

from lite_forms.generators import error_page

from exporter.core.wizard.views import BaseSessionWizardView
from exporter.applications.views.goods.common.mixins import ApplicationMixin
from exporter.core.common.exceptions import ServiceError

from .forms import SecurityClassifiedDetailsForm, F680ReferenceNumberForm, SecurityOtherDetailsForm, F1686DetailsForm

from .constants import ExportDetailsSteps
from .conditionals import is_f680_approval, is_f1686_approval, is_other_approval


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

    def get_payload(self, form_dict):
        good_payload = {}
        return good_payload

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

    def done(self, form_list, form_dict, **kwargs):
        try:
            pass
        except ServiceError as e:
            return self.handle_service_error(e)

        return redirect(self.get_success_url())
