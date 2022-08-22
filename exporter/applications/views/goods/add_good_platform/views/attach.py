import logging

from http import HTTPStatus

from django.conf import settings
from django.shortcuts import redirect
from django.urls import reverse

from lite_forms.generators import error_page

from core.auth.views import LoginRequiredMixin
from exporter.core.wizard.views import BaseSessionWizardView
from exporter.applications.services import post_platform_good_on_application

from exporter.applications.views.goods.common.conditionals import is_onward_exported
from .constants import AddGoodPlatformToApplicationSteps
from exporter.core.common.decorators import expect_status
from exporter.core.common.exceptions import ServiceError
from .mixins import NonFirearmsFlagMixin
from exporter.applications.views.goods.common.mixins import ApplicationMixin, GoodMixin
from .payloads import AddGoodPlatformToApplicationPayloadBuilder

from exporter.goods.forms.firearms import (
    FirearmOnwardExportedForm,
    FirearmOnwardAlteredProcessedForm,
    FirearmOnwardIncorporatedForm,
    FirearmQuantityAndValueForm,
)

logger = logging.getLogger(__name__)


class AttachPlatformToApplication(
    LoginRequiredMixin,
    NonFirearmsFlagMixin,
    ApplicationMixin,
    GoodMixin,
    BaseSessionWizardView,
):
    form_list = [
        (AddGoodPlatformToApplicationSteps.ONWARD_EXPORTED, FirearmOnwardExportedForm),
        (AddGoodPlatformToApplicationSteps.ONWARD_ALTERED_PROCESSED, FirearmOnwardAlteredProcessedForm),
        (AddGoodPlatformToApplicationSteps.ONWARD_INCORPORATED, FirearmOnwardIncorporatedForm),
        (AddGoodPlatformToApplicationSteps.QUANTITY_AND_VALUE, FirearmQuantityAndValueForm),
    ]
    condition_dict = {
        AddGoodPlatformToApplicationSteps.ONWARD_ALTERED_PROCESSED: is_onward_exported,
        AddGoodPlatformToApplicationSteps.ONWARD_INCORPORATED: is_onward_exported,
    }

    def get_form_kwargs(self, step=None):
        kwargs = super().get_form_kwargs(step)
        return kwargs

    def get_success_url(self):
        return reverse(
            "applications:attach_product_on_application_summary",
            kwargs={
                "pk": self.kwargs["pk"],
                "good_on_application_pk": self.good_on_application["id"],
            },
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

    def get_payload(self, form_dict):
        good_payload = AddGoodPlatformToApplicationPayloadBuilder().build(form_dict)
        return good_payload

    @expect_status(
        HTTPStatus.CREATED,
        "Error adding platform to application",
        "Unexpected error adding platform to application",
    )
    def post_platform_to_application(self, form_dict):
        payload = self.get_payload(form_dict)
        return post_platform_good_on_application(
            self.request,
            self.application["id"],
            self.good["id"],
            payload,
        )

    def get_context_data(self, form, **kwargs):
        ctx = super().get_context_data(form, **kwargs)

        ctx["back_link_url"] = reverse(
            "applications:preexisting_good",
            kwargs={
                "pk": self.kwargs["pk"],
            },
        )
        ctx["title"] = form.Layout.TITLE

        return ctx

    def done(self, form_list, form_dict, **kwargs):
        try:
            good_on_application, _ = self.post_platform_to_application(form_dict)
            good_on_application = good_on_application["good"]
        except ServiceError as e:
            return self.handle_service_error(e)
        self.good_on_application = good_on_application

        return redirect(self.get_success_url())
