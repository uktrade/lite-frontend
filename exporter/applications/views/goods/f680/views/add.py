import logging

from http import HTTPStatus

from django.shortcuts import redirect
from django.urls import reverse

from core.auth.views import LoginRequiredMixin
from core.decorators import expect_status

from core.wizard.views import BaseSessionWizardView
from exporter.goods.forms.common import (
    ProductControlListEntryForm,
    ProductDescriptionForm,
    ProductNameForm,
    ProductProspectValueForm,
)

from exporter.goods.services import post_complete_item
from exporter.applications.services import post_complete_item_good_on_application
from exporter.applications.views.goods.common.mixins import (
    ApplicationMixin,
    GoodMixin,
)

from .constants import (
    AddF680GoodDetailsSteps,
    AddF680GoodDetailsToApplicationSteps,
)
from .payloads import (
    AddF680GoodDetailsPayloadBuilder,
    AddF680GoodDetailsToApplicationPayloadBuilder,
)

logger = logging.getLogger(__name__)


class AddF680GoodDetails(
    LoginRequiredMixin,
    ApplicationMixin,
    BaseSessionWizardView,
):
    form_list = [
        (AddF680GoodDetailsSteps.NAME, ProductNameForm),
        (AddF680GoodDetailsSteps.PRODUCT_CONTROL_LIST_ENTRY, ProductControlListEntryForm),
        (AddF680GoodDetailsSteps.PRODUCT_DESCRIPTION, ProductDescriptionForm),
    ]

    def get_form_kwargs(self, step=None):
        kwargs = super().get_form_kwargs(step)

        if step == AddF680GoodDetailsSteps.PRODUCT_CONTROL_LIST_ENTRY:
            kwargs["request"] = self.request

        return kwargs

    def get_context_data(self, form, **kwargs):
        ctx = super().get_context_data(form, **kwargs)

        ctx["title"] = form.Layout.TITLE

        return ctx

    def get_payload(self, form_dict):
        good_payload = AddF680GoodDetailsPayloadBuilder().build(form_dict)
        good_payload["is_pv_graded"] = "no"
        return good_payload

    def get_success_url(self):
        return reverse(
            "applications:f680_good_details_summary",
            kwargs={"pk": self.application["id"], "good_pk": self.good["id"]},
        )

    @expect_status(
        HTTPStatus.CREATED,
        "Error creating complete product",
        "Unexpected error adding complete product",
    )
    def post_complete_item(self, form_dict):
        payload = self.get_payload(form_dict)

        return post_complete_item(
            self.request,
            payload,
        )

    def done(self, form_list, form_dict, **kwargs):
        good, _ = self.post_complete_item(form_dict)
        self.good = good["good"]

        return redirect(self.get_success_url())


class AddF680GoodDetailsToApplication(
    LoginRequiredMixin,
    ApplicationMixin,
    GoodMixin,
    BaseSessionWizardView,
):
    form_list = [
        (AddF680GoodDetailsToApplicationSteps.PROSPECT_VALUE, ProductProspectValueForm),
    ]

    def get_form_kwargs(self, step=None):
        kwargs = super().get_form_kwargs(step)
        return kwargs

    def get_success_url(self):
        return reverse(
            "applications:f680_good_details_on_application_summary",
            kwargs={
                "pk": self.kwargs["pk"],
                "good_on_application_pk": self.good_on_application["id"],
            },
        )

    def get_payload(self, form_dict):
        good_on_application_payload = AddF680GoodDetailsToApplicationPayloadBuilder().build(form_dict)
        return good_on_application_payload

    @expect_status(
        HTTPStatus.CREATED,
        "Error adding complete item to application",
        "Unexpected error adding complete item to application",
    )
    def post_complete_item_to_application(self, form_dict):
        payload = self.get_payload(form_dict)
        return post_complete_item_good_on_application(
            self.request,
            self.application["id"],
            self.good["id"],
            payload,
        )

    def get_context_data(self, form, **kwargs):
        ctx = super().get_context_data(form, **kwargs)

        ctx["back_link_url"] = reverse(
            "applications:f680_good_details_summary",
            kwargs={
                "pk": self.kwargs["pk"],
                "good_pk": self.good["id"],
            },
        )
        ctx["title"] = form.Layout.TITLE

        return ctx

    def done(self, form_list, form_dict, **kwargs):
        good_on_application, _ = self.post_complete_item_to_application(form_dict)
        good_on_application = good_on_application["good"]
        self.good_on_application = good_on_application

        return redirect(self.get_success_url())
