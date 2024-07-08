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
)
from exporter.goods.forms.goods import (
    ProductDeclaredAtCustomsForm,
    ProductSecurityFeaturesForm,
)
from exporter.goods.services import post_technology
from exporter.applications.services import post_technology_good_on_application
from exporter.applications.views.goods.common.mixins import ApplicationMixin, GoodMixin
from exporter.applications.views.goods.common.conditionals import (
    is_pv_graded,
    is_product_document_available,
    is_document_sensitive,
    is_onward_exported,
)
from core.wizard.conditionals import C

from .constants import (
    AddGoodTechnologySteps,
    AddGoodTechnologyToApplicationSteps,
)
from .payloads import (
    AddGoodTechnologyPayloadBuilder,
    AddGoodTechnologyToApplicationPayloadBuilder,
)

logger = logging.getLogger(__name__)


class AddGoodTechnology(
    LoginRequiredMixin,
    ApplicationMixin,
    BaseSessionWizardView,
    ProductSecurityFeaturesForm,
):
    form_list = [
        (AddGoodTechnologySteps.NAME, ProductNameForm),
        (AddGoodTechnologySteps.PRODUCT_CONTROL_LIST_ENTRY, ProductControlListEntryForm),
        (AddGoodTechnologySteps.PART_NUMBER, ProductPartNumberForm),
        (AddGoodTechnologySteps.PV_GRADING, ProductPVGradingForm),
        (AddGoodTechnologySteps.PV_GRADING_DETAILS, ProductPVGradingDetailsForm),
        (AddGoodTechnologySteps.SECURITY_FEATURES, ProductSecurityFeaturesForm),
        (AddGoodTechnologySteps.PRODUCT_DECLARED_AT_CUSTOMS, ProductDeclaredAtCustomsForm),
        (AddGoodTechnologySteps.PRODUCT_DOCUMENT_AVAILABILITY, ProductDocumentAvailabilityForm),
        (AddGoodTechnologySteps.PRODUCT_DOCUMENT_SENSITIVITY, ProductDocumentSensitivityForm),
        (AddGoodTechnologySteps.PRODUCT_DOCUMENT_UPLOAD, ProductDocumentUploadForm),
        (AddGoodTechnologySteps.PRODUCT_DESCRIPTION, ProductDescriptionForm),
        (AddGoodTechnologySteps.PRODUCT_MILITARY_USE, ProductMilitaryUseForm),
    ]
    condition_dict = {
        AddGoodTechnologySteps.PV_GRADING_DETAILS: is_pv_graded,
        AddGoodTechnologySteps.PRODUCT_DOCUMENT_SENSITIVITY: is_product_document_available,
        AddGoodTechnologySteps.PRODUCT_DOCUMENT_UPLOAD: C(is_product_document_available) & ~C(is_document_sensitive),
        AddGoodTechnologySteps.PRODUCT_DESCRIPTION: ~C(is_product_document_available),
    }

    def get_form_kwargs(self, step=None):
        kwargs = super().get_form_kwargs(step)

        if step == AddGoodTechnologySteps.PRODUCT_CONTROL_LIST_ENTRY:
            kwargs["request"] = self.request

        if step == AddGoodTechnologySteps.PV_GRADING_DETAILS:
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
        good_payload = AddGoodTechnologyPayloadBuilder().build(form_dict)
        return good_payload

    def get_success_url(self):
        return reverse(
            "applications:technology_product_summary",
            kwargs={"pk": self.application["id"], "good_pk": self.good["id"]},
        )

    @expect_status(
        HTTPStatus.CREATED,
        "Error creating complete product",
        "Unexpected error adding complete product",
    )
    def post_technology(self, form_dict):
        payload = self.get_payload(form_dict)

        return post_technology(
            self.request,
            payload,
        )

    def done(self, form_list, form_dict, **kwargs):
        good, _ = self.post_technology(form_dict)
        self.good = good["good"]

        ProductDocumentAction(self).run()

        return redirect(self.get_success_url())


class AddGoodTechnologyToApplication(
    LoginRequiredMixin,
    ApplicationMixin,
    GoodMixin,
    BaseSessionWizardView,
):
    form_list = [
        (AddGoodTechnologyToApplicationSteps.ONWARD_EXPORTED, ProductOnwardExportedForm),
        (AddGoodTechnologyToApplicationSteps.ONWARD_ALTERED_PROCESSED, ProductOnwardAlteredProcessedForm),
        (AddGoodTechnologyToApplicationSteps.ONWARD_INCORPORATED, ProductOnwardIncorporatedForm),
        (AddGoodTechnologyToApplicationSteps.QUANTITY_AND_VALUE, ProductQuantityAndValueForm),
    ]

    condition_dict = {
        AddGoodTechnologyToApplicationSteps.ONWARD_ALTERED_PROCESSED: is_onward_exported,
        AddGoodTechnologyToApplicationSteps.ONWARD_INCORPORATED: is_onward_exported,
    }

    def get_form_kwargs(self, step=None):
        kwargs = super().get_form_kwargs(step)
        return kwargs

    def get_success_url(self):
        return reverse(
            "applications:technology_on_application_summary",
            kwargs={
                "pk": self.kwargs["pk"],
                "good_on_application_pk": self.good_on_application["id"],
            },
        )

    def get_payload(self, form_dict):
        good_on_application_payload = AddGoodTechnologyToApplicationPayloadBuilder().build(form_dict)
        return good_on_application_payload

    @expect_status(
        HTTPStatus.CREATED,
        "Error adding technology to application",
        "Unexpected error adding technology to application",
    )
    def post_technology_to_application(self, form_dict):
        payload = self.get_payload(form_dict)
        return post_technology_good_on_application(
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
        good_on_application, _ = self.post_technology_to_application(form_dict)
        good_on_application = good_on_application["good"]
        self.good_on_application = good_on_application

        return redirect(self.get_success_url())
