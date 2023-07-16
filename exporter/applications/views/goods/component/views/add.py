import logging

from http import HTTPStatus

from django.shortcuts import redirect
from django.urls import reverse

from core.auth.views import LoginRequiredMixin
from core.decorators import expect_status
from core.helpers import get_document_data

from exporter.applications.views.goods.common.actions import ProductDocumentAction
from core.wizard.views import BaseSessionWizardView
from exporter.goods.forms.common import (
    ProductControlListEntryForm,
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
    ProductDescriptionForm,
)
from exporter.goods.forms.goods import ProductIsComponentForm, ProductComponentDetailsForm
from exporter.goods.services import post_component_accessory, post_good_documents
from exporter.applications.services import post_component_accessory_good_on_application
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
from .conditionals import is_component
from core.wizard.conditionals import C

from .constants import (
    AddGoodComponentSteps,
    AddGoodComponentToApplicationSteps,
)
from .payloads import (
    AddGoodComponentPayloadBuilder,
    AddGoodComponentToApplicationPayloadBuilder,
)

logger = logging.getLogger(__name__)


class AddGoodComponentAccessory(
    LoginRequiredMixin,
    ApplicationMixin,
    BaseSessionWizardView,
):
    form_list = [
        (AddGoodComponentSteps.NAME, ProductNameForm),
        (AddGoodComponentSteps.IS_COMPONENT, ProductIsComponentForm),
        (AddGoodComponentSteps.COMPONENT_DETAILS, ProductComponentDetailsForm),
        (AddGoodComponentSteps.PRODUCT_CONTROL_LIST_ENTRY, ProductControlListEntryForm),
        (AddGoodComponentSteps.PART_NUMBER, ProductPartNumberForm),
        (AddGoodComponentSteps.PV_GRADING, ProductPVGradingForm),
        (AddGoodComponentSteps.PV_GRADING_DETAILS, ProductPVGradingDetailsForm),
        (AddGoodComponentSteps.PRODUCT_USES_INFORMATION_SECURITY, ProductUsesInformationSecurityForm),
        (AddGoodComponentSteps.PRODUCT_DOCUMENT_AVAILABILITY, ProductDocumentAvailabilityForm),
        (AddGoodComponentSteps.PRODUCT_DOCUMENT_SENSITIVITY, ProductDocumentSensitivityForm),
        (AddGoodComponentSteps.PRODUCT_DOCUMENT_UPLOAD, ProductDocumentUploadForm),
        (AddGoodComponentSteps.PRODUCT_DESCRIPTION, ProductDescriptionForm),
        (AddGoodComponentSteps.PRODUCT_MILITARY_USE, ProductMilitaryUseForm),
    ]
    condition_dict = {
        AddGoodComponentSteps.PV_GRADING_DETAILS: is_pv_graded,
        AddGoodComponentSteps.COMPONENT_DETAILS: is_component,
        AddGoodComponentSteps.PRODUCT_DOCUMENT_SENSITIVITY: is_product_document_available,
        AddGoodComponentSteps.PRODUCT_DOCUMENT_UPLOAD: C(is_product_document_available) & ~C(is_document_sensitive),
        AddGoodComponentSteps.PRODUCT_DESCRIPTION: ~C(is_product_document_available),
    }

    def get_form_kwargs(self, step=None):
        kwargs = super().get_form_kwargs(step)

        if step == AddGoodComponentSteps.PRODUCT_CONTROL_LIST_ENTRY:
            kwargs["request"] = self.request

        if step == AddGoodComponentSteps.PV_GRADING_DETAILS:
            kwargs["request"] = self.request

        return kwargs

    def get_product_document_payload(self):
        data = self.get_cleaned_data_for_step(AddGoodComponentSteps.PRODUCT_DOCUMENT_UPLOAD)
        document = data["product_document"]
        payload = {
            **get_document_data(document),
            "description": data["description"],
        }
        return payload

    @expect_status(
        HTTPStatus.CREATED,
        "Error with product document when creating component accessory",
        "Unexpected error adding component accessory",
    )
    def post_product_documentation(self, good):
        document_payload = self.get_product_document_payload()
        return post_good_documents(
            request=self.request,
            pk=good["id"],
            json=document_payload,
        )

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
        good_payload = AddGoodComponentPayloadBuilder().build(form_dict)
        return good_payload

    def get_success_url(self):
        return reverse(
            "applications:component_accessory_product_summary",
            kwargs={"pk": self.application["id"], "good_pk": self.good["id"]},
        )

    @expect_status(
        HTTPStatus.CREATED,
        "Error creating complete component accessory",
        "Unexpected error adding complete product",
    )
    def post_component_accessory(self, form_dict):
        payload = self.get_payload(form_dict)

        return post_component_accessory(
            self.request,
            payload,
        )

    def done(self, form_list, form_dict, **kwargs):
        good, _ = self.post_component_accessory(form_dict)
        self.good = good["good"]

        ProductDocumentAction(self).run()

        return redirect(self.get_success_url())


class AddGoodComponentAccessoryToApplication(
    LoginRequiredMixin,
    ApplicationMixin,
    GoodMixin,
    BaseSessionWizardView,
):
    form_list = [
        (AddGoodComponentToApplicationSteps.ONWARD_EXPORTED, ProductOnwardExportedForm),
        (AddGoodComponentToApplicationSteps.ONWARD_ALTERED_PROCESSED, ProductOnwardAlteredProcessedForm),
        (AddGoodComponentToApplicationSteps.ONWARD_INCORPORATED, ProductOnwardIncorporatedForm),
        (AddGoodComponentToApplicationSteps.QUANTITY_AND_VALUE, ProductQuantityAndValueForm),
    ]

    condition_dict = {
        AddGoodComponentToApplicationSteps.ONWARD_ALTERED_PROCESSED: is_onward_exported,
        AddGoodComponentToApplicationSteps.ONWARD_INCORPORATED: is_onward_exported,
    }

    def get_form_kwargs(self, step=None):
        kwargs = super().get_form_kwargs(step)
        return kwargs

    def get_success_url(self):
        return reverse(
            "applications:component_accessory_on_application_summary",
            kwargs={
                "pk": self.kwargs["pk"],
                "good_on_application_pk": self.good_on_application["id"],
            },
        )

    def get_payload(self, form_dict):
        good_on_application_payload = AddGoodComponentToApplicationPayloadBuilder().build(form_dict)
        return good_on_application_payload

    @expect_status(
        HTTPStatus.CREATED,
        "Error adding component accessory to application",
        "Unexpected error adding component accessory to application",
    )
    def post_component_accessory_to_application(self, form_dict):
        payload = self.get_payload(form_dict)
        return post_component_accessory_good_on_application(
            self.request,
            self.application["id"],
            self.good["id"],
            payload,
        )

    def get_context_data(self, form, **kwargs):
        ctx = super().get_context_data(form, **kwargs)

        ctx["back_link_url"] = reverse(
            "applications:component_accessory_product_summary",
            kwargs={
                "pk": self.kwargs["pk"],
                "good_pk": self.good["id"],
            },
        )
        ctx["title"] = form.Layout.TITLE

        return ctx

    def done(self, form_list, form_dict, **kwargs):
        good_on_application, _ = self.post_component_accessory_to_application(form_dict)
        good_on_application = good_on_application["good"]
        self.good_on_application = good_on_application

        return redirect(self.get_success_url())
