import logging

from deepmerge import always_merger
from http import HTTPStatus

from django.shortcuts import redirect
from django.urls import reverse

from core.auth.views import LoginRequiredMixin
from core.constants import (
    FirearmsActDocumentType,
    FirearmsActSections,
    OrganisationDocumentType,
)
from core.decorators import expect_status
from core.helpers import get_document_data

from exporter.applications.services import (
    post_additional_document,
    post_firearm_good_on_application,
)
from exporter.applications.views.goods.common.actions import ProductDocumentAction
from exporter.core.helpers import (
    get_rfd_certificate,
    has_valid_rfd_certificate as has_valid_organisation_rfd_certificate,
)
from core.wizard.conditionals import C
from core.wizard.views import BaseSessionWizardView
from exporter.goods.forms.common import (
    ProductControlListEntryForm,
    ProductDescriptionForm,
    ProductDocumentAvailabilityForm,
    ProductDocumentSensitivityForm,
    ProductDocumentUploadForm,
    ProductNameForm,
    ProductOnwardAlteredProcessedForm,
    ProductOnwardExportedForm,
    ProductOnwardIncorporatedForm,
    ProductPVGradingDetailsForm,
    ProductPVGradingForm,
    ProductQuantityAndValueForm,
)
from exporter.goods.forms.firearms import (
    FirearmAttachFirearmCertificateForm,
    FirearmAttachRFDCertificate,
    FirearmAttachSection5LetterOfAuthorityForm,
    FirearmAttachShotgunCertificateForm,
    FirearmCalibreForm,
    FirearmCategoryForm,
    FirearmDeactivationDetailsForm,
    FirearmFirearmAct1968Form,
    FirearmIsDeactivatedForm,
    FirearmRegisteredFirearmsDealerForm,
    FirearmReplicaForm,
    FirearmRFDValidityForm,
    FirearmSection5Form,
    FirearmMadeBefore1938Form,
    FirearmYearOfManufactureForm,
    FirearmSerialIdentificationMarkingsForm,
    FirearmSerialNumbersForm,
)
from exporter.goods.services import post_firearm
from exporter.organisation.services import delete_document_on_organisation

from .actions import (
    GoodOnApplicationFirearmActCertificateAction,
    OrganisationFirearmActCertificateAction,
)
from .conditionals import (
    has_application_rfd_certificate,
    has_organisation_firearm_act_document,
    has_organisation_rfd_certificate,
    is_certificate_required,
    is_deactivated,
    is_product_category_made_before_1938,
    is_product_covered_by_firearm_act_section,
    is_product_made_before_1938,
    is_registered_firearms_dealer,
    is_rfd_certificate_invalid,
    is_serial_numbers_available,
    should_display_is_registered_firearms_dealer_step,
)
from exporter.applications.views.goods.common.conditionals import (
    is_document_sensitive,
    is_pv_graded,
    is_product_document_available,
    is_onward_exported,
)
from exporter.applications.views.goods.common.mixins import ApplicationMixin, GoodMixin

from .constants import AddGoodFirearmSteps, AddGoodFirearmToApplicationSteps
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
    ApplicationMixin,
    BaseSessionWizardView,
):
    form_list = [
        (AddGoodFirearmSteps.CATEGORY, FirearmCategoryForm),
        (AddGoodFirearmSteps.NAME, ProductNameForm),
        (AddGoodFirearmSteps.PRODUCT_CONTROL_LIST_ENTRY, ProductControlListEntryForm),
        (AddGoodFirearmSteps.PV_GRADING, ProductPVGradingForm),
        (AddGoodFirearmSteps.PV_GRADING_DETAILS, ProductPVGradingDetailsForm),
        (AddGoodFirearmSteps.CALIBRE, FirearmCalibreForm),
        (AddGoodFirearmSteps.IS_REPLICA, FirearmReplicaForm),
        (AddGoodFirearmSteps.IS_RFD_CERTIFICATE_VALID, FirearmRFDValidityForm),
        (AddGoodFirearmSteps.IS_REGISTERED_FIREARMS_DEALER, FirearmRegisteredFirearmsDealerForm),
        (AddGoodFirearmSteps.FIREARM_ACT_1968, FirearmFirearmAct1968Form),
        (AddGoodFirearmSteps.ATTACH_RFD_CERTIFICATE, FirearmAttachRFDCertificate),
        (AddGoodFirearmSteps.IS_COVERED_BY_SECTION_5, FirearmSection5Form),
        (AddGoodFirearmSteps.ATTACH_SECTION_5_LETTER_OF_AUTHORITY, FirearmAttachSection5LetterOfAuthorityForm),
        (AddGoodFirearmSteps.PRODUCT_DOCUMENT_AVAILABILITY, ProductDocumentAvailabilityForm),
        (AddGoodFirearmSteps.PRODUCT_DESCRIPTION, ProductDescriptionForm),
        (AddGoodFirearmSteps.PRODUCT_DOCUMENT_SENSITIVITY, ProductDocumentSensitivityForm),
        (AddGoodFirearmSteps.PRODUCT_DOCUMENT_UPLOAD, ProductDocumentUploadForm),
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
        AddGoodFirearmSteps.PRODUCT_DESCRIPTION: ~C(is_product_document_available),
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
            "document_type": OrganisationDocumentType.RFD_CERTIFICATE,
            "document_on_organisation": {
                "expiry_date": expiry_date.isoformat(),
                "reference_code": reference_code,
                "document_type": OrganisationDocumentType.RFD_CERTIFICATE,
            },
        }
        return rfd_certificate_payload

    def get_success_url(self):
        return reverse(
            "applications:firearm_product_summary",
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
                "document_type": OrganisationDocumentType.RFD_CERTIFICATE,
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

    def done(self, form_list, form_dict, **kwargs):
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

        ProductDocumentAction(self).run()

        return redirect(self.get_success_url())


class AddGoodFirearmToApplication(
    LoginRequiredMixin,
    ApplicationMixin,
    GoodMixin,
    BaseSessionWizardView,
):
    form_list = [
        (AddGoodFirearmToApplicationSteps.ATTACH_FIREARM_CERTIFICATE, FirearmAttachFirearmCertificateForm),
        (AddGoodFirearmToApplicationSteps.ATTACH_SHOTGUN_CERTIFICATE, FirearmAttachShotgunCertificateForm),
        (AddGoodFirearmToApplicationSteps.MADE_BEFORE_1938, FirearmMadeBefore1938Form),
        (AddGoodFirearmToApplicationSteps.YEAR_OF_MANUFACTURE, FirearmYearOfManufactureForm),
        (AddGoodFirearmToApplicationSteps.ONWARD_EXPORTED, ProductOnwardExportedForm),
        (AddGoodFirearmToApplicationSteps.ONWARD_ALTERED_PROCESSED, ProductOnwardAlteredProcessedForm),
        (AddGoodFirearmToApplicationSteps.ONWARD_INCORPORATED, ProductOnwardIncorporatedForm),
        (AddGoodFirearmToApplicationSteps.IS_DEACTIVATED, FirearmIsDeactivatedForm),
        (AddGoodFirearmToApplicationSteps.IS_DEACTIVATED_TO_STANDARD, FirearmDeactivationDetailsForm),
        (AddGoodFirearmToApplicationSteps.QUANTITY_AND_VALUE, ProductQuantityAndValueForm),
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
        AddGoodFirearmToApplicationSteps.MADE_BEFORE_1938: ~C(is_product_category_made_before_1938),
        AddGoodFirearmToApplicationSteps.YEAR_OF_MANUFACTURE: C(is_product_category_made_before_1938)
        | C(is_product_made_before_1938),
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
            "applications:firearm_product_summary",
            kwargs={
                "pk": self.kwargs["pk"],
                "good_pk": self.good["id"],
            },
        )
        ctx["title"] = form.Layout.TITLE

        return ctx

    def done(self, form_list, form_dict, **kwargs):
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

        self.good_on_application = good_on_application

        return redirect(self.get_success_url())
