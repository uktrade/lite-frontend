import logging

from deepmerge import always_merger
from http import HTTPStatus

from django.conf import settings
from django.shortcuts import redirect
from django.urls import reverse

from core.auth.views import LoginRequiredMixin
from lite_forms.generators import error_page

from exporter.applications.services import (
    post_additional_document,
    post_firearm_good_on_application,
)
from exporter.core.constants import (
    DocumentType,
    FirearmsActDocumentType,
    FirearmsActSections,
)
from exporter.core.helpers import (
    get_document_data,
    get_rfd_certificate,
    has_valid_rfd_certificate as has_valid_organisation_rfd_certificate,
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
    FirearmDeactivationDetailsForm,
    FirearmDocumentAvailability,
    FirearmDocumentSensitivityForm,
    FirearmDocumentUploadForm,
    FirearmFirearmAct1968Form,
    FirearmIsDeactivatedForm,
    FirearmNameForm,
    FirearmProductControlListEntryForm,
    FirearmPvGradingForm,
    FirearmPvGradingDetailsForm,
    FirearmRegisteredFirearmsDealerForm,
    FirearmReplicaForm,
    FirearmRFDValidityForm,
    FirearmSection5Form,
    FirearmMadeBefore1938Form,
    FirearmYearOfManufactureForm,
    FirearmOnwardExportedForm,
    FirearmOnwardAlteredProcessedForm,
    FirearmOnwardIncorporatedForm,
    FirearmQuantityAndValueForm,
    FirearmSerialIdentificationMarkingsForm,
    FirearmSerialNumbersForm,
)
from exporter.goods.services import (
    post_firearm,
    post_good_documents,
)
from exporter.organisation.services import delete_document_on_organisation

from .actions import GoodOnApplicationFirearmActCertificateAction, OrganisationFirearmActCertificateAction
from .conditionals import (
    has_application_rfd_certificate,
    has_organisation_firearm_act_document,
    has_organisation_rfd_certificate,
    is_certificate_required,
    is_deactivated,
    is_document_sensitive,
    is_onward_exported,
    is_product_covered_by_firearm_act_section,
    is_product_document_available,
    is_product_made_before_1938,
    is_pv_graded,
    is_registered_firearms_dealer,
    is_rfd_certificate_invalid,
    is_serial_numbers_available,
    should_display_is_registered_firearms_dealer_step,
)
from .constants import AddGoodFirearmSteps, AddGoodFirearmToApplicationSteps
from .decorators import expect_status
from .exceptions import ServiceError
from .mixins import ApplicationMixin, GoodMixin, Product2FlagMixin
from .payloads import (
    AddGoodFirearmPayloadBuilder,
    AddGoodFirearmToApplicationPayloadBuilder,
    FirearmsActPayloadBuilder,
)


logger = logging.getLogger(__name__)


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


class AddGoodFirearm(
    LoginRequiredMixin,
    Product2FlagMixin,
    ApplicationMixin,
    BaseSessionWizardView,
):
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
        AddGoodFirearmSteps.ATTACH_SECTION_5_LETTER_OF_AUTHORITY: C(
            is_product_covered_by_firearm_act_section(FirearmsActSections.SECTION_5)
        )
        & ~C(has_organisation_firearm_act_document(FirearmsActDocumentType.SECTION_5)),
        AddGoodFirearmSteps.ATTACH_RFD_CERTIFICATE: is_registered_firearms_dealer,
        AddGoodFirearmSteps.PRODUCT_DOCUMENT_SENSITIVITY: is_product_document_available,
        AddGoodFirearmSteps.PRODUCT_DOCUMENT_UPLOAD: C(is_product_document_available) & ~C(is_document_sensitive),
    }

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
        good_payload = AddGoodFirearmPayloadBuilder().build(form_dict)
        firearms_act_payload = FirearmsActPayloadBuilder(
            self.application,
            good_payload["firearm_details"],
        ).build(form_dict)

        payload = always_merger.merge(good_payload, firearms_act_payload)

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

    def get_success_url(self):
        return reverse(
            "applications:product_summary",
            kwargs={"pk": self.application["id"], "good_pk": self.good["id"]},
        )

    @expect_status(
        HTTPStatus.CREATED,
        "Error creating firearm",
        "Unexpected error adding firearm",
    )
    def post_firearm(self, form_dict):
        payload = self.get_payload(form_dict)
        return post_firearm(
            self.request,
            payload,
        )

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

    @expect_status(
        HTTPStatus.NO_CONTENT,
        "Error deleting existing rfd certificate to application",
        "Unexpected error adding firearm",
    )
    def delete_existing_organisation_rfd_certificate(self, application):
        organisation_rfd_certificate_data = get_rfd_certificate(application)
        status_code = delete_document_on_organisation(
            self.request,
            organisation_id=organisation_rfd_certificate_data["organisation"],
            document_id=organisation_rfd_certificate_data["id"],
        )
        return {}, status_code

    @expect_status(
        HTTPStatus.CREATED,
        "Error attaching existing rfd certificate to application",
        "Unexpected error adding firearm",
    )
    def attach_rfd_certificate_to_application(self, application):
        organisation_rfd_certificate_data = get_rfd_certificate(application)
        document = organisation_rfd_certificate_data["document"]
        return post_additional_document(
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

    @expect_status(
        HTTPStatus.CREATED,
        "Error with rfd certificate when creating firearm",
        "Unexpected error adding firearm",
    )
    def post_rfd_certificate(self, application):
        rfd_certificate_payload = self.get_rfd_certificate_payload()
        return post_additional_document(
            request=self.request,
            pk=application["id"],
            json=rfd_certificate_payload,
        )

    @expect_status(
        HTTPStatus.CREATED,
        "Error with product document when creating firearm",
        "Unexpected error adding firearm",
    )
    def post_product_documentation(self, good):
        document_payload = self.get_product_document_payload()
        return post_good_documents(
            request=self.request,
            pk=good["id"],
            json=document_payload,
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
            good, _ = self.post_firearm(form_dict)
            self.good = good["good"]

            if self.has_existing_valid_organisation_rfd_certificate(self.application):
                self.attach_rfd_certificate_to_application(self.application)
            else:
                if self.is_existing_organisation_rfd_certificate_invalid(self.application):
                    self.delete_existing_organisation_rfd_certificate(self.application)
                if self.has_organisation_rfd_certificate_data():
                    self.post_rfd_certificate(self.application)

            OrganisationFirearmActCertificateAction(
                self.request,
                FirearmsActDocumentType.SECTION_5,
                self.application,
                self.good,
                self.get_cleaned_data_for_step(AddGoodFirearmSteps.ATTACH_SECTION_5_LETTER_OF_AUTHORITY),
            ).run()

            if self.has_product_documentation():
                self.post_product_documentation(self.good)
        except ServiceError as e:
            return self.handle_service_error(e)

        return redirect(self.get_success_url())


class AddGoodFirearmToApplication(
    LoginRequiredMixin,
    Product2FlagMixin,
    ApplicationMixin,
    GoodMixin,
    BaseSessionWizardView,
):
    form_list = [
        (AddGoodFirearmToApplicationSteps.ATTACH_FIREARM_CERTIFICATE, FirearmAttachFirearmCertificateForm),
        (AddGoodFirearmToApplicationSteps.ATTACH_SHOTGUN_CERTIFICATE, FirearmAttachShotgunCertificateForm),
        (AddGoodFirearmToApplicationSteps.MADE_BEFORE_1938, FirearmMadeBefore1938Form),
        (AddGoodFirearmToApplicationSteps.YEAR_OF_MANUFACTURE, FirearmYearOfManufactureForm),
        (AddGoodFirearmToApplicationSteps.ONWARD_EXPORTED, FirearmOnwardExportedForm),
        (AddGoodFirearmToApplicationSteps.ONWARD_ALTERED_PROCESSED, FirearmOnwardAlteredProcessedForm),
        (AddGoodFirearmToApplicationSteps.ONWARD_INCORPORATED, FirearmOnwardIncorporatedForm),
        (AddGoodFirearmToApplicationSteps.IS_DEACTIVATED, FirearmIsDeactivatedForm),
        (AddGoodFirearmToApplicationSteps.IS_DEACTIVATED_TO_STANDARD, FirearmDeactivationDetailsForm),
        (AddGoodFirearmToApplicationSteps.QUANTITY_AND_VALUE, FirearmQuantityAndValueForm),
        (AddGoodFirearmToApplicationSteps.SERIAL_IDENTIFICATION_MARKING, FirearmSerialIdentificationMarkingsForm),
        (AddGoodFirearmToApplicationSteps.SERIAL_NUMBERS, FirearmSerialNumbersForm),
    ]

    condition_dict = {
        AddGoodFirearmToApplicationSteps.ATTACH_FIREARM_CERTIFICATE: is_certificate_required(
            FirearmsActSections.SECTION_1,
        ),
        AddGoodFirearmToApplicationSteps.ATTACH_SHOTGUN_CERTIFICATE: is_certificate_required(
            FirearmsActSections.SECTION_2,
        ),
        AddGoodFirearmToApplicationSteps.YEAR_OF_MANUFACTURE: is_product_made_before_1938,
        AddGoodFirearmToApplicationSteps.ONWARD_ALTERED_PROCESSED: is_onward_exported,
        AddGoodFirearmToApplicationSteps.ONWARD_INCORPORATED: is_onward_exported,
        AddGoodFirearmToApplicationSteps.IS_DEACTIVATED_TO_STANDARD: is_deactivated,
        AddGoodFirearmToApplicationSteps.SERIAL_NUMBERS: is_serial_numbers_available,
    }

    def get_form_kwargs(self, step=None):
        kwargs = super().get_form_kwargs(step)
        if step == AddGoodFirearmToApplicationSteps.SERIAL_NUMBERS:
            quantity_step_data = self.get_cleaned_data_for_step(AddGoodFirearmToApplicationSteps.QUANTITY_AND_VALUE)
            kwargs["number_of_items"] = quantity_step_data["number_of_items"]

        return kwargs

    def get_success_url(self):
        return reverse(
            "applications:product_on_application_summary",
            kwargs={
                "pk": self.kwargs["pk"],
                "good_on_application_pk": self.good_on_application["id"],
            },
        )

    def get_payload(self, form_dict):
        good_on_application_payload = AddGoodFirearmToApplicationPayloadBuilder().build(form_dict)
        return good_on_application_payload

    @expect_status(
        HTTPStatus.CREATED,
        "Error adding firearm to application",
        "Unexpected error adding firearm to application",
    )
    def post_firearm_to_application(self, form_dict):
        payload = self.get_payload(form_dict)
        return post_firearm_good_on_application(
            self.request,
            self.application["id"],
            self.good["id"],
            payload,
        )

    def get_context_data(self, form, **kwargs):
        ctx = super().get_context_data(form, **kwargs)

        ctx["back_link_url"] = reverse(
            "applications:product_summary",
            kwargs={
                "pk": self.kwargs["pk"],
                "good_pk": self.good["id"],
            },
        )
        ctx["title"] = form.Layout.TITLE

        return ctx

    def done(self, form_list, form_dict, **kwargs):
        try:
            good_on_application, _ = self.post_firearm_to_application(form_dict)
            good_on_application = good_on_application["good"]

            GoodOnApplicationFirearmActCertificateAction(
                self.request,
                FirearmsActDocumentType.SECTION_1,
                self.application,
                self.good,
                good_on_application,
                self.get_cleaned_data_for_step(AddGoodFirearmToApplicationSteps.ATTACH_FIREARM_CERTIFICATE),
            ).run()

            GoodOnApplicationFirearmActCertificateAction(
                self.request,
                FirearmsActDocumentType.SECTION_2,
                self.application,
                self.good,
                good_on_application,
                self.get_cleaned_data_for_step(AddGoodFirearmToApplicationSteps.ATTACH_SHOTGUN_CERTIFICATE),
            ).run()
        except ServiceError as e:
            return self.handle_service_error(e)

        self.good_on_application = good_on_application

        return redirect(self.get_success_url())
