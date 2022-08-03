import logging

from http import HTTPStatus

from django.conf import settings
from django.shortcuts import redirect
from django.urls import reverse

from lite_forms.generators import error_page

from core.auth.views import LoginRequiredMixin

from exporter.core.wizard.views import BaseSessionWizardView
from exporter.goods.forms.firearms import (
    FirearmNameForm,
    FirearmPvGradingForm,
    FirearmPvGradingDetailsForm,
)
from exporter.goods.services import (
    post_complete_product,
)

from .constants import CompleteProductSteps
from .payloads import AddGoodCompleteProductPayloadBuilder
from .mixins import NonFirearmsFlagMixin
from exporter.applications.views.goods.add_good_firearm.views.mixins import ApplicationMixin
from exporter.applications.views.goods.add_good_firearm.views.conditionals import is_pv_graded

from exporter.core.common.decorators import expect_status
from exporter.core.common.exceptions import ServiceError

logger = logging.getLogger(__name__)


class AddGoodCompleteProduct(
    LoginRequiredMixin,
    NonFirearmsFlagMixin,
    ApplicationMixin,
    BaseSessionWizardView,
):
    form_list = [
        (CompleteProductSteps.NAME, FirearmNameForm),
        (CompleteProductSteps.PV_GRADING, FirearmPvGradingForm),
        (CompleteProductSteps.PV_GRADING_DETAILS, FirearmPvGradingDetailsForm),
    ]
    condition_dict = {
        CompleteProductSteps.PV_GRADING_DETAILS: is_pv_graded,
    }

    def get_form_kwargs(self, step=None):
        kwargs = super().get_form_kwargs(step)
        if step == CompleteProductSteps.PV_GRADING_DETAILS:
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
        good_payload = AddGoodCompleteProductPayloadBuilder().build(form_dict)
        payload = good_payload
        return payload

    def get_success_url(self):
        return reverse(
            "applications:compete_product_summary",
            kwargs={"pk": self.application["id"], "good_pk": self.good["id"]},
        )

    @expect_status(
        HTTPStatus.CREATED,
        "Error creating complete product",
        "Unexpected error adding complete product",
    )
    def post_complete_product(self, form_dict):
        payload = self.get_payload(form_dict)

        return post_complete_product(
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
            good, _ = self.post_complete_product(form_dict)
            self.good = good["good"]
        except ServiceError as e:
            return self.handle_service_error(e)

        return redirect(self.get_success_url())
