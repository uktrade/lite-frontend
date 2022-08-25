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
from exporter.core.helpers import get_document_data
from exporter.goods.forms.common import (
    ProductControlListEntryForm,
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
    ProductQuantityAndValueForm,
)
from exporter.goods.forms.goods import ProductUsesInformationSecurityForm, ProductMilitaryUseForm

from exporter.goods.services import post_platform, post_good_documents
from exporter.applications.services import post_platform_good_on_application
from exporter.applications.views.goods.common.mixins import (
    ApplicationMixin,
    GoodMixin,
    NonFirearmsFlagMixin,
)
from exporter.applications.views.goods.common.conditionals import (
    is_pv_graded,
    is_product_document_available,
    is_document_sensitive,
    is_onward_exported,
)
from exporter.core.wizard.conditionals import C

from .constants import (
    AddGoodPlatformSteps,
    AddGoodPlatformToApplicationSteps,
)
from .payloads import (
    AddGoodPlatformPayloadBuilder,
    AddGoodPlatformToApplicationPayloadBuilder,
)


logger = logging.getLogger(__name__)


class AddGoodPlatform(
    LoginRequiredMixin,
    NonFirearmsFlagMixin,
    ApplicationMixin,
    BaseSessionWizardView,
    ProductUsesInformationSecurityForm,
):
    form_list = [
        (AddGoodPlatformSteps.NAME, ProductNameForm),
        (AddGoodPlatformSteps.PRODUCT_CONTROL_LIST_ENTRY, ProductControlListEntryForm),
        (AddGoodPlatformSteps.PART_NUMBER, ProductPartNumberForm),
        (AddGoodPlatformSteps.PV_GRADING, ProductPVGradingForm),
        (AddGoodPlatformSteps.PV_GRADING_DETAILS, ProductPVGradingDetailsForm),
        (AddGoodPlatformSteps.PRODUCT_USES_INFORMATION_SECURITY, ProductUsesInformationSecurityForm),
        (AddGoodPlatformSteps.PRODUCT_DOCUMENT_AVAILABILITY, ProductDocumentAvailabilityForm),
        (AddGoodPlatformSteps.PRODUCT_DOCUMENT_SENSITIVITY, ProductDocumentSensitivityForm),
        (AddGoodPlatformSteps.PRODUCT_DOCUMENT_UPLOAD, ProductDocumentUploadForm),
        (AddGoodPlatformSteps.PRODUCT_MILITARY_USE, ProductMilitaryUseForm),
    ]
    condition_dict = {
        AddGoodPlatformSteps.PV_GRADING_DETAILS: is_pv_graded,
        AddGoodPlatformSteps.PRODUCT_DOCUMENT_SENSITIVITY: is_product_document_available,
        AddGoodPlatformSteps.PRODUCT_DOCUMENT_UPLOAD: C(is_product_document_available) & ~C(is_document_sensitive),
    }

    def get_form_kwargs(self, step=None):
        kwargs = super().get_form_kwargs(step)

        if step == AddGoodPlatformSteps.PRODUCT_CONTROL_LIST_ENTRY:
            kwargs["request"] = self.request

        if step == AddGoodPlatformSteps.PV_GRADING_DETAILS:
            kwargs["request"] = self.request
        return kwargs

    def has_product_documentation(self):
        return self.condition_dict[AddGoodPlatformSteps.PRODUCT_DOCUMENT_UPLOAD](self)

    def get_product_document_payload(self):
        data = self.get_cleaned_data_for_step(AddGoodPlatformSteps.PRODUCT_DOCUMENT_UPLOAD)
        document = data["product_document"]
        payload = {
            **get_document_data(document),
            "description": data["description"],
        }
        return payload

    @expect_status(
        HTTPStatus.CREATED,
        "Error with product document when creating platform",
        "Unexpected error adding platform",
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
            "applications:platform_product_summary",
            kwargs={"pk": self.application["id"], "good_pk": self.good["id"]},
        )

    @expect_status(
        HTTPStatus.CREATED,
        "Error creating complete product",
        "Unexpected error adding complete product",
    )
    def post_platform(self, form_dict):
        payload = self.get_payload(form_dict)

        return post_platform(
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
            good, _ = self.post_platform(form_dict)
            self.good = good["good"]
            if self.has_product_documentation():
                self.post_product_documentation(self.good)
        except ServiceError as e:
            return self.handle_service_error(e)

        return redirect(self.get_success_url())


class AddGoodPlatformToApplication(
    LoginRequiredMixin,
    NonFirearmsFlagMixin,
    ApplicationMixin,
    GoodMixin,
    BaseSessionWizardView,
):
    form_list = [
        (AddGoodPlatformToApplicationSteps.ONWARD_EXPORTED, ProductOnwardExportedForm),
        (AddGoodPlatformToApplicationSteps.ONWARD_ALTERED_PROCESSED, ProductOnwardAlteredProcessedForm),
        (AddGoodPlatformToApplicationSteps.ONWARD_INCORPORATED, ProductOnwardIncorporatedForm),
        (AddGoodPlatformToApplicationSteps.QUANTITY_AND_VALUE, ProductQuantityAndValueForm),
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
            "applications:platform_on_application_summary",
            kwargs={
                "pk": self.kwargs["pk"],
                "good_on_application_pk": self.good_on_application["id"],
            },
        )

    def get_payload(self, form_dict):
        good_on_application_payload = AddGoodPlatformToApplicationPayloadBuilder().build(form_dict)
        return good_on_application_payload

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
            "applications:platform_product_summary",
            kwargs={
                "pk": self.kwargs["pk"],
                "good_pk": self.good["id"],
            },
        )
        ctx["title"] = form.Layout.TITLE

        return ctx

    def handle_service_error(self, service_error):
        logger.error(
            service_error.log_message,
            service_error.status_code,
            service_error.response,
            exc_info=True,
        )
        if settings.DEBUG:  # pragma: no cover
            raise service_error
        return error_page(self.request, service_error.user_message)

    def done(self, form_list, form_dict, **kwargs):
        try:
            good_on_application, _ = self.post_platform_to_application(form_dict)
            good_on_application = good_on_application["good"]
        except ServiceError as e:
            return self.handle_service_error(e)
        self.good_on_application = good_on_application

        return redirect(self.get_success_url())
