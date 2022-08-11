import logging

from http import HTTPStatus

from django.conf import settings
from django.shortcuts import redirect
from django.urls import reverse
from django.utils.functional import cached_property
from django.views.generic import FormView

from lite_forms.generators import error_page

from core.auth.views import LoginRequiredMixin

from exporter.applications.views.goods.common.conditionals import (
    is_document_sensitive,
    is_product_document_available,
    is_pv_graded,
)
from exporter.applications.views.goods.common.helpers import get_product_document
from exporter.applications.views.goods.common.initial import (
    get_control_list_entry_initial_data,
    get_name_initial_data,
    get_pv_grading_initial_data,
    get_pv_grading_details_initial_data,
)
from exporter.applications.views.goods.common.mixins import ApplicationMixin, GoodMixin
from exporter.applications.views.goods.common.payloads import (
    get_cleaned_data,
    get_pv_grading_details_payload,
    ProductEditProductDocumentAvailabilityPayloadBuilder,
    ProductEditPVGradingPayloadBuilder,
)
from exporter.core.common.decorators import expect_status
from exporter.core.common.exceptions import ServiceError
from exporter.core.helpers import get_document_data
from exporter.core.wizard.conditionals import C
from exporter.core.wizard.views import BaseSessionWizardView
from exporter.goods.forms.common import (
    ProductControlListEntryForm,
    ProductDocumentAvailability,
    ProductDocumentSensitivityForm,
    ProductDocumentUploadForm,
    ProductNameForm,
    ProductPVGradingDetailsForm,
    ProductPVGradingForm,
)
from exporter.goods.forms.goods import ProductUsesInformationSecurityForm
from exporter.goods.services import (
    delete_good_document,
    edit_platform,
    post_good_documents,
    update_good_document_data,
)

from .constants import AddGoodPlatformSteps
from .mixins import NonFirearmsFlagMixin


logger = logging.getLogger(__name__)


class BaseEditView(
    LoginRequiredMixin,
    NonFirearmsFlagMixin,
    ApplicationMixin,
    GoodMixin,
    FormView,
):
    template_name = "core/form.html"

    def get_success_url(self):
        return reverse("applications:platform_summary", kwargs=self.kwargs)

    def get_edit_payload(self, form):
        raise NotImplementedError(f"Implement `get_edit_payload` for {self.__class__.__name__}")

    def form_valid(self, form):
        edit_platform(self.request, self.good["id"], self.get_edit_payload(form))
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)

        ctx["back_link_url"] = reverse("applications:platform_summary", kwargs=self.kwargs)

        return ctx


class BasePlatformEditView(BaseEditView):
    def get_edit_payload(self, form):
        return get_cleaned_data(form)


class PlatformEditName(BasePlatformEditView):
    form_class = ProductNameForm

    def get_initial(self):
        return get_name_initial_data(self.good)


class PlatformEditControlListEntry(BasePlatformEditView):
    form_class = ProductControlListEntryForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        return {**kwargs, "request": self.request}

    def get_initial(self):
        return get_control_list_entry_initial_data(self.good)


class BaseEditWizardView(
    LoginRequiredMixin,
    NonFirearmsFlagMixin,
    ApplicationMixin,
    GoodMixin,
    BaseSessionWizardView,
):
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

    def get_context_data(self, form, **kwargs):
        ctx = super().get_context_data(form, **kwargs)

        ctx["back_link_url"] = reverse("applications:platform_summary", kwargs=self.kwargs)
        ctx["title"] = form.Layout.TITLE
        return ctx

    def get_success_url(self):
        return reverse("applications:platform_summary", kwargs=self.kwargs)

    def get_payload(self, form_dict):
        raise NotImplementedError(f"Implement `get_payload` on f{self.__class__.__name__}")

    @expect_status(HTTPStatus.OK, "Error updating firearm", "Unexpected error updating firearm")
    def edit_platform(self, good_pk, form_dict):
        payload = self.get_payload(form_dict)
        return edit_platform(self.request, good_pk, payload)


class PlatformEditPVGrading(BaseEditWizardView):
    form_list = [
        (AddGoodPlatformSteps.PV_GRADING, ProductPVGradingForm),
        (AddGoodPlatformSteps.PV_GRADING_DETAILS, ProductPVGradingDetailsForm),
    ]
    condition_dict = {
        AddGoodPlatformSteps.PV_GRADING_DETAILS: is_pv_graded,
    }

    def get_form_initial(self, step):
        initial = {}
        if step == AddGoodPlatformSteps.PV_GRADING:
            initial = get_pv_grading_initial_data(self.good)
        elif step == AddGoodPlatformSteps.PV_GRADING_DETAILS and self.good["pv_grading_details"]:
            initial = get_pv_grading_details_initial_data(self.good)
        return initial

    def get_form_kwargs(self, step=None):
        kwargs = super().get_form_kwargs(step)

        if step == AddGoodPlatformSteps.PV_GRADING_DETAILS:
            kwargs["request"] = self.request
        return kwargs

    def get_payload(self, form_dict):
        return ProductEditPVGradingPayloadBuilder().build(form_dict)

    def done(self, form_list, form_dict, **kwargs):
        try:
            self.edit_platform(self.good["id"], form_dict)
        except ServiceError as e:
            return self.handle_service_error(e)

        return redirect(self.get_success_url())


class PlatformEditPVGradingDetails(BasePlatformEditView):
    form_class = ProductPVGradingDetailsForm

    def get_initial(self):
        return get_pv_grading_details_initial_data(self.good)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        return {**kwargs, "request": self.request}

    def get_edit_payload(self, form):
        grading_details = get_pv_grading_details_payload(form)
        return {"is_pv_graded": self.good["is_pv_graded"].get("key"), **grading_details}


class PlatformEditUsesInformationSecurity(BasePlatformEditView):
    form_class = ProductUsesInformationSecurityForm

    def get_initial(self):
        if not self.good["uses_information_security"]:
            return {
                "uses_information_security": self.good["uses_information_security"],
            }

        return {
            "uses_information_security": self.good["uses_information_security"],
            "information_security_details": self.good["information_security_details"],
        }

    def get_edit_payload(self, form):
        return get_cleaned_data(form)


class BaseEditProductDocumentView(BaseEditWizardView):
    @cached_property
    def product_document(self):
        return get_product_document(self.good)

    def get_form_kwargs(self, step=None):
        kwargs = super().get_form_kwargs(step)

        if step == AddGoodPlatformSteps.PRODUCT_DOCUMENT_UPLOAD:
            kwargs["good_id"] = self.good["id"]
            kwargs["document"] = self.product_document

        return kwargs

    def get_form_initial(self, step):
        return {
            "is_document_available": self.good["is_document_available"],
            "no_document_comments": self.good["no_document_comments"],
            "is_document_sensitive": self.good["is_document_sensitive"],
            "description": self.product_document["description"] if self.product_document else "",
        }

    def has_updated_product_documentation(self):
        data = self.get_cleaned_data_for_step(AddGoodPlatformSteps.PRODUCT_DOCUMENT_UPLOAD)
        return data.get("product_document", None)

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
        "Error adding product document when creating firearm",
        "Unexpected error adding document to firearm",
    )
    def post_product_documentation(self, good_pk):
        document_payload = self.get_product_document_payload()
        return post_good_documents(
            request=self.request,
            pk=good_pk,
            json=document_payload,
        )

    @expect_status(HTTPStatus.OK, "Error deleting the product document", "Unexpected error deleting product document")
    def delete_product_documentation(self, good_pk, document_pk):
        return delete_good_document(self.request, good_pk, document_pk)

    @expect_status(
        HTTPStatus.OK,
        "Error updating the product document description",
        "Unexpected error updating product document description",
    )
    def update_product_document_data(self, good_pk, document_pk, payload):
        return update_good_document_data(self.request, good_pk, document_pk, payload)


class PlatformEditProductDocumentAvailability(BaseEditProductDocumentView):
    form_list = [
        (AddGoodPlatformSteps.PRODUCT_DOCUMENT_AVAILABILITY, ProductDocumentAvailability),
        (AddGoodPlatformSteps.PRODUCT_DOCUMENT_SENSITIVITY, ProductDocumentSensitivityForm),
        (AddGoodPlatformSteps.PRODUCT_DOCUMENT_UPLOAD, ProductDocumentUploadForm),
    ]

    condition_dict = {
        AddGoodPlatformSteps.PRODUCT_DOCUMENT_SENSITIVITY: is_product_document_available,
        AddGoodPlatformSteps.PRODUCT_DOCUMENT_UPLOAD: C(is_product_document_available) & ~C(is_document_sensitive),
    }

    def get_payload(self, form_dict):
        return ProductEditProductDocumentAvailabilityPayloadBuilder().build(form_dict)

    def done(self, form_list, form_dict, **kwargs):
        all_data = {k: v for form in form_list for k, v in form.cleaned_data.items()}
        is_document_available = all_data.get("is_document_available", None)
        is_document_sensitive = all_data.get("is_document_sensitive", None)

        try:
            self.edit_platform(self.good["id"], form_dict)

            existing_product_document = self.product_document
            if not is_document_available or (is_document_available and is_document_sensitive):
                if existing_product_document:
                    self.delete_product_documentation(self.good["id"], existing_product_document["id"])
            else:
                description = all_data.get("description", "")
                if self.has_updated_product_documentation():
                    self.post_product_documentation(self.good["id"])
                    if existing_product_document:
                        self.delete_product_documentation(self.good["id"], existing_product_document["id"])
                elif existing_product_document and existing_product_document["description"] != description:
                    payload = {"description": description}
                    self.update_product_document_data(self.good["id"], existing_product_document["id"], payload)

        except ServiceError as e:
            return self.handle_service_error(e)

        return redirect(self.get_success_url())
