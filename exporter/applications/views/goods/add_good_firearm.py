import logging
import requests

from http import HTTPStatus

from django.conf import settings
from django.http import Http404
from django.shortcuts import redirect
from django.urls import reverse
from django.utils.functional import cached_property
from django.views.generic import TemplateView, FormView

from core.auth.views import LoginRequiredMixin

from exporter.applications.services import get_application, post_additional_document
from exporter.core.constants import FirearmsProductType
from exporter.core.helpers import get_document_data, get_rfd_certificate, has_valid_rfd_certificate
from exporter.core.wizard.conditionals import C
from exporter.core.wizard.views import BaseSessionWizardView
from exporter.goods.forms import GroupTwoProductTypeForm
from exporter.goods.forms.firearms import (
    FirearmAttachRFDCertificate,
    FirearmCalibreForm,
    FirearmCategoryForm,
    FirearmNameForm,
    FirearmProductControlListEntryForm,
    FirearmPvGradingForm,
    FirearmPvGradingDetailsForm,
    FirearmRegisteredFirearmsDealerForm,
    FirearmReplicaForm,
    FirearmRFDValidityForm,
    FirearmDocumentAvailability,
    FirearmDocumentSensitivityForm,
    FirearmDocumentUploadForm,
)
from exporter.goods.services import post_firearm, edit_firearm, post_good_documents, get_good, get_good_documents
from lite_forms.generators import error_page


logger = logging.getLogger(__name__)


class AddGoodFirearmSteps:
    CATEGORY = "CATEGORY"
    NAME = "NAME"
    PRODUCT_CONTROL_LIST_ENTRY = "PRODUCT_CONTROL_LIST_ENTRY"
    PV_GRADING = "PV_GRADING"
    PV_GRADING_DETAILS = "PV_GRADING_DETAILS"
    CALIBRE = "CALIBRE"
    IS_REPLICA = "IS_REPLICA"
    IS_RFD_CERTIFICATE_VALID = "IS_RFD_CERTIFICATE_VALID"
    IS_REGISTERED_FIREARMS_DEALER = "IS_REGISTERED_FIREARMS_DEALER"
    ATTACH_RFD_CERTIFICATE = "ATTACH_RFD_CERTIFICATE"
    PRODUCT_DOCUMENT_AVAILABILITY = "PRODUCT_DOCUMENT_AVAILABILITY"
    PRODUCT_DOCUMENT_SENSITIVITY = "PRODUCT_DOCUMENT_SENSITIVITY"
    PRODUCT_DOCUMENT_UPLOAD = "PRODUCT_DOCUMENT_UPLOAD"


def is_product_document_available(wizard):
    cleaned_data = wizard.get_cleaned_data_for_step(AddGoodFirearmSteps.PRODUCT_DOCUMENT_AVAILABILITY)
    return cleaned_data.get("is_document_available")


def is_document_sensitive(wizard):
    cleaned_data = wizard.get_cleaned_data_for_step(AddGoodFirearmSteps.PRODUCT_DOCUMENT_SENSITIVITY)
    return cleaned_data.get("is_document_sensitive")


def has_rfd_certificate(wizard):
    return has_valid_rfd_certificate(wizard.application)


def is_pv_graded(wizard):
    add_goods_cleaned_data = wizard.get_cleaned_data_for_step(AddGoodFirearmSteps.PV_GRADING)
    return add_goods_cleaned_data.get("is_pv_graded")


def has_user_marked_rfd_certificate_invalid(wizard):
    is_rfd_certificate_valid_cleaned_data = wizard.get_cleaned_data_for_step(
        AddGoodFirearmSteps.IS_RFD_CERTIFICATE_VALID
    )
    return not is_rfd_certificate_valid_cleaned_data.get("is_rfd_valid", False)


def has_user_marked_as_registered_firearms_dealer(wizard):
    is_registered_firearms_dealer_cleaned_data = wizard.get_cleaned_data_for_step(
        AddGoodFirearmSteps.IS_REGISTERED_FIREARMS_DEALER
    )
    return is_registered_firearms_dealer_cleaned_data.get("is_registered_firearm_dealer", False)


def get_cleaned_data(form):
    return form.cleaned_data


def get_pv_grading_payload(form):
    return {
        "is_pv_graded": "yes" if form.cleaned_data["is_pv_graded"] else "no",
    }


def get_pv_grading_good_payload(form):
    payload = form.cleaned_data.copy()
    payload["date_of_issue"] = payload["date_of_issue"].isoformat()
    return payload


class ServiceError(Exception):
    def __init__(self, status_code, response, log_message, user_message):
        super().__init__()
        self.status_code = status_code
        self.response = response
        self.log_message = log_message
        self.user_message = user_message


class AddGoodFirearm(LoginRequiredMixin, BaseSessionWizardView):
    form_list = [
        (AddGoodFirearmSteps.CATEGORY, FirearmCategoryForm),
        (AddGoodFirearmSteps.NAME, FirearmNameForm),
        (AddGoodFirearmSteps.PRODUCT_CONTROL_LIST_ENTRY, FirearmProductControlListEntryForm),
        (AddGoodFirearmSteps.PV_GRADING, FirearmPvGradingForm),
        (AddGoodFirearmSteps.PV_GRADING_DETAILS, FirearmPvGradingDetailsForm),
        (AddGoodFirearmSteps.CALIBRE, FirearmCalibreForm),
        (AddGoodFirearmSteps.IS_REPLICA, FirearmReplicaForm),
        (AddGoodFirearmSteps.IS_RFD_CERTIFICATE_VALID, FirearmRFDValidityForm),
        (AddGoodFirearmSteps.IS_REGISTERED_FIREARMS_DEALER, FirearmRegisteredFirearmsDealerForm),
        (AddGoodFirearmSteps.ATTACH_RFD_CERTIFICATE, FirearmAttachRFDCertificate),
        (AddGoodFirearmSteps.PRODUCT_DOCUMENT_AVAILABILITY, FirearmDocumentAvailability),
        (AddGoodFirearmSteps.PRODUCT_DOCUMENT_SENSITIVITY, FirearmDocumentSensitivityForm),
        (AddGoodFirearmSteps.PRODUCT_DOCUMENT_UPLOAD, FirearmDocumentUploadForm),
    ]

    condition_dict = {
        AddGoodFirearmSteps.PV_GRADING_DETAILS: is_pv_graded,
        AddGoodFirearmSteps.IS_RFD_CERTIFICATE_VALID: has_rfd_certificate,
        AddGoodFirearmSteps.IS_REGISTERED_FIREARMS_DEALER: (
            C(has_rfd_certificate) & C(has_user_marked_rfd_certificate_invalid)
        )
        | ~C(has_rfd_certificate),
        AddGoodFirearmSteps.ATTACH_RFD_CERTIFICATE: has_user_marked_as_registered_firearms_dealer,
        AddGoodFirearmSteps.PRODUCT_DOCUMENT_SENSITIVITY: is_product_document_available,
        AddGoodFirearmSteps.PRODUCT_DOCUMENT_UPLOAD: C(is_product_document_available) & ~C(is_document_sensitive),
    }
    good_payload_dict = {
        AddGoodFirearmSteps.NAME: get_cleaned_data,
        AddGoodFirearmSteps.PRODUCT_CONTROL_LIST_ENTRY: get_cleaned_data,
        AddGoodFirearmSteps.PV_GRADING: get_pv_grading_payload,
        AddGoodFirearmSteps.PV_GRADING_DETAILS: get_pv_grading_good_payload,
        AddGoodFirearmSteps.PRODUCT_DOCUMENT_AVAILABILITY: get_cleaned_data,
        AddGoodFirearmSteps.PRODUCT_DOCUMENT_SENSITIVITY: get_cleaned_data,
    }
    firearm_payload_dict = {
        AddGoodFirearmSteps.CATEGORY: get_cleaned_data,
        AddGoodFirearmSteps.CALIBRE: get_cleaned_data,
        AddGoodFirearmSteps.IS_REPLICA: get_cleaned_data,
        AddGoodFirearmSteps.IS_REGISTERED_FIREARMS_DEALER: get_cleaned_data,
    }

    def dispatch(self, request, *args, **kwargs):
        if not settings.FEATURE_FLAG_PRODUCT_2_0:
            raise Http404

        try:
            self.application = get_application(self.request, self.kwargs["pk"])
        except requests.exceptions.HTTPError:
            raise Http404

        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, form, **kwargs):
        ctx = super().get_context_data(form, **kwargs)

        ctx["hide_step_count"] = True
        ctx["back_link_url"] = reverse(
            "applications:new_good",
            kwargs={
                "pk": self.kwargs["pk"],
            },
        )
        ctx["title"] = form.Layout.TITLE

        return ctx

    def get_form_kwargs(self, step=None):
        kwargs = super().get_form_kwargs(step)

        if step == AddGoodFirearmSteps.PRODUCT_CONTROL_LIST_ENTRY:
            kwargs["request"] = self.request

        if step == AddGoodFirearmSteps.PV_GRADING_DETAILS:
            kwargs["request"] = self.request

        if step == AddGoodFirearmSteps.IS_RFD_CERTIFICATE_VALID:
            kwargs["rfd_certificate"] = get_rfd_certificate(self.application)

        return kwargs

    def get_payload(self, form_dict):
        good_payload = {}
        for step_name, payload_func in self.good_payload_dict.items():
            form = form_dict.get(step_name)
            if form:
                good_payload.update(payload_func(form))

        firearm_payload = {}
        for step_name, payload_func in self.firearm_payload_dict.items():
            form = form_dict.get(step_name)
            if form:
                firearm_payload.update(payload_func(form))

        good_payload["firearm_details"] = firearm_payload

        return good_payload

    def has_rfd_certificate_data(self):
        return bool(self.get_cleaned_data_for_step(AddGoodFirearmSteps.ATTACH_RFD_CERTIFICATE))

    def get_rfd_certificate_payload(self):
        rfd_certificate_cleaned_data = self.get_cleaned_data_for_step(AddGoodFirearmSteps.ATTACH_RFD_CERTIFICATE)
        cert_file = rfd_certificate_cleaned_data["file"]
        expiry_date = rfd_certificate_cleaned_data["expiry_date"]
        reference_code = rfd_certificate_cleaned_data["reference_code"]

        rfd_certificate_payload = {
            **get_document_data(cert_file),
            "document_on_organisation": {
                "expiry_date": expiry_date.isoformat(),
                "reference_code": reference_code,
                "document_type": "rfd-certificate",
            },
        }
        return rfd_certificate_payload

    def has_product_documentation(self):
        return self.condition_dict[AddGoodFirearmSteps.PRODUCT_DOCUMENT_UPLOAD](self)

    def get_product_document_payload(self):
        data = self.get_cleaned_data_for_step(AddGoodFirearmSteps.PRODUCT_DOCUMENT_UPLOAD)
        document = data["product_document"]
        payload = {
            **get_document_data(document),
            "description": data["description"],
        }
        return payload

    def get_success_url(self, pk, good_pk):
        return reverse(
            "applications:product_summary",
            kwargs={"pk": pk, "good_pk": good_pk},
        )

    def post_firearm(self, form_dict):
        payload = self.get_payload(form_dict)
        api_resp_data, status_code = post_firearm(
            self.request,
            payload,
        )
        if status_code != HTTPStatus.CREATED:
            raise ServiceError(
                status_code,
                api_resp_data,
                "Error creating firearm - response was: %s - %s",
                "Unexpected error adding firearm",
            )

        application_pk = str(self.kwargs["pk"])
        good_pk = api_resp_data["good"]["id"]

        return application_pk, good_pk

    def post_rfd_certificate(self, application_pk):
        rfd_certificate_payload = self.get_rfd_certificate_payload()
        api_resp_data, status_code = post_additional_document(
            request=self.request,
            pk=application_pk,
            json=rfd_certificate_payload,
        )
        if status_code != HTTPStatus.CREATED:
            raise ServiceError(
                status_code,
                api_resp_data,
                "Error rfd certificate when creating firearm - response was: %s - %s",
                "Unexpected error adding firearm",
            )

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
                "Error product document when creating firearm - response was: %s - %s",
                "Unexpected error adding document to firearm",
            )

    def handle_service_error(self, service_error):
        logger.error(
            service_error.log_message,
            service_error.status_code,
            service_error.response,
            exc_info=True,
        )
        return error_page(self.request, service_error.user_message)

    def done(self, form_list, form_dict, **kwargs):
        try:
            application_pk, good_pk = self.post_firearm(form_dict)

            if self.has_rfd_certificate_data():
                self.post_rfd_certificate(application_pk)

            if self.has_product_documentation():
                self.post_product_documentation(good_pk)
        except ServiceError as e:
            return self.handle_service_error(e)

        return redirect(self.get_success_url(application_pk, good_pk))


class FirearmProductSummary(LoginRequiredMixin, TemplateView):
    template_name = "applications/goods/firearms/product-summary.html"

    @cached_property
    def application_id(self):
        return str(self.kwargs["pk"])

    @cached_property
    def good_id(self):
        return str(self.kwargs["good_pk"])

    @cached_property
    def good(self):
        return get_good(self.request, self.good_id, full_detail=True)[0]

    def dispatch(self, request, *args, **kwargs):
        if not settings.FEATURE_FLAG_PRODUCT_2_0:
            raise Http404

        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        documents = get_good_documents(self.request, self.good_id)
        application = get_application(self.request, self.application_id)
        is_user_rfd = has_valid_rfd_certificate(application)

        return {
            **context,
            "is_user_rfd": is_user_rfd,
            "application_id": self.application_id,
            "good": self.good,
            "documents": documents,
        }


class FirearmEditView(LoginRequiredMixin, FormView):
    template_name = "core/form.html"

    @cached_property
    def application_id(self):
        return str(self.kwargs["pk"])

    @cached_property
    def good_id(self):
        return str(self.kwargs["good_pk"])

    @property
    def good(self):
        return get_good(self.request, self.good_id, full_detail=True)[0]

    def form_valid(self, form):
        edit_firearm(self.request, self.good_id, {"firearm_details": form.cleaned_data})
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("applications:product_summary", kwargs=self.kwargs)


class FirearmEditProductType(FirearmEditView):
    form_class = GroupTwoProductTypeForm

    def get_initial(self):
        return {"type": self.good["firearm_details"]["type"]["key"]}
