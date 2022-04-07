import datetime
import logging
import requests
from datetime import date

from deepmerge import always_merger
from http import HTTPStatus
from functools import wraps

from django.conf import settings
from django.http import Http404
from django.shortcuts import redirect
from django.urls import reverse
from django.utils.functional import cached_property
from django.views.generic import TemplateView, FormView

from core.auth.views import LoginRequiredMixin

from exporter.applications.services import get_application, post_additional_document, post_application_document
from exporter.core.constants import (
    DocumentType,
    FirearmsActSections,
    FirearmsActDocumentType,
)
from exporter.core.helpers import (
    get_document_data,
    get_organisation_documents,
    get_rfd_certificate,
    has_firearm_act_document as _has_firearm_act_document,
    has_valid_rfd_certificate as has_valid_organisation_rfd_certificate,
    str_to_bool,
)

from exporter.core.wizard.conditionals import C
from exporter.core.wizard.views import BaseSessionWizardView
from exporter.goods.forms.firearms import (
    FirearmAttachFirearmCertificateForm,
    FirearmAttachRFDCertificate,
    FirearmAttachSection5LetterOfAuthorityForm,
    FirearmAttachShotgunCertificateForm,
    FirearmCalibreForm,
    FirearmCategoryForm,
    FirearmDocumentAvailability,
    FirearmDocumentSensitivityForm,
    FirearmDocumentUploadForm,
    FirearmFirearmAct1968Form,
    FirearmNameForm,
    FirearmProductControlListEntryForm,
    FirearmPvGradingForm,
    FirearmPvGradingDetailsForm,
    FirearmRegisteredFirearmsDealerForm,
    FirearmReplicaForm,
    FirearmRFDValidityForm,
    FirearmSection5Form,
)
from exporter.goods.services import (
    post_firearm,
    post_good_documents,
    delete_good_document,
    update_good_document_data,
    get_good,
    get_good_documents,
    edit_firearm,
)
from exporter.organisation.services import delete_document_on_organisation
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
    FIREARM_ACT_1968 = "FIREARM_ACT_1968"
    ATTACH_FIREARM_CERTIFICATE = "ATTACH_FIREARM_CERTIFICATE"
    ATTACH_SHOTGUN_CERTIFICATE = "ATTACH_SHOTGUN_CERTIFICATE"
    ATTACH_SECTION_5_LETTER_OF_AUTHORITY = "ATTACH_SECTION_5_LETTER_OF_AUTHORITY"
    IS_COVERED_BY_SECTION_5 = "IS_COVERED_BY_SECTION_5"


def is_product_document_available(wizard):
    cleaned_data = wizard.get_cleaned_data_for_step(AddGoodFirearmSteps.PRODUCT_DOCUMENT_AVAILABILITY)
    return cleaned_data.get("is_document_available")


def is_document_sensitive(wizard):
    cleaned_data = wizard.get_cleaned_data_for_step(AddGoodFirearmSteps.PRODUCT_DOCUMENT_SENSITIVITY)
    return cleaned_data.get("is_document_sensitive")


def has_organisation_rfd_certificate(wizard):
    return has_valid_organisation_rfd_certificate(wizard.application)


def has_application_rfd_certificate(wizard):
    additional_documents = wizard.application.get("additional_documents")
    if not additional_documents:
        return False

    for additional_document in additional_documents:
        if additional_document.get("document_type") == DocumentType.RFD_CERTIFICATE:
            return True

    return False


def has_firearm_act_document(document_type):
    def check(wizard):
        return _has_firearm_act_document(wizard.application, document_type)

    return check


def is_pv_graded(wizard):
    add_goods_cleaned_data = wizard.get_cleaned_data_for_step(AddGoodFirearmSteps.PV_GRADING)
    return add_goods_cleaned_data.get("is_pv_graded")


def is_rfd_certificate_invalid(wizard):
    is_rfd_certificate_valid_cleaned_data = wizard.get_cleaned_data_for_step(
        AddGoodFirearmSteps.IS_RFD_CERTIFICATE_VALID
    )
    if not is_rfd_certificate_valid_cleaned_data:
        return False

    return not is_rfd_certificate_valid_cleaned_data.get("is_rfd_certificate_valid", False)


def is_registered_firearms_dealer(wizard):
    is_registered_firearms_dealer_cleaned_data = wizard.get_cleaned_data_for_step(
        AddGoodFirearmSteps.IS_REGISTERED_FIREARMS_DEALER
    )
    return is_registered_firearms_dealer_cleaned_data.get("is_registered_firearm_dealer", False)


def should_display_is_registered_firearms_dealer_step(wizard):
    if (
        has_organisation_rfd_certificate(wizard)
        and not has_application_rfd_certificate(wizard)
        and is_rfd_certificate_invalid(wizard)
    ):
        return True

    return not has_organisation_rfd_certificate(wizard)


def is_product_covered_by_firearm_act_section(section):
    def _is_product_covered_by_section(wizard):
        firearm_act_1968_cleaned_data = wizard.get_cleaned_data_for_step(AddGoodFirearmSteps.FIREARM_ACT_1968)
        firearms_act_section = firearm_act_1968_cleaned_data.get("firearms_act_section")
        if firearms_act_section == section:
            return True

        is_covered_by_section_5_cleaned_data = wizard.get_cleaned_data_for_step(
            AddGoodFirearmSteps.IS_COVERED_BY_SECTION_5
        )
        if is_covered_by_section_5_cleaned_data and section == FirearmsActSections.SECTION_5:
            return (
                is_covered_by_section_5_cleaned_data.get("is_covered_by_section_5")
                == FirearmSection5Form.Section5Choices.YES
            )

        return False

    return _is_product_covered_by_section


def get_cleaned_data(form):
    return form.cleaned_data


def firearm_details_payload(f):
    @wraps(f)
    def wrapper(form):
        return {"firearm_details": f(form)}

    return wrapper


@firearm_details_payload
def get_firearm_details_cleaned_data(form):
    return get_cleaned_data(form)


def get_pv_grading_payload(form):
    return {
        "is_pv_graded": "yes" if form.cleaned_data["is_pv_graded"] else "no",
    }


def get_pv_grading_good_payload(form):
    payload = form.cleaned_data.copy()
    payload["date_of_issue"] = payload["date_of_issue"].isoformat()
    return {"pv_grading_details": payload}


@firearm_details_payload
def get_firearm_act_1968_payload(form):
    firearms_act_section = form.cleaned_data["firearms_act_section"]

    if firearms_act_section == FirearmFirearmAct1968Form.SectionChoices.NO:
        return {
            "is_covered_by_firearm_act_section_one_two_or_five": "No",
        }

    if firearms_act_section == FirearmFirearmAct1968Form.SectionChoices.DONT_KNOW:
        not_covered_explanation = form.cleaned_data["not_covered_explanation"]
        return {
            "is_covered_by_firearm_act_section_one_two_or_five": "Unsure",
            "is_covered_by_firearm_act_section_one_two_or_five_explanation": not_covered_explanation,
        }

    return {
        "is_covered_by_firearm_act_section_one_two_or_five": "Yes",
        "firearms_act_section": firearms_act_section,
    }


@firearm_details_payload
def get_firearm_section_5_payload(form):
    is_covered_by_section_5 = form.cleaned_data["is_covered_by_section_5"]

    if is_covered_by_section_5 == FirearmSection5Form.Section5Choices.NO:
        return {
            "is_covered_by_firearm_act_section_one_two_or_five": "No",
        }

    if is_covered_by_section_5 == FirearmSection5Form.Section5Choices.DONT_KNOW:
        not_covered_explanation = form.cleaned_data["not_covered_explanation"]
        return {
            "is_covered_by_firearm_act_section_one_two_or_five": "Unsure",
            "is_covered_by_firearm_act_section_one_two_or_five_explanation": not_covered_explanation,
        }

    return {
        "is_covered_by_firearm_act_section_one_two_or_five": "Yes",
        "firearms_act_section": "firearms_act_section5",
    }


@firearm_details_payload
def get_attach_firearm_act_certificate_payload(form):
    firearm_certificate_data = form.cleaned_data

    if firearm_certificate_data["section_certificate_missing"]:
        return {
            "section_certificate_missing": True,
            "section_certificate_missing_reason": firearm_certificate_data["section_certificate_missing_reason"],
        }

    return {
        "section_certificate_missing": False,
        "section_certificate_number": firearm_certificate_data["section_certificate_number"],
        "section_certificate_date_of_expiry": firearm_certificate_data[
            "section_certificate_date_of_expiry"
        ].isoformat(),
    }


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
        (AddGoodFirearmSteps.FIREARM_ACT_1968, FirearmFirearmAct1968Form),
        (AddGoodFirearmSteps.ATTACH_RFD_CERTIFICATE, FirearmAttachRFDCertificate),
        (AddGoodFirearmSteps.IS_COVERED_BY_SECTION_5, FirearmSection5Form),
        (AddGoodFirearmSteps.ATTACH_FIREARM_CERTIFICATE, FirearmAttachFirearmCertificateForm),
        (AddGoodFirearmSteps.ATTACH_SHOTGUN_CERTIFICATE, FirearmAttachShotgunCertificateForm),
        (AddGoodFirearmSteps.ATTACH_SECTION_5_LETTER_OF_AUTHORITY, FirearmAttachSection5LetterOfAuthorityForm),
        (AddGoodFirearmSteps.PRODUCT_DOCUMENT_AVAILABILITY, FirearmDocumentAvailability),
        (AddGoodFirearmSteps.PRODUCT_DOCUMENT_SENSITIVITY, FirearmDocumentSensitivityForm),
        (AddGoodFirearmSteps.PRODUCT_DOCUMENT_UPLOAD, FirearmDocumentUploadForm),
    ]
    condition_dict = {
        AddGoodFirearmSteps.PV_GRADING_DETAILS: is_pv_graded,
        AddGoodFirearmSteps.IS_RFD_CERTIFICATE_VALID: C(has_organisation_rfd_certificate)
        & ~C(has_application_rfd_certificate),
        AddGoodFirearmSteps.IS_REGISTERED_FIREARMS_DEALER: should_display_is_registered_firearms_dealer_step,
        AddGoodFirearmSteps.IS_COVERED_BY_SECTION_5: (
            C(has_organisation_rfd_certificate) & ~C(is_rfd_certificate_invalid)
        )
        | C(is_registered_firearms_dealer),
        AddGoodFirearmSteps.FIREARM_ACT_1968: C(should_display_is_registered_firearms_dealer_step)
        & ~C(is_registered_firearms_dealer),
        AddGoodFirearmSteps.ATTACH_FIREARM_CERTIFICATE: C(
            is_product_covered_by_firearm_act_section(FirearmsActSections.SECTION_1)
        )
        & ~C(has_firearm_act_document(FirearmsActDocumentType.SECTION_1)),
        AddGoodFirearmSteps.ATTACH_SHOTGUN_CERTIFICATE: C(
            is_product_covered_by_firearm_act_section(FirearmsActSections.SECTION_2)
        )
        & ~C(has_firearm_act_document(FirearmsActDocumentType.SECTION_2)),
        AddGoodFirearmSteps.ATTACH_SECTION_5_LETTER_OF_AUTHORITY: C(
            is_product_covered_by_firearm_act_section(FirearmsActSections.SECTION_5)
        )
        & ~C(has_firearm_act_document(FirearmsActDocumentType.SECTION_5)),
        AddGoodFirearmSteps.ATTACH_RFD_CERTIFICATE: is_registered_firearms_dealer,
        AddGoodFirearmSteps.PRODUCT_DOCUMENT_SENSITIVITY: is_product_document_available,
        AddGoodFirearmSteps.PRODUCT_DOCUMENT_UPLOAD: C(is_product_document_available) & ~C(is_document_sensitive),
    }
    payload_dict = {
        AddGoodFirearmSteps.NAME: get_cleaned_data,
        AddGoodFirearmSteps.PRODUCT_CONTROL_LIST_ENTRY: get_cleaned_data,
        AddGoodFirearmSteps.PV_GRADING: get_pv_grading_payload,
        AddGoodFirearmSteps.PV_GRADING_DETAILS: get_pv_grading_good_payload,
        AddGoodFirearmSteps.PRODUCT_DOCUMENT_AVAILABILITY: get_cleaned_data,
        AddGoodFirearmSteps.PRODUCT_DOCUMENT_SENSITIVITY: get_cleaned_data,
        AddGoodFirearmSteps.CATEGORY: get_firearm_details_cleaned_data,
        AddGoodFirearmSteps.CALIBRE: get_firearm_details_cleaned_data,
        AddGoodFirearmSteps.IS_REPLICA: get_firearm_details_cleaned_data,
        AddGoodFirearmSteps.IS_RFD_CERTIFICATE_VALID: get_firearm_details_cleaned_data,
        AddGoodFirearmSteps.IS_REGISTERED_FIREARMS_DEALER: get_firearm_details_cleaned_data,
        AddGoodFirearmSteps.FIREARM_ACT_1968: get_firearm_act_1968_payload,
        AddGoodFirearmSteps.IS_COVERED_BY_SECTION_5: get_firearm_section_5_payload,
        AddGoodFirearmSteps.ATTACH_FIREARM_CERTIFICATE: get_attach_firearm_act_certificate_payload,
        AddGoodFirearmSteps.ATTACH_SHOTGUN_CERTIFICATE: get_attach_firearm_act_certificate_payload,
        AddGoodFirearmSteps.ATTACH_SECTION_5_LETTER_OF_AUTHORITY: get_attach_firearm_act_certificate_payload,
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

    def has_skipped_firearms_attach_step(self, form_dict, firearm_details, section_value, attach_step_name):
        firearms_act_section = firearm_details["firearms_act_section"]
        return firearms_act_section == section_value and attach_step_name not in form_dict

    def get_payload(self, form_dict):
        payload = {}
        for step_name, payload_func in self.payload_dict.items():
            form = form_dict.get(step_name)
            if form:
                always_merger.merge(payload, payload_func(form))

        firearm_details = payload["firearm_details"]
        if firearm_details.get("is_covered_by_firearm_act_section_one_two_or_five") == "Yes":
            for section_value, attach_step_name, document_type in (
                (
                    FirearmsActSections.SECTION_1,
                    AddGoodFirearmSteps.ATTACH_FIREARM_CERTIFICATE,
                    FirearmsActDocumentType.SECTION_1,
                ),
                (
                    FirearmsActSections.SECTION_2,
                    AddGoodFirearmSteps.ATTACH_SHOTGUN_CERTIFICATE,
                    FirearmsActDocumentType.SECTION_2,
                ),
                (
                    FirearmsActSections.SECTION_5,
                    AddGoodFirearmSteps.ATTACH_SECTION_5_LETTER_OF_AUTHORITY,
                    FirearmsActDocumentType.SECTION_5,
                ),
            ):
                if self.has_skipped_firearms_attach_step(form_dict, firearm_details, section_value, attach_step_name):
                    certificate = get_organisation_documents(self.application)[document_type]
                    firearm_details.update(
                        {
                            "section_certificate_missing": False,
                            "section_certificate_number": certificate["reference_code"],
                            "section_certificate_date_of_expiry": datetime.datetime.strptime(
                                certificate["expiry_date"], "%d %B %Y"
                            )
                            .date()
                            .isoformat(),
                        }
                    )
                    break

        return payload

    def has_organisation_rfd_certificate_data(self):
        return bool(self.get_cleaned_data_for_step(AddGoodFirearmSteps.ATTACH_RFD_CERTIFICATE))

    def get_rfd_certificate_payload(self):
        rfd_certificate_cleaned_data = self.get_cleaned_data_for_step(AddGoodFirearmSteps.ATTACH_RFD_CERTIFICATE)
        cert_file = rfd_certificate_cleaned_data["file"]
        expiry_date = rfd_certificate_cleaned_data["expiry_date"]
        reference_code = rfd_certificate_cleaned_data["reference_code"]

        rfd_certificate_payload = {
            **get_document_data(cert_file),
            "description": "Registered firearm dealer certificate",
            "document_type": DocumentType.RFD_CERTIFICATE,
            "document_on_organisation": {
                "expiry_date": expiry_date.isoformat(),
                "reference_code": reference_code,
                "document_type": DocumentType.RFD_CERTIFICATE,
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

    def has_existing_valid_organisation_rfd_certificate(self, application):
        if not has_valid_organisation_rfd_certificate(application):
            return False

        is_rfd_certificate_valid_cleaned_data = self.get_cleaned_data_for_step(
            AddGoodFirearmSteps.IS_RFD_CERTIFICATE_VALID
        )
        return is_rfd_certificate_valid_cleaned_data.get("is_rfd_certificate_valid", False)

    def is_existing_organisation_rfd_certificate_invalid(self, application):
        if not has_valid_organisation_rfd_certificate(application):
            return False

        is_rfd_certificate_valid_cleaned_data = self.get_cleaned_data_for_step(
            AddGoodFirearmSteps.IS_RFD_CERTIFICATE_VALID
        )
        return is_rfd_certificate_valid_cleaned_data.get("is_rfd_certificate_valid") is False

    def delete_existing_organisation_rfd_certificate(self, application):
        organisation_rfd_certificate_data = get_rfd_certificate(self.application)
        status_code = delete_document_on_organisation(
            self.request,
            organisation_id=organisation_rfd_certificate_data["organisation"],
            document_id=organisation_rfd_certificate_data["id"],
        )
        if status_code != HTTPStatus.NO_CONTENT:
            raise ServiceError(
                status_code,
                {},
                "Error deleting existing rfd certificate to application - response was: %s - %s",
                "Unexpected error adding firearm",
            )

    def attach_rfd_certificate_to_application(self, application):
        organisation_rfd_certificate_data = get_rfd_certificate(self.application)
        document = organisation_rfd_certificate_data["document"]
        api_resp_data, status_code = post_additional_document(
            self.request,
            pk=application["id"],
            json={
                "name": document["name"],
                "s3_key": document["s3_key"],
                "safe": document["safe"],
                "size": document["size"],
                "document_type": DocumentType.RFD_CERTIFICATE,
                "description": "Registered firearm dealer certificate",
            },
        )
        if status_code != HTTPStatus.CREATED:
            raise ServiceError(
                status_code,
                api_resp_data,
                "Error attaching existing rfd certificate to application - response was: %s - %s",
                "Unexpected error adding firearm",
            )

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

    def has_firearm_act_certificate(self, step_name):
        attach_firearm_certificate = self.get_cleaned_data_for_step(step_name)
        return bool(attach_firearm_certificate.get("file"))

    def get_firearm_act_certificate_payload(self, step_name, document_type):
        data = self.get_cleaned_data_for_step(step_name)
        certificate = data["file"]
        payload = {
            **get_document_data(certificate),
            "document_on_organisation": {
                "expiry_date": data["section_certificate_date_of_expiry"].isoformat(),
                "reference_code": data["section_certificate_number"],
                "document_type": document_type,
            },
        }
        return payload

    def post_firearm_act_certificate(self, step_name, document_type, application_pk, good_pk):
        firearm_certificate_payload = self.get_firearm_act_certificate_payload(step_name, document_type)
        api_resp_data, status_code = post_application_document(
            request=self.request,
            pk=application_pk,
            good_pk=good_pk,
            data=firearm_certificate_payload,
        )
        if status_code != HTTPStatus.CREATED:
            raise ServiceError(
                status_code,
                api_resp_data,
                "Error adding firearm certificate when creating firearm - response was: %s - %s",
                "Unexpected error adding firearm certificate",
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

            if self.has_existing_valid_organisation_rfd_certificate(self.application):
                self.attach_rfd_certificate_to_application(self.application)
            else:
                if self.is_existing_organisation_rfd_certificate_invalid(self.application):
                    self.delete_existing_organisation_rfd_certificate(self.application)
                if self.has_organisation_rfd_certificate_data():
                    self.post_rfd_certificate(application_pk)

            if self.has_firearm_act_certificate(AddGoodFirearmSteps.ATTACH_FIREARM_CERTIFICATE):
                self.post_firearm_act_certificate(
                    AddGoodFirearmSteps.ATTACH_FIREARM_CERTIFICATE,
                    FirearmsActDocumentType.SECTION_1,
                    application_pk,
                    good_pk,
                )

            if self.has_firearm_act_certificate(AddGoodFirearmSteps.ATTACH_SHOTGUN_CERTIFICATE):
                self.post_firearm_act_certificate(
                    AddGoodFirearmSteps.ATTACH_SHOTGUN_CERTIFICATE,
                    FirearmsActDocumentType.SECTION_2,
                    application_pk,
                    good_pk,
                )

            if self.has_firearm_act_certificate(AddGoodFirearmSteps.ATTACH_SECTION_5_LETTER_OF_AUTHORITY):
                self.post_firearm_act_certificate(
                    AddGoodFirearmSteps.ATTACH_SECTION_5_LETTER_OF_AUTHORITY,
                    FirearmsActDocumentType.SECTION_5,
                    application_pk,
                    good_pk,
                )

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
        is_user_rfd = has_valid_organisation_rfd_certificate(application)
        organisation_documents = {k.replace("-", "_"): v for k, v in get_organisation_documents(application).items()}

        return {
            **context,
            "is_user_rfd": is_user_rfd,
            "application_id": self.application_id,
            "good": self.good,
            "documents": documents,
            "organisation_documents": organisation_documents,
        }


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


class FirearmEditPvGrading(LoginRequiredMixin, BaseSessionWizardView):

    form_list = [
        (AddGoodFirearmSteps.PV_GRADING, FirearmPvGradingForm),
        (AddGoodFirearmSteps.PV_GRADING_DETAILS, FirearmPvGradingDetailsForm),
    ]

    condition_dict = {
        AddGoodFirearmSteps.PV_GRADING_DETAILS: is_pv_graded,
    }

    payload_dict = {
        AddGoodFirearmSteps.PV_GRADING: get_pv_grading_payload,
        AddGoodFirearmSteps.PV_GRADING_DETAILS: get_pv_grading_good_payload,
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
        payload = {}
        for step_name, payload_func in self.payload_dict.items():
            form = form_dict.get(step_name)
            if form:
                always_merger.merge(payload, payload_func(form))

        return payload

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


class FirearmEditProductDocumentView(BaseGoodEditView):
    form_class = FirearmDocumentUploadForm

    @cached_property
    def product_document(self):
        is_document_available = self.good["is_document_available"]
        is_document_sensitive = self.good["is_document_sensitive"]
        if not is_document_available or is_document_sensitive:
            return None

        if not self.good["documents"]:
            return None

        # when creating new product we can only add one document but we save it as
        # a list because from the product detail page user can add multiple documents
        return self.good["documents"][0]

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        return {**kwargs, "good_id": self.good_id, "document": self.product_document}

    def get_initial(self):
        return {"description": self.product_document["description"] if self.product_document else ""}

    def form_valid(self, form):
        product_document = form.cleaned_data.pop("product_document", None)
        description = form.cleaned_data.pop("description", "")
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
            api_resp_data, status_code = delete_good_document(self.request, self.good_id, self.product_document["id"])
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
                    "Error deleting the product document - response was: %s - %s",
                    "Unexpected error deleting product document",
                )

        return redirect(self.get_success_url())
