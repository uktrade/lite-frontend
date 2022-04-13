import logging
import requests

from datetime import date
from http import HTTPStatus

from django.conf import settings
from django.http import Http404
from django.shortcuts import redirect
from django.urls import reverse
from django.utils.functional import cached_property
from django.views.generic import FormView

from core.auth.views import LoginRequiredMixin
from lite_forms.generators import error_page

from exporter.applications.services import get_application
from exporter.core.helpers import (
    get_document_data,
    str_to_bool,
)
from exporter.core.wizard.conditionals import C
from exporter.core.wizard.payloads import MergingPayloadBuilder
from exporter.core.wizard.views import BaseSessionWizardView
from exporter.goods.services import (
    delete_good_document,
    edit_firearm,
    get_good,
    post_good_documents,
    update_good_document_data,
)
from exporter.goods.forms.firearms import (
    FirearmCalibreForm,
    FirearmCategoryForm,
    FirearmDocumentAvailability,
    FirearmDocumentSensitivityForm,
    FirearmDocumentUploadForm,
    FirearmNameForm,
    FirearmProductControlListEntryForm,
    FirearmPvGradingDetailsForm,
    FirearmPvGradingForm,
    FirearmReplicaForm,
)

from .conditionals import (
    is_document_sensitive,
    is_product_document_available,
    is_pv_graded,
)
from .constants import AddGoodFirearmSteps
from .exceptions import ServiceError
from .payloads import (
    FirearmEditProductDocumentAvailabilityPayloadBuilder,
    FirearmEditProductDocumentSensitivityPayloadBuilder,
    get_cleaned_data,
    get_firearm_details_cleaned_data,
    get_pv_grading_good_payload,
    get_pv_grading_payload,
)


logger = logging.getLogger(__name__)


class BaseEditView(LoginRequiredMixin, FormView):
    template_name = "core/form.html"

    @cached_property
    def application_id(self):
        return str(self.kwargs["pk"])

    @cached_property
    def good_id(self):
        return str(self.kwargs["good_pk"])

    @cached_property
    def good(self):
        try:
            good = get_good(self.request, self.good_id, full_detail=True)[0]
        except requests.exceptions.HTTPError:
            raise Http404

        return good

    def dispatch(self, request, *args, **kwargs):
        if not settings.FEATURE_FLAG_PRODUCT_2_0:
            raise Http404

        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse("applications:product_summary", kwargs=self.kwargs)

    def get_edit_payload(self, form):
        raise NotImplementedError(f"Implement `get_edit_payload` for {self.__class__.__name__}")

    def form_valid(self, form):
        edit_firearm(self.request, self.good_id, self.get_edit_payload(form))
        return super().form_valid(form)


class BaseGoodEditView(BaseEditView):
    def get_edit_payload(self, form):
        return get_cleaned_data(form)


class BaseFirearmEditView(BaseEditView):
    def get_edit_payload(self, form):
        return get_firearm_details_cleaned_data(form)


class FirearmEditName(BaseGoodEditView):
    form_class = FirearmNameForm

    def get_initial(self):
        return {"name": self.good["name"]}


class FirearmEditCategory(BaseFirearmEditView):
    form_class = FirearmCategoryForm

    def get_initial(self):
        firearm_details = self.good["firearm_details"]
        categories = [category["key"] for category in firearm_details["category"]]
        return {"category": categories}


class FirearmEditCalibre(BaseFirearmEditView):
    form_class = FirearmCalibreForm

    def get_initial(self):
        return {"calibre": self.good["firearm_details"]["calibre"]}


class FirearmEditControlListEntry(BaseGoodEditView):
    form_class = FirearmProductControlListEntryForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        return {**kwargs, "request": self.request}

    def get_initial(self):
        control_list_entries = []
        is_good_controlled = self.good["is_good_controlled"]["key"]
        if is_good_controlled == "True":
            control_list_entries = [clc["rating"] for clc in self.good.get("control_list_entries", [])]

        return {
            "is_good_controlled": is_good_controlled,
            "control_list_entries": control_list_entries,
        }


class FirearmEditReplica(BaseFirearmEditView):
    form_class = FirearmReplicaForm

    def get_initial(self):
        firearm_details = self.good["firearm_details"]
        return {
            "is_replica": firearm_details["is_replica"],
            "replica_description": firearm_details["replica_description"],
        }


class FirearmEditPvGradingPayloadBuilder(MergingPayloadBuilder):
    payload_dict = {
        AddGoodFirearmSteps.PV_GRADING: get_pv_grading_payload,
        AddGoodFirearmSteps.PV_GRADING_DETAILS: get_pv_grading_good_payload,
    }


class FirearmEditPvGrading(LoginRequiredMixin, BaseSessionWizardView):

    form_list = [
        (AddGoodFirearmSteps.PV_GRADING, FirearmPvGradingForm),
        (AddGoodFirearmSteps.PV_GRADING_DETAILS, FirearmPvGradingDetailsForm),
    ]

    condition_dict = {
        AddGoodFirearmSteps.PV_GRADING_DETAILS: is_pv_graded,
    }

    @cached_property
    def good_id(self):
        return str(self.kwargs["good_pk"])

    @cached_property
    def good(self):
        try:
            good = get_good(self.request, self.good_id, full_detail=True)[0]
        except requests.exceptions.HTTPError:
            raise Http404

        return good

    def get_pv_grading_payload(self, dict):
        return {
            "is_pv_graded": "yes" if dict["is_pv_graded"] else "no",
        }

    def get_form_initial(self, step):
        initial = {}
        if step == AddGoodFirearmSteps.PV_GRADING:
            initial = {"is_pv_graded": str_to_bool(self.good["is_pv_graded"].get("key"))}
        elif step == AddGoodFirearmSteps.PV_GRADING_DETAILS and self.good["pv_grading_details"]:
            pv_grading_details = self.good["pv_grading_details"]
            initial = {
                "prefix": pv_grading_details.get("prefix"),
                "grading": pv_grading_details["grading"].get("key"),
                "suffix": pv_grading_details.get("suffix"),
                "issuing_authority": pv_grading_details.get("issuing_authority"),
                "reference": pv_grading_details.get("reference"),
                "date_of_issue": date.fromisoformat(pv_grading_details["date_of_issue"])
                if pv_grading_details["date_of_issue"]
                else None,
            }
        return initial

    def get_form_kwargs(self, step=None):
        kwargs = super().get_form_kwargs(step)

        if step == AddGoodFirearmSteps.PV_GRADING_DETAILS:
            kwargs["request"] = self.request
        return kwargs

    def get_payload(self, form_dict):
        return FirearmEditPvGradingPayloadBuilder().build(form_dict)

    def edit_firearm(self, form_dict):
        payload = self.get_payload(form_dict)
        api_resp_data, status_code = edit_firearm(
            self.request,
            self.good_id,
            payload,
        )

        return api_resp_data, status_code

    def done(self, form_list, form_dict, **kwargs):
        self.edit_firearm(form_dict)
        return redirect(reverse("applications:product_summary", kwargs=self.kwargs))


def get_product_document(good):
    is_document_available = good["is_document_available"]
    is_document_sensitive = good["is_document_sensitive"]
    if not is_document_available or (is_document_available and is_document_sensitive):
        return None

    if not good["documents"]:
        return None

    # when creating new product we can only add one document but we save it as
    # a list because from the product detail page user can add multiple documents
    return good["documents"][0]


class FirearmEditProductDocumentView(BaseGoodEditView):
    form_class = FirearmDocumentUploadForm

    @cached_property
    def product_document(self):
        return get_product_document(self.good)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        return {**kwargs, "good_id": self.good_id, "document": self.product_document}

    def get_initial(self):
        return {"description": self.product_document["description"] if self.product_document else ""}

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
            api_resp_data, status_code = post_good_documents(
                request=self.request,
                pk=self.good_id,
                json=payload,
            )
            if status_code != HTTPStatus.CREATED:
                raise ServiceError(
                    status_code,
                    api_resp_data,
                    "Error product document when creating firearm - response was: %s - %s",
                    "Unexpected error adding document to firearm",
                )

            # Delete existing document
            if existing_product_document:
                api_resp_data, status_code = delete_good_document(
                    self.request, self.good_id, self.product_document["id"]
                )
                if status_code != HTTPStatus.OK:
                    raise ServiceError(
                        status_code,
                        api_resp_data,
                        "Error deleting the product document - response was: %s - %s",
                        "Unexpected error deleting product document",
                    )
        elif self.product_document["description"] != description:
            api_resp_data, status_code = update_good_document_data(
                self.request, self.good_id, self.product_document["id"], payload
            )
            if status_code != HTTPStatus.OK:
                raise ServiceError(
                    status_code,
                    api_resp_data,
                    "Error updating the product document description - response was: %s - %s",
                    "Unexpected error updating product document description",
                )

        return redirect(self.get_success_url())


class AddGoodWizardCommon:
    @cached_property
    def application_id(self):
        return str(self.kwargs["pk"])

    @cached_property
    def good_id(self):
        return str(self.kwargs["good_pk"])

    @cached_property
    def good(self):
        try:
            good = get_good(self.request, self.good_id, full_detail=True)[0]
        except requests.exceptions.HTTPError:
            raise Http404

        return good

    def dispatch(self, request, *args, **kwargs):
        if not settings.FEATURE_FLAG_PRODUCT_2_0:
            raise Http404

        try:
            self.application = get_application(self.request, self.application_id)
        except requests.exceptions.HTTPError:
            raise Http404

        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, form, **kwargs):
        ctx = super().get_context_data(form, **kwargs)

        ctx["hide_step_count"] = True
        ctx["back_link_url"] = reverse("applications:product_summary", kwargs=self.kwargs)
        ctx["title"] = form.Layout.TITLE
        return ctx

    def get_success_url(self):
        return reverse("applications:product_summary", kwargs=self.kwargs)

    def handle_service_error(self, service_error):
        logger.error(
            service_error.log_message,
            service_error.status_code,
            service_error.response,
            exc_info=True,
        )
        return error_page(self.request, service_error.user_message)

    def get_payload(self, form_dict):
        raise NotImplementedError(f"Implement `get_payload` on f{self.__class__.__name__}")

    def edit_firearm(self, good_pk, form_dict):
        payload = self.get_payload(form_dict)
        api_resp_data, status_code = edit_firearm(
            self.request,
            good_pk,
            payload,
        )
        if status_code != HTTPStatus.OK:
            raise ServiceError(
                status_code,
                api_resp_data,
                "Error updating firearm - response was: %s - %s",
                "Unexpected error updating firearm",
            )


class AddGoodDocumentWizardCommon(AddGoodWizardCommon):
    @cached_property
    def product_document(self):
        return get_product_document(self.good)

    def get_form_kwargs(self, step=None):
        kwargs = super().get_form_kwargs(step)

        if step == AddGoodFirearmSteps.PRODUCT_DOCUMENT_UPLOAD:
            kwargs["good_id"] = self.good_id
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
        data = self.get_cleaned_data_for_step(AddGoodFirearmSteps.PRODUCT_DOCUMENT_UPLOAD)
        return data.get("product_document", None)

    def get_product_document_payload(self):
        data = self.get_cleaned_data_for_step(AddGoodFirearmSteps.PRODUCT_DOCUMENT_UPLOAD)
        document = data["product_document"]
        payload = {
            **get_document_data(document),
            "description": data["description"],
        }
        return payload

    def post_product_documentation(self, good_pk):
        document_payload = self.get_product_document_payload()
        api_resp_data, status_code = post_good_documents(
            request=self.request,
            pk=good_pk,
            json=document_payload,
        )
        if status_code != HTTPStatus.CREATED:
            raise ServiceError(
                status_code,
                api_resp_data,
                "Error adding product document when creating firearm - response was: %s - %s",
                "Unexpected error adding document to firearm",
            )

    def delete_product_documentation(self, good_pk, document_pk):
        api_resp_data, status_code = delete_good_document(self.request, good_pk, document_pk)
        if status_code != HTTPStatus.OK:
            raise ServiceError(
                status_code,
                api_resp_data,
                "Error deleting the product document - response was: %s - %s",
                "Unexpected error deleting product document",
            )

    def update_product_document_data(self, good_pk, document_pk, payload):
        api_resp_data, status_code = update_good_document_data(self.request, good_pk, document_pk, payload)
        if status_code != HTTPStatus.OK:
            raise ServiceError(
                status_code,
                api_resp_data,
                "Error updating the product document description - response was: %s - %s",
                "Unexpected error updating product document description",
            )


class FirearmEditProductDocumentSensitivity(LoginRequiredMixin, AddGoodDocumentWizardCommon, BaseSessionWizardView):
    form_list = [
        (AddGoodFirearmSteps.PRODUCT_DOCUMENT_SENSITIVITY, FirearmDocumentSensitivityForm),
        (AddGoodFirearmSteps.PRODUCT_DOCUMENT_UPLOAD, FirearmDocumentUploadForm),
    ]

    condition_dict = {
        AddGoodFirearmSteps.PRODUCT_DOCUMENT_UPLOAD: C(is_product_document_available) & ~C(is_document_sensitive),
    }

    def get_cleaned_data_for_step(self, step):
        cleaned_data = super().get_cleaned_data_for_step(step)
        return {**cleaned_data, "is_document_available": True}

    def get_payload(self, form_dict):
        return FirearmEditProductDocumentSensitivityPayloadBuilder().build(form_dict)

    def done(self, form_list, form_dict, **kwargs):
        all_data = {k: v for form in form_list for k, v in form.cleaned_data.items()}
        is_document_sensitive = all_data.get("is_document_sensitive", None)

        try:
            self.edit_firearm(self.good_id, form_dict)

            existing_product_document = self.product_document
            if is_document_sensitive:
                if existing_product_document:
                    self.delete_product_documentation(self.good_id, existing_product_document["id"])
            else:
                description = all_data.get("description", "")
                if self.has_updated_product_documentation():
                    self.post_product_documentation(self.good_id)
                    if existing_product_document:
                        self.delete_product_documentation(self.good_id, existing_product_document["id"])
                elif existing_product_document and existing_product_document["description"] != description:
                    payload = {"description": description}
                    self.update_product_document_data(self.good_id, existing_product_document["id"], payload)

        except ServiceError as e:
            return self.handle_service_error(e)

        return redirect(self.get_success_url())


class FirearmEditProductDocumentAvailability(LoginRequiredMixin, AddGoodDocumentWizardCommon, BaseSessionWizardView):
    form_list = [
        (AddGoodFirearmSteps.PRODUCT_DOCUMENT_AVAILABILITY, FirearmDocumentAvailability),
        (AddGoodFirearmSteps.PRODUCT_DOCUMENT_SENSITIVITY, FirearmDocumentSensitivityForm),
        (AddGoodFirearmSteps.PRODUCT_DOCUMENT_UPLOAD, FirearmDocumentUploadForm),
    ]

    condition_dict = {
        AddGoodFirearmSteps.PRODUCT_DOCUMENT_SENSITIVITY: is_product_document_available,
        AddGoodFirearmSteps.PRODUCT_DOCUMENT_UPLOAD: C(is_product_document_available) & ~C(is_document_sensitive),
    }

    def get_payload(self, form_dict):
        return FirearmEditProductDocumentAvailabilityPayloadBuilder().build(form_dict)

    def done(self, form_list, form_dict, **kwargs):
        all_data = {k: v for form in form_list for k, v in form.cleaned_data.items()}
        is_document_available = all_data.get("is_document_available", None)
        is_document_sensitive = all_data.get("is_document_sensitive", None)

        try:
            self.edit_firearm(self.good_id, form_dict)

            existing_product_document = self.product_document
            if not is_document_available or (is_document_available and is_document_sensitive):
                if existing_product_document:
                    self.delete_product_documentation(self.good_id, existing_product_document["id"])
            else:
                description = all_data.get("description", "")
                if self.has_updated_product_documentation():
                    self.post_product_documentation(self.good_id)
                    if existing_product_document:
                        self.delete_product_documentation(self.good_id, existing_product_document["id"])
                elif existing_product_document and existing_product_document["description"] != description:
                    payload = {"description": description}
                    self.update_product_document_data(self.good_id, existing_product_document["id"], payload)

        except ServiceError as e:
            return self.handle_service_error(e)

        return redirect(self.get_success_url())
