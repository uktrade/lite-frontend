import logging

from http import HTTPStatus

from django.shortcuts import redirect
from django.utils.functional import cached_property
from django.views.generic import FormView

from core.auth.views import LoginRequiredMixin
from core.decorators import expect_status

from core.helpers import get_document_data
from core.wizard.conditionals import C
from core.wizard.views import BaseSessionWizardView
from exporter.goods.forms.common import (
    ProductDescriptionForm,
    ProductDocumentAvailabilityForm,
    ProductDocumentSensitivityForm,
    ProductDocumentUploadForm,
)
from exporter.goods.services import (
    delete_good_document,
    post_good_documents,
    update_good_document_data,
)

from .conditionals import (
    is_document_sensitive,
    is_product_document_available,
)
from . import constants
from .helpers import get_product_document
from .mixins import (
    ApplicationMixin,
    GoodMixin,
)
from .payloads import (
    ProductEditProductDocumentAvailabilityPayloadBuilder,
    ProductEditProductDocumentSensitivityPayloadBuilder,
)


logger = logging.getLogger(__name__)


class BaseProductEditView(
    LoginRequiredMixin,
    ApplicationMixin,
    GoodMixin,
    FormView,
):
    template_name = "core/form.html"

    def get_success_url(self):
        raise NotImplementedError(f"Implement `get_success_url` for {self.__class__.__name__}")

    def get_back_link_url(self):
        return self.get_success_url()

    def get_edit_payload(self, form):
        raise NotImplementedError(f"Implement `get_edit_payload` for {self.__class__.__name__}")

    def edit_object(self, request, good_id, payload):
        raise NotImplementedError(f"Implement `edit_object` for {self.__class__.__name__}")

    def form_valid(self, form):
        self.edit_object(self.request, self.good["id"], self.get_edit_payload(form))
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)

        ctx["back_link_url"] = self.get_back_link_url()
        ctx["title"] = self.form_class.Layout.TITLE

        return ctx


class BaseEditProductDescription:
    form_class = ProductDescriptionForm

    def get_initial(self):
        return {
            "product_description": self.good["product_description"],
        }


class BaseProductEditWizardView(
    LoginRequiredMixin,
    ApplicationMixin,
    GoodMixin,
    BaseSessionWizardView,
):
    def get_success_url(self):
        raise NotImplementedError(f"Implement `get_success_url` for {self.__class__.__name__}")

    def get_back_link_url(self):
        return self.get_success_url()

    def get_context_data(self, form, **kwargs):
        ctx = super().get_context_data(form, **kwargs)

        ctx["back_link_url"] = self.get_success_url()
        ctx["title"] = form.Layout.TITLE
        return ctx

    def get_payload(self, form_dict):
        raise NotImplementedError(f"Implement `get_payload` on f{self.__class__.__name__}")

    @expect_status(
        HTTPStatus.OK,
        "Error updating product",
        "Unexpected error updating product",
    )
    def edit_object(self, request, good_pk, payload):
        raise NotImplementedError(f"Implement `edit_object` on f{self.__class__.__name__}")

    def process_forms(self, form_list, form_dict, **kwargs):
        self.edit_object(self.request, self.good["id"], self.get_payload(form_dict))

    def done(self, form_list, form_dict, **kwargs):
        self.process_forms(form_list, form_dict, **kwargs)

        return redirect(self.get_success_url())


class BaseEditProductDocumentView:
    @cached_property
    def product_document(self):
        return get_product_document(self.good)

    def get_form_kwargs(self, step=None):
        kwargs = super().get_form_kwargs(step)

        if step == constants.PRODUCT_DOCUMENT_UPLOAD:
            kwargs["good_id"] = self.good["id"]
            kwargs["document"] = self.product_document

        return kwargs

    def get_form_initial(self, step):
        return {
            "is_document_available": self.good["is_document_available"],
            "no_document_comments": self.good["no_document_comments"],
            "is_document_sensitive": self.good["is_document_sensitive"],
            "description": self.product_document["description"] if self.product_document else "",
            "product_description": self.good.get("product_description", ""),
        }

    def has_updated_product_documentation(self):
        data = self.get_cleaned_data_for_step(constants.PRODUCT_DOCUMENT_UPLOAD)
        return data.get("product_document", None)

    def get_product_document_payload(self):
        data = self.get_cleaned_data_for_step(constants.PRODUCT_DOCUMENT_UPLOAD)
        document = data["product_document"]
        payload = {
            **get_document_data(document),
            "description": data["description"],
        }
        return payload

    @expect_status(
        HTTPStatus.CREATED,
        "Error adding product document when creating product",
        "Unexpected error adding document to product",
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


class BaseEditProductDocumentAvailability:
    form_list = [
        (constants.PRODUCT_DOCUMENT_AVAILABILITY, ProductDocumentAvailabilityForm),
        (constants.PRODUCT_DESCRIPTION, ProductDescriptionForm),
        (constants.PRODUCT_DOCUMENT_SENSITIVITY, ProductDocumentSensitivityForm),
        (constants.PRODUCT_DOCUMENT_UPLOAD, ProductDocumentUploadForm),
    ]

    condition_dict = {
        constants.PRODUCT_DESCRIPTION: ~C(is_product_document_available),
        constants.PRODUCT_DOCUMENT_SENSITIVITY: is_product_document_available,
        constants.PRODUCT_DOCUMENT_UPLOAD: C(is_product_document_available) & ~C(is_document_sensitive),
    }

    def get_payload(self, form_dict):
        return ProductEditProductDocumentAvailabilityPayloadBuilder().build(form_dict)

    def process_forms(self, form_list, form_dict, **kwargs):
        super().process_forms(form_list, form_dict, **kwargs)

        all_data = {k: v for form in form_list for k, v in form.cleaned_data.items()}
        is_document_available = all_data.get("is_document_available", None)
        is_document_sensitive = all_data.get("is_document_sensitive", None)

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


class BaseEditProductDocumentSensitivity:
    form_list = [
        (constants.PRODUCT_DOCUMENT_SENSITIVITY, ProductDocumentSensitivityForm),
        (constants.PRODUCT_DOCUMENT_UPLOAD, ProductDocumentUploadForm),
    ]

    condition_dict = {
        constants.PRODUCT_DOCUMENT_UPLOAD: C(is_product_document_available) & ~C(is_document_sensitive),
    }

    def get_cleaned_data_for_step(self, step):
        cleaned_data = super().get_cleaned_data_for_step(step)
        return {**cleaned_data, "is_document_available": True}

    def get_payload(self, form_dict):
        return ProductEditProductDocumentSensitivityPayloadBuilder().build(form_dict)

    def process_forms(self, form_list, form_dict, **kwargs):
        super().process_forms(form_list, form_dict, **kwargs)

        all_data = {k: v for form in form_list for k, v in form.cleaned_data.items()}
        is_document_sensitive = all_data.get("is_document_sensitive", None)

        existing_product_document = self.product_document
        if is_document_sensitive:
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


class BaseProductDocumentUpload:
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
