import logging

from datetime import date

from deepmerge import always_merger
from http import HTTPStatus

from django.conf import settings
from django.http import Http404
from django.shortcuts import redirect
from django.urls import reverse
from django.utils.functional import cached_property
from django.views.generic import FormView

from core.auth.views import LoginRequiredMixin
from lite_forms.generators import error_page

from exporter.applications.services import (
    edit_firearm_good_on_application,
    get_application_documents,
)
from exporter.core.constants import (
    FirearmsActDocumentType,
    FirearmsActSections,
)
from exporter.core.forms import CurrentFile
from exporter.core.helpers import (
    convert_api_date_string_to_date,
    get_document_data,
    get_rfd_certificate,
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
    FirearmAttachFirearmCertificateForm,
    FirearmAttachRFDCertificate,
    FirearmAttachSection5LetterOfAuthorityForm,
    FirearmCalibreForm,
    FirearmCategoryForm,
    FirearmDeactivationDetailsForm,
    FirearmDocumentAvailability,
    FirearmDocumentSensitivityForm,
    FirearmDocumentUploadForm,
    FirearmFirearmAct1968Form,
    FirearmIsDeactivatedForm,
    FirearmMadeBefore1938Form,
    FirearmNameForm,
    FirearmOnwardAlteredProcessedForm,
    FirearmOnwardExportedForm,
    FirearmOnwardIncorporatedForm,
    FirearmProductControlListEntryForm,
    FirearmPvGradingDetailsForm,
    FirearmPvGradingForm,
    FirearmQuantityAndValueForm,
    FirearmRegisteredFirearmsDealerForm,
    FirearmReplicaForm,
    FirearmSection5Form,
    FirearmSerialIdentificationMarkingsForm,
    FirearmSerialNumbersForm,
    FirearmYearOfManufactureForm,
)

from .actions import (
    GoodOnApplicationFirearmActCertificateAction,
    OrganisationFirearmActCertificateAction,
    IsRfdAction,
    RfdCertificateAction,
)
from .conditionals import (
    has_organisation_firearm_act_document,
    is_deactivated,
    is_document_sensitive,
    is_onward_exported,
    is_product_covered_by_firearm_act_section,
    is_product_document_available,
    is_product_made_before_1938,
    is_pv_graded,
    is_registered_firearms_dealer,
    is_serial_numbers_available,
)
from .constants import AddGoodFirearmSteps, AddGoodFirearmToApplicationSteps
from .decorators import expect_status
from .exceptions import ServiceError
from .helpers import get_organisation_document_url
from .initial import (
    get_attach_good_on_application_certificate_initial_data,
    get_attach_organisation_certificate_initial_data,
    get_firearm_act_1968_initial_data,
    get_is_covered_by_section_5_initial_data,
    get_is_deactivated_to_standard_initial_data,
    get_onward_altered_processed_initial_data,
    get_onward_incorporated_initial_data,
    get_serial_numbers_initial_data,
    get_year_of_manufacture_initial_data,
)
from .mixins import (
    ApplicationMixin,
    GoodMixin,
    GoodOnApplicationMixin,
    Product2FlagMixin,
)
from .payloads import (
    FirearmsActPayloadBuilder,
    FirearmEditFirearmsAct1968PayloadBuilder,
    FirearmEditProductDocumentAvailabilityPayloadBuilder,
    FirearmEditProductDocumentSensitivityPayloadBuilder,
    FirearmEditPvGradingPayloadBuilder,
    FirearmEditRegisteredFirearmsDealerPayloadBuilder,
    FirearmEditSection5FirearmsAct1968PayloadBuilder,
    FirearmProductOnApplicationSummaryEditIsDeactivatedPayloadBuilder,
    FirearmProductOnApplicationSummaryEditMadeBefore1938PayloadBuilder,
    FirearmProductOnApplicationSummaryEditOnwardExportedPayloadBuilder,
    FirearmProductOnApplicationSummaryEditSerialIdentificationMarkingsPayloadBuilder,
    get_attach_firearm_act_certificate_payload,
    get_cleaned_data,
    get_deactivation_details_payload,
    get_firearm_details_cleaned_data,
    get_onward_incorporated_payload,
    get_pv_grading_good_payload,
    get_quantity_and_value_payload,
    get_serial_numbers_payload,
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

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)

        ctx["back_link_url"] = reverse("applications:product_summary", kwargs=self.kwargs)

        return ctx


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
        if settings.DEBUG:
            raise service_error
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
        (AddGoodFirearmSteps.FIREARM_ACT_1968, FirearmFirearmAct1968Form),
        (AddGoodFirearmSteps.ATTACH_RFD_CERTIFICATE, FirearmAttachRFDCertificate),
        (AddGoodFirearmSteps.IS_COVERED_BY_SECTION_5, FirearmSection5Form),
        (AddGoodFirearmSteps.ATTACH_SECTION_5_LETTER_OF_AUTHORITY, FirearmAttachSection5LetterOfAuthorityForm),
    ]
    condition_dict = {
        AddGoodFirearmSteps.FIREARM_ACT_1968: ~C(is_registered_firearms_dealer),
        AddGoodFirearmSteps.ATTACH_RFD_CERTIFICATE: is_registered_firearms_dealer,
        AddGoodFirearmSteps.IS_COVERED_BY_SECTION_5: C(is_registered_firearms_dealer),
        AddGoodFirearmSteps.ATTACH_SECTION_5_LETTER_OF_AUTHORITY: C(
            is_product_covered_by_firearm_act_section(FirearmsActSections.SECTION_5)
        )
        & ~C(has_organisation_firearm_act_document(FirearmsActDocumentType.SECTION_5)),
    }

    def get_attach_rfd_certificate_initial_data(self):
        rfd_certificate = get_rfd_certificate(self.application)
        if not rfd_certificate:
            return {}

        return {
            "expiry_date": convert_api_date_string_to_date(rfd_certificate["expiry_date"]),
            "reference_code": rfd_certificate["reference_code"],
            "file": CurrentFile(
                rfd_certificate["document"]["name"],
                get_organisation_document_url(rfd_certificate),
                rfd_certificate["document"]["safe"],
            ),
        }

    def get_form_initial(self, step):
        initial = super().get_form_initial(step)

        if step == AddGoodFirearmSteps.IS_REGISTERED_FIREARMS_DEALER:
            initial["is_registered_firearm_dealer"] = has_valid_organisation_rfd_certificate(self.application)

        if step == AddGoodFirearmSteps.ATTACH_RFD_CERTIFICATE:
            initial.update(self.get_attach_rfd_certificate_initial_data())

        if step == AddGoodFirearmSteps.FIREARM_ACT_1968:
            initial.update(get_firearm_act_1968_initial_data(self.good["firearm_details"]))

        if step == AddGoodFirearmSteps.IS_COVERED_BY_SECTION_5:
            initial.update(get_is_covered_by_section_5_initial_data(self.good["firearm_details"]))

        if step == AddGoodFirearmSteps.ATTACH_SECTION_5_LETTER_OF_AUTHORITY:
            initial.update(
                get_attach_organisation_certificate_initial_data(
                    FirearmsActDocumentType.SECTION_5,
                    self.application,
                    self.good,
                )
            )

        return initial

    def has_skipped_firearms_attach_step(self, form_dict, firearm_details, section_value, attach_step_name):
        firearms_act_section = firearm_details["firearms_act_section"]
        return firearms_act_section == section_value and attach_step_name not in form_dict

    def get_payload(self, form_dict):
        good_payload = FirearmEditRegisteredFirearmsDealerPayloadBuilder().build(form_dict)
        firearms_act_payload = FirearmsActPayloadBuilder(
            self.application,
            good_payload["firearm_details"],
        ).build(form_dict)

        payload = always_merger.merge(good_payload, firearms_act_payload)

        return payload

    def done(self, form_list, form_dict, **kwargs):
        try:
            self.edit_firearm(self.good["id"], form_dict)

            IsRfdAction(
                AddGoodFirearmSteps.IS_REGISTERED_FIREARMS_DEALER,
                self,
            ).run()

            RfdCertificateAction(
                AddGoodFirearmSteps.ATTACH_RFD_CERTIFICATE,
                self,
            ).run()

            OrganisationFirearmActCertificateAction(
                self.request,
                FirearmsActDocumentType.SECTION_5,
                self.application,
                self.good,
                self.get_cleaned_data_for_step(AddGoodFirearmSteps.ATTACH_SECTION_5_LETTER_OF_AUTHORITY),
            ).run()
        except ServiceError as e:
            return self.handle_service_error(e)

        return redirect(self.get_success_url())


class FirearmEditSection5FirearmsAct1968(BaseEditWizardView):
    form_list = [
        (AddGoodFirearmSteps.IS_COVERED_BY_SECTION_5, FirearmSection5Form),
        (AddGoodFirearmSteps.ATTACH_SECTION_5_LETTER_OF_AUTHORITY, FirearmAttachSection5LetterOfAuthorityForm),
    ]
    condition_dict = {
        AddGoodFirearmSteps.ATTACH_SECTION_5_LETTER_OF_AUTHORITY: C(
            is_product_covered_by_firearm_act_section(FirearmsActSections.SECTION_5)
        )
        & ~C(has_organisation_firearm_act_document(FirearmsActDocumentType.SECTION_5)),
    }

    def get_form_initial(self, step):
        initial = super().get_form_initial(step)

        if step == AddGoodFirearmSteps.IS_COVERED_BY_SECTION_5:
            initial.update(get_is_covered_by_section_5_initial_data(self.good["firearm_details"]))

        return initial

    def get_payload(self, form_dict):
        good_payload = payload = FirearmEditSection5FirearmsAct1968PayloadBuilder().build(form_dict)
        firearms_act_payload = FirearmsActPayloadBuilder(
            self.application,
            good_payload["firearm_details"],
        ).build(form_dict)

        payload = always_merger.merge(good_payload, firearms_act_payload)

        return payload

    def done(self, form_list, form_dict, **kwargs):
        try:
            self.edit_firearm(self.good["id"], form_dict)

            OrganisationFirearmActCertificateAction(
                self.request,
                FirearmsActDocumentType.SECTION_5,
                self.application,
                self.good,
                self.get_cleaned_data_for_step(AddGoodFirearmSteps.ATTACH_SECTION_5_LETTER_OF_AUTHORITY),
            ).run()
        except ServiceError as e:
            return self.handle_service_error(e)

        return redirect(self.get_success_url())


class FirearmEditLetterOfAuthority(BaseFirearmEditView):
    form_class = FirearmAttachSection5LetterOfAuthorityForm
    document_type = FirearmsActDocumentType.SECTION_5

    def get_initial(self):
        return get_attach_organisation_certificate_initial_data(
            self.document_type,
            self.application,
            self.good,
        )

    def get_edit_payload(self, form):
        return get_attach_firearm_act_certificate_payload(form)

    def form_valid(self, form):
        response = super().form_valid(form)

        OrganisationFirearmActCertificateAction(
            self.request,
            self.document_type,
            self.application,
            self.good,
            form.cleaned_data,
        ).run()

        return response


class FirearmEditFirearmsAct1968(BaseEditWizardView):
    form_list = [
        (AddGoodFirearmSteps.FIREARM_ACT_1968, FirearmFirearmAct1968Form),
        (AddGoodFirearmSteps.ATTACH_SECTION_5_LETTER_OF_AUTHORITY, FirearmAttachSection5LetterOfAuthorityForm),
    ]
    condition_dict = {
        AddGoodFirearmSteps.ATTACH_SECTION_5_LETTER_OF_AUTHORITY: C(
            is_product_covered_by_firearm_act_section(FirearmsActSections.SECTION_5)
        )
        & ~C(has_organisation_firearm_act_document(FirearmsActDocumentType.SECTION_5)),
    }

    def get_form_initial(self, step):
        initial = super().get_form_initial(step)

        if step == AddGoodFirearmSteps.FIREARM_ACT_1968:
            initial.update(get_firearm_act_1968_initial_data(self.good["firearm_details"]))

        if step == AddGoodFirearmSteps.ATTACH_SECTION_5_LETTER_OF_AUTHORITY:
            initial.update(
                get_attach_organisation_certificate_initial_data(
                    FirearmsActDocumentType.SECTION_5,
                    self.application,
                    self.good,
                )
            )

        return initial

    def get_payload(self, form_dict):
        good_payload = FirearmEditFirearmsAct1968PayloadBuilder().build(form_dict)
        firearms_act_payload = FirearmsActPayloadBuilder(
            self.application,
            good_payload["firearm_details"],
        ).build(form_dict)

        payload = always_merger.merge(good_payload, firearms_act_payload)

        return payload

    def done(self, form_list, form_dict, **kwargs):
        try:
            self.edit_firearm(self.good["id"], form_dict)

            OrganisationFirearmActCertificateAction(
                self.request,
                FirearmsActDocumentType.SECTION_5,
                self.application,
                self.good,
                self.get_cleaned_data_for_step(AddGoodFirearmSteps.ATTACH_SECTION_5_LETTER_OF_AUTHORITY),
            ).run()
        except ServiceError as e:
            return self.handle_service_error(e)

        return redirect(self.get_success_url())


class SummaryTypeMixin:
    SUMMARY_TYPES = [
        "product-on-application-summary",
        "attach-product-on-application-summary",
    ]

    def dispatch(self, request, *args, **kwargs):
        if kwargs["summary_type"] not in self.SUMMARY_TYPES:
            raise Http404("Not a valid summary type")

        return super().dispatch(request, *args, **kwargs)

    def get_summary_url(self):
        summary_url_name = self.kwargs["summary_type"].replace("-", "_")

        return reverse(
            f"applications:{summary_url_name}",
            kwargs={
                "pk": self.application["id"],
                "good_on_application_pk": self.good_on_application["id"],
            },
        )

    def get_success_url(self):
        return self.get_summary_url()

    def get_context_data(self, *args, **kwargs):
        ctx = super().get_context_data(*args, **kwargs)

        ctx["back_link_url"] = self.get_summary_url()

        return ctx


class BaseGoodOnApplicationEditView(
    LoginRequiredMixin,
    Product2FlagMixin,
    SummaryTypeMixin,
    ApplicationMixin,
    GoodOnApplicationMixin,
    FormView,
):
    template_name = "core/form.html"

    @expect_status(
        HTTPStatus.OK,
        "Error updating firearm",
        "Unexpected error updating firearm",
    )
    def edit_firearm_good_on_application(self, request, good_on_application_id, payload):
        return edit_firearm_good_on_application(
            request,
            good_on_application_id,
            payload,
        )

    def perform_actions(self, form):
        self.edit_firearm_good_on_application(
            self.request,
            self.good_on_application["id"],
            self.get_edit_payload(form),
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

    def form_valid(self, form):
        try:
            self.perform_actions(form)
        except ServiceError as e:
            return self.handle_service_error(e)

        return super().form_valid(form)

    def get_edit_payload(self, form):
        return get_firearm_details_cleaned_data(form)


class BaseFirearmActCertificateGoodOnApplicationEditView(BaseGoodOnApplicationEditView):
    def get_initial(self):
        application_documents, _ = get_application_documents(
            self.request,
            self.application["id"],
            self.good["id"],
        )
        application_documents = application_documents["documents"]

        good_on_application_documents = {
            document["document_type"]: document
            for document in application_documents
            if document["good_on_application"] == self.good_on_application["id"]
        }

        return get_attach_good_on_application_certificate_initial_data(
            good_on_application_documents[self.document_type],
            self.application,
            self.good,
            self.good_on_application,
        )

    def get_edit_payload(self, form):
        return get_attach_firearm_act_certificate_payload(form)

    def perform_actions(self, form):
        super().perform_actions(form)

        GoodOnApplicationFirearmActCertificateAction(
            self.request,
            self.document_type,
            self.application,
            self.good,
            self.good_on_application,
            form.cleaned_data,
        ).run()


class FirearmProductOnApplicationSummaryEditFirearmCertificate(BaseFirearmActCertificateGoodOnApplicationEditView):
    form_class = FirearmAttachFirearmCertificateForm
    document_type = FirearmsActDocumentType.SECTION_1


class FirearmProductOnApplicationSummaryEditShotgunCertificate(BaseFirearmActCertificateGoodOnApplicationEditView):
    form_class = FirearmAttachFirearmCertificateForm
    document_type = FirearmsActDocumentType.SECTION_2


class BaseProductOnApplicationSummaryEditWizardView(
    LoginRequiredMixin,
    Product2FlagMixin,
    SummaryTypeMixin,
    ApplicationMixin,
    GoodOnApplicationMixin,
    BaseSessionWizardView,
):
    @expect_status(
        HTTPStatus.OK,
        "Error updating firearm",
        "Unexpected error updating firearm",
    )
    def edit_firearm_good_on_application(self, request, good_on_application_id, payload):
        return edit_firearm_good_on_application(
            request,
            good_on_application_id,
            payload,
        )

    def done(self, form_list, form_dict, **kwargs):
        try:
            self.edit_firearm_good_on_application(
                self.request,
                self.good_on_application["id"],
                self.get_edit_firearm_good_on_application_payload(form_dict),
            )
        except ServiceError as e:
            return self.handle_service_error(e)

        return redirect(self.get_success_url())


class FirearmProductOnApplicationSummaryEditMadeBefore1938(BaseProductOnApplicationSummaryEditWizardView):
    form_list = [
        (AddGoodFirearmToApplicationSteps.MADE_BEFORE_1938, FirearmMadeBefore1938Form),
        (AddGoodFirearmToApplicationSteps.YEAR_OF_MANUFACTURE, FirearmYearOfManufactureForm),
    ]
    condition_dict = {
        AddGoodFirearmToApplicationSteps.YEAR_OF_MANUFACTURE: is_product_made_before_1938,
    }

    def get_form_initial(self, step):
        initial = super().get_form_initial(step)

        if step == AddGoodFirearmToApplicationSteps.MADE_BEFORE_1938:
            initial["is_made_before_1938"] = self.good_on_application["firearm_details"]["is_made_before_1938"]

        if step == AddGoodFirearmToApplicationSteps.YEAR_OF_MANUFACTURE:
            initial.update(get_year_of_manufacture_initial_data(self.good_on_application["firearm_details"]))

        return initial

    def get_edit_firearm_good_on_application_payload(self, form_dict):
        return FirearmProductOnApplicationSummaryEditMadeBefore1938PayloadBuilder().build(form_dict)


class FirearmProductOnApplicationSummaryEditYearOfManufacture(BaseGoodOnApplicationEditView):
    form_class = FirearmYearOfManufactureForm

    def get_initial(self):
        return get_year_of_manufacture_initial_data(self.good_on_application["firearm_details"])


class FirearmProductOnApplicationSummaryEditOnwardExported(BaseProductOnApplicationSummaryEditWizardView):
    form_list = [
        (AddGoodFirearmToApplicationSteps.ONWARD_EXPORTED, FirearmOnwardExportedForm),
        (AddGoodFirearmToApplicationSteps.ONWARD_ALTERED_PROCESSED, FirearmOnwardAlteredProcessedForm),
        (AddGoodFirearmToApplicationSteps.ONWARD_INCORPORATED, FirearmOnwardIncorporatedForm),
    ]
    condition_dict = {
        AddGoodFirearmToApplicationSteps.ONWARD_ALTERED_PROCESSED: is_onward_exported,
        AddGoodFirearmToApplicationSteps.ONWARD_INCORPORATED: is_onward_exported,
    }

    def get_form_initial(self, step):
        initial = super().get_form_initial(step)

        if step == AddGoodFirearmToApplicationSteps.ONWARD_EXPORTED:
            initial["is_onward_exported"] = self.good_on_application["firearm_details"]["is_onward_exported"]

        if step == AddGoodFirearmToApplicationSteps.ONWARD_ALTERED_PROCESSED:
            initial.update(get_onward_altered_processed_initial_data(self.good_on_application["firearm_details"]))

        if step == AddGoodFirearmToApplicationSteps.ONWARD_INCORPORATED:
            initial.update(get_onward_incorporated_initial_data(self.good_on_application["firearm_details"]))

        return initial

    def get_edit_firearm_good_on_application_payload(self, form_dict):
        return FirearmProductOnApplicationSummaryEditOnwardExportedPayloadBuilder().build(form_dict)


class FirearmProductOnApplicationSummaryEditOnwardAltered(BaseGoodOnApplicationEditView):
    form_class = FirearmOnwardAlteredProcessedForm

    def get_initial(self):
        return get_onward_altered_processed_initial_data(self.good_on_application["firearm_details"])


class FirearmProductOnApplicationSummaryEditOnwardIncorporated(BaseGoodOnApplicationEditView):
    form_class = FirearmOnwardIncorporatedForm

    def get_initial(self):
        return get_onward_incorporated_initial_data(self.good_on_application["firearm_details"])

    def get_edit_payload(self, form):
        return get_onward_incorporated_payload(form)


class FirearmProductOnApplicationSummaryEditIsDeactivated(BaseProductOnApplicationSummaryEditWizardView):
    form_list = [
        (AddGoodFirearmToApplicationSteps.IS_DEACTIVATED, FirearmIsDeactivatedForm),
        (AddGoodFirearmToApplicationSteps.IS_DEACTIVATED_TO_STANDARD, FirearmDeactivationDetailsForm),
    ]
    condition_dict = {
        AddGoodFirearmToApplicationSteps.IS_DEACTIVATED_TO_STANDARD: is_deactivated,
    }

    def get_form_initial(self, step):
        initial = super().get_form_initial(step)

        firearm_details = self.good_on_application["firearm_details"]

        if step == AddGoodFirearmToApplicationSteps.IS_DEACTIVATED:
            initial["is_deactivated"] = firearm_details["is_deactivated"]

        if step == AddGoodFirearmToApplicationSteps.IS_DEACTIVATED_TO_STANDARD:
            initial.update(get_is_deactivated_to_standard_initial_data(firearm_details))

        return initial

    def get_edit_firearm_good_on_application_payload(self, form_dict):
        return FirearmProductOnApplicationSummaryEditIsDeactivatedPayloadBuilder().build(form_dict)


class FirearmProductOnApplicationSummaryEditIsDeactivatedToStandard(BaseGoodOnApplicationEditView):
    form_class = FirearmDeactivationDetailsForm

    def get_initial(self):
        return get_is_deactivated_to_standard_initial_data(self.good_on_application["firearm_details"])

    def get_edit_payload(self, form):
        return get_deactivation_details_payload(form)


class FirearmProductOnApplicationSummaryEditQuantityValue(BaseGoodOnApplicationEditView):
    form_class = FirearmQuantityAndValueForm

    def get_initial(self):
        return {
            "number_of_items": int(self.good_on_application["quantity"]),
            "value": self.good_on_application["value"],
        }

    def get_edit_payload(self, form):
        return get_quantity_and_value_payload(form)


class FirearmProductOnApplicationSummaryEditSerialIdentificationMarkings(BaseProductOnApplicationSummaryEditWizardView):
    form_list = [
        (AddGoodFirearmToApplicationSteps.SERIAL_IDENTIFICATION_MARKING, FirearmSerialIdentificationMarkingsForm),
        (AddGoodFirearmToApplicationSteps.SERIAL_NUMBERS, FirearmSerialNumbersForm),
    ]
    condition_dict = {
        AddGoodFirearmToApplicationSteps.SERIAL_NUMBERS: is_serial_numbers_available,
    }

    def get_form_kwargs(self, step=None):
        kwargs = super().get_form_kwargs(step)
        if step == AddGoodFirearmToApplicationSteps.SERIAL_NUMBERS:
            kwargs["number_of_items"] = int(self.good_on_application["quantity"])
        return kwargs

    def get_form_initial(self, step):
        initial = super().get_form_initial(step)

        firearm_details = self.good_on_application["firearm_details"]

        if step == AddGoodFirearmToApplicationSteps.SERIAL_IDENTIFICATION_MARKING:
            initial.update(
                {
                    "serial_numbers_available": firearm_details["serial_numbers_available"],
                    "no_identification_markings_details": firearm_details["no_identification_markings_details"],
                }
            )

        if step == AddGoodFirearmToApplicationSteps.SERIAL_NUMBERS:
            initial.update(get_serial_numbers_initial_data(firearm_details))

        return initial

    def get_edit_firearm_good_on_application_payload(self, form_dict):
        return FirearmProductOnApplicationSummaryEditSerialIdentificationMarkingsPayloadBuilder().build(form_dict)


class FirearmProductOnApplicationSummaryEditSerialNumbers(BaseGoodOnApplicationEditView):
    form_class = FirearmSerialNumbersForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()

        kwargs["number_of_items"] = int(self.good_on_application["quantity"])

        return kwargs

    def get_initial(self):
        return get_serial_numbers_initial_data(self.good_on_application["firearm_details"])

    def get_edit_payload(self, form):
        return get_serial_numbers_payload(form)
