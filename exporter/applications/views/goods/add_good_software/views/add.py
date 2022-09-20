import logging

from http import HTTPStatus

from django.shortcuts import redirect
from django.urls import reverse

from core.auth.views import LoginRequiredMixin
from core.decorators import expect_status

from exporter.core.wizard.views import BaseSessionWizardView
from exporter.core.helpers import get_document_data
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
)
from exporter.goods.forms.goods import (
    ProductDeclaredAtCustomsForm,
    ProductSecurityFeaturesForm,
)
from exporter.goods.services import post_software, post_good_documents
from exporter.applications.services import post_software_good_on_application
from exporter.applications.views.goods.common.mixins import ApplicationMixin, GoodMixin
from exporter.applications.views.goods.common.conditionals import (
    is_pv_graded,
    is_product_document_available,
    is_document_sensitive,
    is_onward_exported,
)
from exporter.core.wizard.conditionals import C

from .constants import (
    AddGoodSoftwareSteps,
    AddGoodSoftwareToApplicationSteps,
)
from .payloads import (
    AddGoodSoftwarePayloadBuilder,
    AddGoodSoftwareToApplicationPayloadBuilder,
)
from .mixins import NonFirearmsSoftwareFlagMixin

logger = logging.getLogger(__name__)


class AddGoodSoftware(
    LoginRequiredMixin,
    NonFirearmsSoftwareFlagMixin,
    ApplicationMixin,
    BaseSessionWizardView,
    ProductSecurityFeaturesForm,
):
    form_list = [
        (AddGoodSoftwareSteps.NAME, ProductNameForm),
        (AddGoodSoftwareSteps.PRODUCT_CONTROL_LIST_ENTRY, ProductControlListEntryForm),
        (AddGoodSoftwareSteps.PART_NUMBER, ProductPartNumberForm),
        (AddGoodSoftwareSteps.PV_GRADING, ProductPVGradingForm),
        (AddGoodSoftwareSteps.PV_GRADING_DETAILS, ProductPVGradingDetailsForm),
        (AddGoodSoftwareSteps.SECURITY_FEATURES, ProductSecurityFeaturesForm),
        (AddGoodSoftwareSteps.PRODUCT_DECLARED_AT_CUSTOMS, ProductDeclaredAtCustomsForm),
        (AddGoodSoftwareSteps.PRODUCT_DOCUMENT_AVAILABILITY, ProductDocumentAvailabilityForm),
        (AddGoodSoftwareSteps.PRODUCT_DOCUMENT_SENSITIVITY, ProductDocumentSensitivityForm),
        (AddGoodSoftwareSteps.PRODUCT_DOCUMENT_UPLOAD, ProductDocumentUploadForm),
        (AddGoodSoftwareSteps.PRODUCT_DESCRIPTION, ProductDescriptionForm),
        (AddGoodSoftwareSteps.PRODUCT_MILITARY_USE, ProductMilitaryUseForm),
    ]
    condition_dict = {
        AddGoodSoftwareSteps.PV_GRADING_DETAILS: is_pv_graded,
        AddGoodSoftwareSteps.PRODUCT_DOCUMENT_SENSITIVITY: is_product_document_available,
        AddGoodSoftwareSteps.PRODUCT_DOCUMENT_UPLOAD: C(is_product_document_available) & ~C(is_document_sensitive),
        AddGoodSoftwareSteps.PRODUCT_DESCRIPTION: ~C(is_product_document_available),
    }

    def get_form_kwargs(self, step=None):
        kwargs = super().get_form_kwargs(step)

        if step == AddGoodSoftwareSteps.PRODUCT_CONTROL_LIST_ENTRY:
            kwargs["request"] = self.request

        if step == AddGoodSoftwareSteps.PV_GRADING_DETAILS:
            kwargs["request"] = self.request
        return kwargs

    def has_product_documentation(self):
        data = self.get_cleaned_data_for_step(AddGoodSoftwareSteps.PRODUCT_DOCUMENT_UPLOAD)
        return data.get("product_document", None)

    def get_product_document_payload(self):
        data = self.get_cleaned_data_for_step(AddGoodSoftwareSteps.PRODUCT_DOCUMENT_UPLOAD)
        document = data.get("product_document", None)
        payload = {
            **get_document_data(document),
            "description": data["description"],
        }
        return payload

    @expect_status(
        HTTPStatus.CREATED,
        "Error with product document when creating software",
        "Unexpected error adding software",
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
            "applications:non_firearm_category",
            kwargs={
                "pk": self.kwargs["pk"],
            },
        )
        ctx["title"] = form.Layout.TITLE

        return ctx

    def get_payload(self, form_dict):
        good_payload = AddGoodSoftwarePayloadBuilder().build(form_dict)
        return good_payload

    def get_success_url(self):
        return reverse(
            "applications:software_product_summary",
            kwargs={"pk": self.application["id"], "good_pk": self.good["id"]},
        )

    @expect_status(
        HTTPStatus.CREATED,
        "Error creating complete product",
        "Unexpected error adding complete product",
    )
    def post_software(self, form_dict):
        payload = self.get_payload(form_dict)

        return post_software(
            self.request,
            payload,
        )

    def done(self, form_list, form_dict, **kwargs):
        good, _ = self.post_software(form_dict)
        self.good = good["good"]
        if self.has_product_documentation():
            self.post_product_documentation(self.good)

        return redirect(self.get_success_url())


class AddGoodSoftwareToApplication(
    LoginRequiredMixin,
    NonFirearmsSoftwareFlagMixin,
    ApplicationMixin,
    GoodMixin,
    BaseSessionWizardView,
):
    form_list = [
        (AddGoodSoftwareToApplicationSteps.ONWARD_EXPORTED, ProductOnwardExportedForm),
        (AddGoodSoftwareToApplicationSteps.ONWARD_ALTERED_PROCESSED, ProductOnwardAlteredProcessedForm),
        (AddGoodSoftwareToApplicationSteps.ONWARD_INCORPORATED, ProductOnwardIncorporatedForm),
        (AddGoodSoftwareToApplicationSteps.QUANTITY_AND_VALUE, ProductQuantityAndValueForm),
    ]

    condition_dict = {
        AddGoodSoftwareToApplicationSteps.ONWARD_ALTERED_PROCESSED: is_onward_exported,
        AddGoodSoftwareToApplicationSteps.ONWARD_INCORPORATED: is_onward_exported,
    }

    def get_form_kwargs(self, step=None):
        kwargs = super().get_form_kwargs(step)
        return kwargs

    def get_success_url(self):
        return reverse(
            "applications:software_on_application_summary",
            kwargs={
                "pk": self.kwargs["pk"],
                "good_on_application_pk": self.good_on_application["id"],
            },
        )

    def get_payload(self, form_dict):
        good_on_application_payload = AddGoodSoftwareToApplicationPayloadBuilder().build(form_dict)
        return good_on_application_payload

    @expect_status(
        HTTPStatus.CREATED,
        "Error adding software to application",
        "Unexpected error adding software to application",
    )
    def post_software_to_application(self, form_dict):
        payload = self.get_payload(form_dict)
        return post_software_good_on_application(
            self.request,
            self.application["id"],
            self.good["id"],
            payload,
        )

    def get_context_data(self, form, **kwargs):
        ctx = super().get_context_data(form, **kwargs)

        ctx["back_link_url"] = reverse(
            "applications:software_product_summary",
            kwargs={
                "pk": self.kwargs["pk"],
                "good_pk": self.good["id"],
            },
        )
        ctx["title"] = form.Layout.TITLE

        return ctx

    def done(self, form_list, form_dict, **kwargs):
        good_on_application, _ = self.post_software_to_application(form_dict)
        good_on_application = good_on_application["good"]
        self.good_on_application = good_on_application

        return redirect(self.get_success_url())
