import logging

from datetime import date, datetime
from http import HTTPStatus

from django.conf import settings
from django.http import Http404
from django.shortcuts import redirect
from django.urls import reverse
from django.utils.functional import cached_property
from django.views.generic import FormView

from core.auth.views import LoginRequiredMixin
from lite_forms.generators import error_page

from exporter.applications.services import post_additional_document
from exporter.core.constants import DocumentType, FirearmsActDocumentType
from exporter.core.forms import CurrentFile
from exporter.core.helpers import (
    convert_api_date_string_to_date,
    get_document_data,
    get_firearm_act_document,
    get_rfd_certificate,
    has_firearm_act_document,
    has_valid_rfd_certificate as has_valid_organisation_rfd_certificate,
    str_to_bool,
)
from exporter.core.wizard.conditionals import C
from exporter.core.wizard.views import BaseSessionWizardView
from exporter.goods.services import (
    delete_good_document,
    edit_firearm,
    post_good_documents,
    update_good_document_data,
)
from exporter.goods.forms.firearms import (
    FirearmAttachRFDCertificate,
    FirearmAttachSection5LetterOfAuthorityForm,
    FirearmCalibreForm,
    FirearmCategoryForm,
    FirearmDocumentAvailability,
    FirearmDocumentSensitivityForm,
    FirearmDocumentUploadForm,
    FirearmNameForm,
    FirearmProductControlListEntryForm,
    FirearmPvGradingDetailsForm,
    FirearmPvGradingForm,
    FirearmRegisteredFirearmsDealerForm,
    FirearmReplicaForm,
    FirearmSection5Form,
)
from exporter.organisation.services import update_document_on_organisation

from .conditionals import (
    is_document_sensitive,
    is_product_document_available,
    is_pv_graded,
)
from .actions import CreateOrUpdateFirearmActCertificateAction
from .constants import AddGoodFirearmSteps
from .decorators import expect_status
from .exceptions import ServiceError
from .mixins import ApplicationMixin, GoodMixin, Product2FlagMixin
from .payloads import (
    FirearmEditProductDocumentAvailabilityPayloadBuilder,
    FirearmEditProductDocumentSensitivityPayloadBuilder,
    FirearmEditPvGradingPayloadBuilder,
    FirearmEditRegisteredFirearmsDealerPayloadBuilder,
    get_cleaned_data,
    get_firearm_details_cleaned_data,
    get_pv_grading_good_payload,
)


logger = logging.getLogger(__name__)


class BaseEditView(
    LoginRequiredMixin,
    Product2FlagMixin,
    ApplicationMixin,
    GoodMixin,
    FormView,
):
    template_name = "core/form.html"

    def get_success_url(self):
        return reverse("applications:product_summary", kwargs=self.kwargs)

    def get_edit_payload(self, form):
        raise NotImplementedError(f"Implement `get_edit_payload` for {self.__class__.__name__}")

    def form_valid(self, form):
        edit_firearm(self.request, self.good["id"], self.get_edit_payload(form))
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


class BaseEditWizardView(
    LoginRequiredMixin,
    Product2FlagMixin,
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
        return error_page(self.request, service_error.user_message)

    def get_context_data(self, form, **kwargs):
        ctx = super().get_context_data(form, **kwargs)

        ctx["back_link_url"] = reverse("applications:product_summary", kwargs=self.kwargs)
        ctx["title"] = form.Layout.TITLE
        return ctx

    def get_success_url(self):
        return reverse("applications:product_summary", kwargs=self.kwargs)

    def get_payload(self, form_dict):
        raise NotImplementedError(f"Implement `get_payload` on f{self.__class__.__name__}")

    @expect_status(HTTPStatus.OK, "Error updating firearm", "Unexpected error updating firearm")
    def edit_firearm(self, good_pk, form_dict):
        payload = self.get_payload(form_dict)
        return edit_firearm(self.request, good_pk, payload)


class FirearmEditPvGrading(BaseEditWizardView):
    form_list = [
        (AddGoodFirearmSteps.PV_GRADING, FirearmPvGradingForm),
        (AddGoodFirearmSteps.PV_GRADING_DETAILS, FirearmPvGradingDetailsForm),
    ]
    condition_dict = {
        AddGoodFirearmSteps.PV_GRADING_DETAILS: is_pv_graded,
    }

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

    def done(self, form_list, form_dict, **kwargs):
        try:
            self.edit_firearm(self.good["id"], form_dict)
        except ServiceError as e:
            return self.handle_service_error(e)

        return redirect(self.get_success_url())


class FirearmEditPVGradingDetails(BaseGoodEditView):
    form_class = FirearmPvGradingDetailsForm

    def get_initial(self):
        pv_grading_details = self.good["pv_grading_details"]
        return {
            "prefix": pv_grading_details.get("prefix"),
            "grading": pv_grading_details["grading"].get("key"),
            "suffix": pv_grading_details.get("suffix"),
            "issuing_authority": pv_grading_details.get("issuing_authority"),
            "reference": pv_grading_details.get("reference"),
            "date_of_issue": date.fromisoformat(pv_grading_details["date_of_issue"])
            if pv_grading_details["date_of_issue"]
            else None,
        }

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        return {**kwargs, "request": self.request}

    def get_edit_payload(self, form):
        grading_details = get_pv_grading_good_payload(form)
        return {"is_pv_graded": self.good["is_pv_graded"].get("key"), **grading_details}


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
        return {**kwargs, "good_id": self.good["id"], "document": self.product_document}

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
                pk=self.good["id"],
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
                    self.request, self.good["id"], self.product_document["id"]
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
                self.request, self.good["id"], self.product_document["id"], payload
            )
            if status_code != HTTPStatus.OK:
                raise ServiceError(
                    status_code,
                    api_resp_data,
                    "Error updating the product document description - response was: %s - %s",
                    "Unexpected error updating product document description",
                )

        return redirect(self.get_success_url())


class BaseEditProductDocumentView(BaseEditWizardView):
    @cached_property
    def product_document(self):
        return get_product_document(self.good)

    def get_form_kwargs(self, step=None):
        kwargs = super().get_form_kwargs(step)

        if step == AddGoodFirearmSteps.PRODUCT_DOCUMENT_UPLOAD:
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


class FirearmEditProductDocumentSensitivity(BaseEditProductDocumentView):
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
            self.edit_firearm(self.good["id"], form_dict)

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

        except ServiceError as e:
            return self.handle_service_error(e)

        return redirect(self.get_success_url())


class FirearmEditProductDocumentAvailability(BaseEditProductDocumentView):
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
            self.edit_firearm(self.good["id"], form_dict)

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


class FirearmEditRegisteredFirearmsDealer(BaseEditWizardView):
    form_list = [
        (AddGoodFirearmSteps.IS_REGISTERED_FIREARMS_DEALER, FirearmRegisteredFirearmsDealerForm),
        (AddGoodFirearmSteps.ATTACH_RFD_CERTIFICATE, FirearmAttachRFDCertificate),
        (AddGoodFirearmSteps.IS_COVERED_BY_SECTION_5, FirearmSection5Form),
        (AddGoodFirearmSteps.ATTACH_SECTION_5_LETTER_OF_AUTHORITY, FirearmAttachSection5LetterOfAuthorityForm),
    ]

    def get_context_data(self, form, **kwargs):
        ctx = super().get_context_data(form, **kwargs)

        ctx["back_link_url"] = reverse(
            "applications:product_summary",
            kwargs={"pk": self.kwargs["pk"], "good_pk": self.kwargs["good_pk"]},
        )
        ctx["title"] = form.Layout.TITLE

        return ctx

    def get_document_url(self, document):
        return reverse(
            "organisation:document",
            kwargs={
                "pk": document["id"],
            },
        )

    def get_attach_rfd_certificate_initial_data(self):
        rfd_certificate = get_rfd_certificate(self.application)
        if not rfd_certificate:
            return {}

        return {
            "expiry_date": convert_api_date_string_to_date(rfd_certificate["expiry_date"]),
            "reference_code": rfd_certificate["reference_code"],
            "file": CurrentFile(
                rfd_certificate["document"]["name"],
                self.get_document_url(rfd_certificate),
                rfd_certificate["document"]["safe"],
            ),
        }

    def get_is_covered_by_section_5_initial_data(self):
        firearm_details = self.good["firearm_details"]
        is_covered_by_firearm_act_section_one_two_or_five = firearm_details.get(
            "is_covered_by_firearm_act_section_one_two_or_five"
        )

        if is_covered_by_firearm_act_section_one_two_or_five is None:
            return {}

        if (
            is_covered_by_firearm_act_section_one_two_or_five == "Yes"
            and firearm_details["firearms_act_section"] == "firearms_act_section5"
        ):
            return {"is_covered_by_section_5": FirearmSection5Form.Section5Choices.YES}

        if is_covered_by_firearm_act_section_one_two_or_five == "No":
            return {"is_covered_by_section_5": FirearmSection5Form.Section5Choices.NO}

        if is_covered_by_firearm_act_section_one_two_or_five == "Unsure":
            is_covered_by_firearm_act_section_one_two_or_five_explanation = firearm_details[
                "is_covered_by_firearm_act_section_one_two_or_five_explanation"
            ]
            return {
                "is_covered_by_section_5": FirearmSection5Form.Section5Choices.DONT_KNOW,
                "not_covered_explanation": is_covered_by_firearm_act_section_one_two_or_five_explanation,
            }

    def get_attach_section_5_letter_of_authority_initial_data(self):
        if not has_firearm_act_document(self.application, FirearmsActDocumentType.SECTION_5):
            return {}

        section_5_document = get_firearm_act_document(self.application, FirearmsActDocumentType.SECTION_5)
        firearm_details = self.good["firearm_details"]
        return {
            "section_certificate_missing": firearm_details["section_certificate_missing"],
            "section_certificate_number": firearm_details["section_certificate_number"],
            "section_certificate_date_of_expiry": datetime.fromisoformat(
                firearm_details["section_certificate_date_of_expiry"]
            ).date(),
            "section_certificate_missing_reason": firearm_details["section_certificate_missing_reason"],
            "file": CurrentFile(
                section_5_document["document"]["name"],
                self.get_document_url(section_5_document),
                section_5_document["document"]["safe"],
            ),
        }

    def get_form_initial(self, step):
        initial = super().get_form_initial(step)

        if step == AddGoodFirearmSteps.IS_REGISTERED_FIREARMS_DEALER:
            initial["is_registered_firearm_dealer"] = has_valid_organisation_rfd_certificate(self.application)

        if step == AddGoodFirearmSteps.ATTACH_RFD_CERTIFICATE:
            initial.update(self.get_attach_rfd_certificate_initial_data())

        if step == AddGoodFirearmSteps.IS_COVERED_BY_SECTION_5:
            initial.update(self.get_is_covered_by_section_5_initial_data())

        if step == AddGoodFirearmSteps.ATTACH_SECTION_5_LETTER_OF_AUTHORITY:
            initial.update(self.get_attach_section_5_letter_of_authority_initial_data())

        return initial

    def has_organisation_rfd_certificate_data(self):
        return bool(self.get_cleaned_data_for_step(AddGoodFirearmSteps.ATTACH_RFD_CERTIFICATE))

    def is_new_rfd_certificate(self):
        attach_rfd_certificate_cleaned_data = self.get_cleaned_data_for_step(AddGoodFirearmSteps.ATTACH_RFD_CERTIFICATE)
        file = attach_rfd_certificate_cleaned_data["file"]
        return not isinstance(file, CurrentFile)

    @expect_status(
        HTTPStatus.CREATED,
        "Error rfd certificate when creating firearm",
        "Unexpected error updating firearm",
    )
    def post_rfd_certificate(self, application):
        rfd_certificate_payload = self.get_rfd_certificate_payload()
        return post_additional_document(
            request=self.request,
            pk=application["id"],
            json=rfd_certificate_payload,
        )

    def get_organisation_document_payload(self):
        rfd_certificate_cleaned_data = self.get_cleaned_data_for_step(AddGoodFirearmSteps.ATTACH_RFD_CERTIFICATE)
        expiry_date = rfd_certificate_cleaned_data["expiry_date"]
        reference_code = rfd_certificate_cleaned_data["reference_code"]

        rfd_certificate_payload = {
            "expiry_date": expiry_date.isoformat(),
            "reference_code": reference_code,
            "document_type": DocumentType.RFD_CERTIFICATE,
        }
        return rfd_certificate_payload

    @expect_status(
        HTTPStatus.OK,
        "Error updating rfd certificate when creating firearm",
        "Unexpected error updating firearm",
    )
    def update_rfd_certificate(self, application):
        rfd_document = get_rfd_certificate(application)
        rfd_certificate_payload = self.get_organisation_document_payload()
        return update_document_on_organisation(
            request=self.request,
            organisation_id=rfd_document["organisation"],
            document_id=rfd_document["id"],
            data=rfd_certificate_payload,
        )

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

    def get_payload(self, form_dict):
        return FirearmEditRegisteredFirearmsDealerPayloadBuilder().build(form_dict)

    def done(self, form_list, form_dict, **kwargs):
        try:
            self.edit_firearm(self.good["id"], form_dict)

            if self.has_organisation_rfd_certificate_data():
                if self.is_new_rfd_certificate():
                    self.post_rfd_certificate(self.application)
                else:
                    self.update_rfd_certificate(self.application)

            CreateOrUpdateFirearmActCertificateAction(
                AddGoodFirearmSteps.ATTACH_SECTION_5_LETTER_OF_AUTHORITY,
                FirearmsActDocumentType.SECTION_5,
                self,
            ).run()
        except ServiceError as e:
            return self.handle_service_error(e)

        return redirect(self.get_success_url())
