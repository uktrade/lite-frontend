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
    ProductNameForm,
    ProductOnwardAlteredProcessedForm,
    ProductOnwardExportedForm,
    ProductOnwardIncorporatedForm,
    ProductPartNumberForm,
    ProductPVGradingDetailsForm,
    ProductPVGradingForm,
    ProductUnitQuantityAndValueForm,
    ProductMilitaryUseForm,
)

from exporter.goods.services import post_material
from exporter.applications.services import post_material_good_on_application
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
    AddGoodMaterialSteps,
    AddGoodMaterialToApplicationSteps,
)
from .payloads import (
    AddGoodMaterialPayloadBuilder,
    AddGoodMaterialToApplicationPayloadBuilder,
)

logger = logging.getLogger(__name__)


class AddGoodMaterial(
    LoginRequiredMixin,
    ApplicationMixin,
    BaseSessionWizardView,
):
    form_list = [
        (AddGoodMaterialSteps.NAME, ProductNameForm),
        (AddGoodMaterialSteps.PRODUCT_CONTROL_LIST_ENTRY, ProductControlListEntryForm),
        (AddGoodMaterialSteps.PART_NUMBER, ProductPartNumberForm),
        (AddGoodMaterialSteps.PV_GRADING, ProductPVGradingForm),
        (AddGoodMaterialSteps.PV_GRADING_DETAILS, ProductPVGradingDetailsForm),
        (AddGoodMaterialSteps.PRODUCT_DOCUMENT_AVAILABILITY, ProductDocumentAvailabilityForm),
        (AddGoodMaterialSteps.PRODUCT_DESCRIPTION, ProductDescriptionForm),
        (AddGoodMaterialSteps.PRODUCT_DOCUMENT_SENSITIVITY, ProductDocumentSensitivityForm),
        (AddGoodMaterialSteps.PRODUCT_DOCUMENT_UPLOAD, ProductDocumentUploadForm),
        (AddGoodMaterialSteps.PRODUCT_MILITARY_USE, ProductMilitaryUseForm),
    ]
    condition_dict = {
        AddGoodMaterialSteps.PV_GRADING_DETAILS: is_pv_graded,
        AddGoodMaterialSteps.PRODUCT_DESCRIPTION: ~C(is_product_document_available),
        AddGoodMaterialSteps.PRODUCT_DOCUMENT_SENSITIVITY: is_product_document_available,
        AddGoodMaterialSteps.PRODUCT_DOCUMENT_UPLOAD: C(is_product_document_available) & ~C(is_document_sensitive),
    }

    def get_form_kwargs(self, step=None):
        kwargs = super().get_form_kwargs(step)

        if step == AddGoodMaterialSteps.PRODUCT_CONTROL_LIST_ENTRY:
            kwargs["request"] = self.request

        if step == AddGoodMaterialSteps.PV_GRADING_DETAILS:
            kwargs["request"] = self.request
        return kwargs

    def get_context_data(self, form, **kwargs):
        ctx = super().get_context_data(form, **kwargs)

        ctx["back_link_url"] = reverse(
            "applications:is_material_substance",
            kwargs={
                "pk": self.kwargs["pk"],
            },
        )
        ctx["title"] = form.Layout.TITLE

        return ctx

    def get_payload(self, form_dict):
        good_payload = AddGoodMaterialPayloadBuilder().build(form_dict)
        return good_payload

    def get_success_url(self):
        return reverse(
            "applications:material_product_summary",
            kwargs={"pk": self.application["id"], "good_pk": self.good["id"]},
        )

    @expect_status(
        HTTPStatus.CREATED,
        "Error creating complete product",
        "Unexpected error adding complete product",
    )
    def post_material(self, form_dict):
        payload = self.get_payload(form_dict)

        return post_material(
            self.request,
            payload,
        )

    def done(self, form_list, form_dict, **kwargs):
        good, _ = self.post_material(form_dict)
        self.good = good["good"]

        ProductDocumentAction(self).run()

        return redirect(self.get_success_url())


class AddGoodMaterialToApplication(
    LoginRequiredMixin,
    ApplicationMixin,
    GoodMixin,
    BaseSessionWizardView,
):
    form_list = [
        (AddGoodMaterialToApplicationSteps.ONWARD_EXPORTED, ProductOnwardExportedForm),
        (AddGoodMaterialToApplicationSteps.ONWARD_ALTERED_PROCESSED, ProductOnwardAlteredProcessedForm),
        (AddGoodMaterialToApplicationSteps.ONWARD_INCORPORATED, ProductOnwardIncorporatedForm),
        (AddGoodMaterialToApplicationSteps.UNIT_QUANTITY_AND_VALUE, ProductUnitQuantityAndValueForm),
    ]

    condition_dict = {
        AddGoodMaterialToApplicationSteps.ONWARD_ALTERED_PROCESSED: is_onward_exported,
        AddGoodMaterialToApplicationSteps.ONWARD_INCORPORATED: is_onward_exported,
    }

    def get_form_kwargs(self, step=None):
        kwargs = super().get_form_kwargs(step)
        if step == AddGoodMaterialToApplicationSteps.UNIT_QUANTITY_AND_VALUE:
            kwargs["request"] = self.request

        return kwargs

    def get_success_url(self):
        return reverse(
            "applications:material_on_application_summary",
            kwargs={
                "pk": self.kwargs["pk"],
                "good_on_application_pk": self.good_on_application["id"],
            },
        )

    def get_payload(self, form_dict):
        good_on_application_payload = AddGoodMaterialToApplicationPayloadBuilder().build(form_dict)
        return good_on_application_payload

    @expect_status(
        HTTPStatus.CREATED,
        "Error adding material to application",
        "Unexpected error adding material to application",
    )
    def post_material_to_application(self, form_dict):
        payload = self.get_payload(form_dict)
        return post_material_good_on_application(
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
        good_on_application, _ = self.post_material_to_application(form_dict)
        good_on_application = good_on_application["good"]
        self.good_on_application = good_on_application

        return redirect(self.get_success_url())
