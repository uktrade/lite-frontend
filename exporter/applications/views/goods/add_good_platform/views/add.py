import logging

from http import HTTPStatus

from django.conf import settings
from django.shortcuts import redirect
from django.urls import reverse

from core.auth.views import LoginRequiredMixin

from lite_forms.generators import error_page

from exporter.core.wizard.views import BaseSessionWizardView
from exporter.core.common.decorators import expect_status
from exporter.core.common.exceptions import ServiceError

from exporter.goods.forms.firearms import (
    FirearmNameForm,
    FirearmPvGradingForm,
    FirearmPvGradingDetailsForm,
)
from exporter.goods.services import post_good_platform

from exporter.applications.views.goods.add_good_firearm.views.mixins import ApplicationMixin
from exporter.applications.views.goods.add_good_firearm.views.conditionals import is_pv_graded

from exporter.applications.views.goods.add_good_platform.views.constants import AddGoodPlatformSteps
from exporter.applications.views.goods.add_good_platform.views.payloads import AddGoodPlatformPayloadBuilder
from exporter.applications.views.goods.add_good_platform.views.mixins import NonFirearmsFlagMixin

logger = logging.getLogger(__name__)


class AddGoodPlatform(
    LoginRequiredMixin,
    NonFirearmsFlagMixin,
    ApplicationMixin,
    BaseSessionWizardView,
):
    form_list = [
        (AddGoodPlatformSteps.NAME, FirearmNameForm),
        (AddGoodPlatformSteps.PV_GRADING, FirearmPvGradingForm),
        (AddGoodPlatformSteps.PV_GRADING_DETAILS, FirearmPvGradingDetailsForm),
    ]
    condition_dict = {
        AddGoodPlatformSteps.PV_GRADING_DETAILS: is_pv_graded,
    }

    def get_form_kwargs(self, step=None):
        kwargs = super().get_form_kwargs(step)
        if step == AddGoodPlatformSteps.PV_GRADING_DETAILS:
            kwargs["request"] = self.request
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
        good_payload = AddGoodPlatformPayloadBuilder().build(form_dict)
        return good_payload

    def get_success_url(self):
        return reverse(
            "applications:platform_summary",
            kwargs={"pk": self.application["id"], "good_pk": self.good["id"]},
        )

    @expect_status(
        HTTPStatus.CREATED,
        "Error creating complete product",
        "Unexpected error adding complete product",
    )
    def post_good_platform(self, form_dict):
        payload = self.get_payload(form_dict)

        return post_good_platform(
            self.request,
            payload,
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
            good, _ = self.post_good_platform(form_dict)
            self.good = good["good"]
        except ServiceError as e:
            return self.handle_service_error(e)

        return redirect(self.get_success_url())
