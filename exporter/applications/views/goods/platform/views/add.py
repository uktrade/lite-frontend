import logging

from http import HTTPStatus

from django.shortcuts import redirect
from django.urls import reverse

from core.auth.views import LoginRequiredMixin
from core.decorators import expect_status

from exporter.applications.views.goods.common.actions import ProductDocumentAction
from core.wizard.views import BaseSessionWizardView
from exporter.goods.forms.common import (
    ProductControlListEntryForm,
    ProductDescriptionForm,
    ProductDocumentAvailabilityForm,
    ProductDocumentSensitivityForm,
    ProductDocumentUploadForm,
    ProductMilitaryUseForm,
    ProductNameForm,
    ProductOnwardAlteredProcessedForm,
    ProductOnwardExportedForm,
    ProductOnwardIncorporatedForm,
    ProductPartNumberForm,
    ProductPVGradingDetailsForm,
    ProductPVGradingForm,
    ProductQuantityAndValueForm,
    ProductUsesInformationSecurityForm,
)

from exporter.goods.services import post_complete_item
from exporter.applications.services import post_complete_item_good_on_application
from exporter.applications.views.goods.common.mixins import (
    ApplicationMixin,
    GoodMixin,
)
from exporter.applications.views.goods.common.conditionals import (
    is_pv_graded,
    is_product_document_available,
    is_document_sensitive,
    is_onward_exported,
)
from core.wizard.conditionals import C

from .constants import (
    AddGoodCompleteItemSteps,
    AddGoodCompleteItemToApplicationSteps,
)
from .payloads import (
    AddGoodCompleteItemPayloadBuilder,
    AddGoodCompleteItemToApplicationPayloadBuilder,
)

logger = logging.getLogger(__name__)


class AddGoodCompleteItem(
    LoginRequiredMixin,
    ApplicationMixin,
    BaseSessionWizardView,
):
    form_list = [
        (AddGoodCompleteItemSteps.NAME, ProductNameForm),
        (AddGoodCompleteItemSteps.PRODUCT_CONTROL_LIST_ENTRY, ProductControlListEntryForm),
        (AddGoodCompleteItemSteps.PART_NUMBER, ProductPartNumberForm),
        (AddGoodCompleteItemSteps.PV_GRADING, ProductPVGradingForm),
        (AddGoodCompleteItemSteps.PV_GRADING_DETAILS, ProductPVGradingDetailsForm),
        (AddGoodCompleteItemSteps.PRODUCT_USES_INFORMATION_SECURITY, ProductUsesInformationSecurityForm),
        (AddGoodCompleteItemSteps.PRODUCT_DOCUMENT_AVAILABILITY, ProductDocumentAvailabilityForm),
        (AddGoodCompleteItemSteps.PRODUCT_DESCRIPTION, ProductDescriptionForm),
        (AddGoodCompleteItemSteps.PRODUCT_DOCUMENT_SENSITIVITY, ProductDocumentSensitivityForm),
        (AddGoodCompleteItemSteps.PRODUCT_DOCUMENT_UPLOAD, ProductDocumentUploadForm),
        (AddGoodCompleteItemSteps.PRODUCT_MILITARY_USE, ProductMilitaryUseForm),
    ]
    condition_dict = {
        AddGoodCompleteItemSteps.PV_GRADING_DETAILS: is_pv_graded,
        AddGoodCompleteItemSteps.PRODUCT_DESCRIPTION: ~C(is_product_document_available),
        AddGoodCompleteItemSteps.PRODUCT_DOCUMENT_SENSITIVITY: is_product_document_available,
        AddGoodCompleteItemSteps.PRODUCT_DOCUMENT_UPLOAD: C(is_product_document_available) & ~C(is_document_sensitive),
    }

    def get_form_kwargs(self, step=None):
        kwargs = super().get_form_kwargs(step)

        if step == AddGoodCompleteItemSteps.PRODUCT_CONTROL_LIST_ENTRY:
            kwargs["request"] = self.request

        if step == AddGoodCompleteItemSteps.PV_GRADING_DETAILS:
            kwargs["request"] = self.request

        return kwargs

    def get_context_data(self, form, **kwargs):
        ctx = super().get_context_data(form, **kwargs)

        ctx["back_link_url"] = reverse(
            "applications:non_firearm_category",
            kwargs={
                "pk": self.kwargs["pk"],
            },
        )
        ctx["title"] = form.Layout.TITLE

        return ctx

    def get_payload(self, form_dict):
        good_payload = AddGoodCompleteItemPayloadBuilder().build(form_dict)
        return good_payload

    def get_success_url(self):
        return reverse(
            "applications:complete_item_product_summary",
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

        ProductDocumentAction(self).run()

        return redirect(self.get_success_url())


class AddGoodCompleteItemToApplication(
    LoginRequiredMixin,
    ApplicationMixin,
    GoodMixin,
    BaseSessionWizardView,
):
    form_list = [
        (AddGoodCompleteItemToApplicationSteps.ONWARD_EXPORTED, ProductOnwardExportedForm),
        (AddGoodCompleteItemToApplicationSteps.ONWARD_ALTERED_PROCESSED, ProductOnwardAlteredProcessedForm),
        (AddGoodCompleteItemToApplicationSteps.ONWARD_INCORPORATED, ProductOnwardIncorporatedForm),
        (AddGoodCompleteItemToApplicationSteps.QUANTITY_AND_VALUE, ProductQuantityAndValueForm),
    ]

    condition_dict = {
        AddGoodCompleteItemToApplicationSteps.ONWARD_ALTERED_PROCESSED: is_onward_exported,
        AddGoodCompleteItemToApplicationSteps.ONWARD_INCORPORATED: is_onward_exported,
    }

    def get_form_kwargs(self, step=None):
        kwargs = super().get_form_kwargs(step)

        if step == AddGoodCompleteItemToApplicationSteps.QUANTITY_AND_VALUE:
            kwargs["request"] = self.request

        return kwargs

    def get_success_url(self):
        return reverse(
            "applications:complete_item_on_application_summary",
            kwargs={
                "pk": self.kwargs["pk"],
                "good_on_application_pk": self.good_on_application["id"],
            },
        )

    def get_payload(self, form_dict):
        good_on_application_payload = AddGoodCompleteItemToApplicationPayloadBuilder().build(form_dict)
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
            "applications:preexisting_good",
            kwargs={
                "pk": self.kwargs["pk"],
            },
        )
        ctx["title"] = form.Layout.TITLE

        return ctx

    def done(self, form_list, form_dict, **kwargs):
        good_on_application, _ = self.post_complete_item_to_application(form_dict)
        good_on_application = good_on_application["good"]
        self.good_on_application = good_on_application

        return redirect(self.get_success_url())
