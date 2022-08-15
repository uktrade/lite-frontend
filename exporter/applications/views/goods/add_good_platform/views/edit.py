import logging

from http import HTTPStatus

from django.shortcuts import redirect
from django.urls import reverse
from django.utils.functional import cached_property

from exporter.applications.views.goods.common.conditionals import is_pv_graded
from exporter.applications.views.goods.common.edit import (
    BaseEditControlListEntry,
    BaseEditName,
    BaseEditProductDocumentAvailability,
    BaseEditProductDocumentSensitivity,
    BaseEditProductDocumentView,
    BaseProductEditView,
    BaseProductEditWizardView,
)
from exporter.applications.views.goods.common.helpers import get_product_document
from exporter.applications.views.goods.common.initial import (
    get_pv_grading_initial_data,
    get_pv_grading_details_initial_data,
)
from exporter.applications.views.goods.common.payloads import (
    get_cleaned_data,
    get_pv_grading_details_payload,
    ProductEditPVGradingPayloadBuilder,
)
from exporter.core.common.decorators import expect_status
from exporter.core.helpers import get_document_data
from exporter.goods.forms.common import (
    ProductDocumentUploadForm,
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
    NonFirearmsFlagMixin,
    BaseProductEditView,
):
    def get_success_url(self):
        return reverse("applications:platform_product_summary", kwargs=self.kwargs)

    def edit_object(self, request, good_id, payload):
        edit_platform(request, good_id, payload)


class BasePlatformEditView(BaseEditView):
    def get_edit_payload(self, form):
        return get_cleaned_data(form)


class PlatformEditName(BaseEditName, BasePlatformEditView):
    pass


class PlatformEditControlListEntry(BaseEditControlListEntry, BasePlatformEditView):
    pass


class BasePlatformEditWizardView(
    NonFirearmsFlagMixin,
    BaseProductEditWizardView,
):
    def get_success_url(self):
        return reverse("applications:platform_product_summary", kwargs=self.kwargs)

    def edit_object(self, request, good_pk, payload):
        return edit_platform(self.request, good_pk, payload)


class PlatformEditPVGrading(BasePlatformEditWizardView):
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


class BasePlatformEditProductDocumentView(
    BaseEditProductDocumentView,
    BasePlatformEditWizardView,
):
    pass


class PlatformEditProductDocumentAvailability(
    BaseEditProductDocumentAvailability,
    BasePlatformEditProductDocumentView,
):
    pass


class PlatformEditProductDocumentSensitivity(
    BaseEditProductDocumentSensitivity,
    BasePlatformEditProductDocumentView,
):
    pass


class PlatformEditProductDocumentView(BasePlatformEditView):
    form_class = ProductDocumentUploadForm

    @cached_property
    def product_document(self):
        return get_product_document(self.good)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        return {**kwargs, "good_id": self.good["id"], "document": self.product_document}

    def get_initial(self):
        return {"description": self.product_document["description"] if self.product_document else ""}

    @expect_status(
        HTTPStatus.CREATED,
        "Error product document when creating firearm",
        "Unexpected error adding document to firearm",
    )
    def post_good_documents(self, payload):
        return post_good_documents(
            request=self.request,
            pk=self.good["id"],
            json=payload,
        )

    @expect_status(
        HTTPStatus.OK,
        "Error deleting the product document",
        "Unexpected error deleting product document",
    )
    def delete_good_document(self):
        return delete_good_document(
            self.request,
            self.good["id"],
            self.product_document["id"],
        )

    @expect_status(
        HTTPStatus.OK,
        "Error updating the product document description",
        "Unexpected error updating product document description",
    )
    def update_good_document_data(self, payload):
        return update_good_document_data(
            self.request,
            self.good["id"],
            self.product_document["id"],
            payload,
        )

    def form_valid(self, form):
        existing_product_document = self.product_document
        product_document = form.cleaned_data.get("product_document", None)
        description = form.cleaned_data.get("description", "")
        payload = {"description": description}
        if product_document:
            payload = {
                **get_document_data(product_document),
                **payload,
            }
            self.post_good_documents(payload)

            # Delete existing document
            if existing_product_document:
                self.delete_good_document()

        elif self.product_document["description"] != description:
            self.update_good_document_data(payload)

        return redirect(self.get_success_url())
