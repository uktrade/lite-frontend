import logging

from deepmerge import always_merger
from http import HTTPStatus
from urllib.parse import urlencode

from django.conf import settings
from django.shortcuts import redirect
from django.urls import reverse

from lite_forms.generators import error_page

from core.auth.views import LoginRequiredMixin

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
    get_rfd_certificate,
    has_valid_rfd_certificate as has_valid_organisation_rfd_certificate,
)
from exporter.core.wizard.conditionals import C
from exporter.core.wizard.views import BaseSessionWizardView
from exporter.goods.forms.firearms import (
    FirearmAttachFirearmCertificateForm,
    FirearmAttachShotgunCertificateForm,
    FirearmCategoryForm,
    FirearmDeactivationDetailsForm,
    FirearmIsDeactivatedForm,
    FirearmRFDInvalidForm,
    FirearmRFDValidityForm,
    FirearmMadeBefore1938Form,
    FirearmYearOfManufactureForm,
    FirearmOnwardExportedForm,
    FirearmOnwardAlteredProcessedForm,
    FirearmOnwardIncorporatedForm,
    FirearmQuantityAndValueForm,
    FirearmSerialIdentificationMarkingsForm,
    FirearmSerialNumbersForm,
)
from exporter.goods.services import edit_firearm_for_attaching

from .actions import GoodOnApplicationFirearmActCertificateAction
from .conditionals import (
    has_application_rfd_certificate,
    has_firearm_category,
    has_organisation_rfd_certificate,
    is_certificate_required,
    is_deactivated,
    is_firearm_certificate_invalid,
    is_onward_exported,
    is_product_made_before_1938,
    is_serial_numbers_available,
)
from .constants import AttachFirearmToApplicationSteps
from .decorators import expect_status
from .exceptions import ServiceError
from .mixins import ApplicationMixin, GoodMixin, Product2FlagMixin
from .payloads import (
    AttachFirearmToApplicationGoodPayloadBuilder,
    AttachFirearmToApplicationGoodOnApplicationPayloadBuilder,
    FirearmsActPayloadBuilder,
)


logger = logging.getLogger(__name__)


has_user_marked_rfd_as_invalid = (
    C(has_organisation_rfd_certificate) & ~C(has_application_rfd_certificate) & C(is_firearm_certificate_invalid)
)


class AttachFirearmToApplication(
    LoginRequiredMixin,
    Product2FlagMixin,
    ApplicationMixin,
    GoodMixin,
    BaseSessionWizardView,
):
    form_list = [
        (AttachFirearmToApplicationSteps.CATEGORY, FirearmCategoryForm),
        (AttachFirearmToApplicationSteps.IS_RFD_CERTIFICATE_VALID, FirearmRFDValidityForm),
        (AttachFirearmToApplicationSteps.RFD_CERTIFICATE_INVALID, FirearmRFDInvalidForm),
        (AttachFirearmToApplicationSteps.ATTACH_FIREARM_CERTIFICATE, FirearmAttachFirearmCertificateForm),
        (AttachFirearmToApplicationSteps.ATTACH_SHOTGUN_CERTIFICATE, FirearmAttachShotgunCertificateForm),
        (AttachFirearmToApplicationSteps.MADE_BEFORE_1938, FirearmMadeBefore1938Form),
        (AttachFirearmToApplicationSteps.YEAR_OF_MANUFACTURE, FirearmYearOfManufactureForm),
        (AttachFirearmToApplicationSteps.ONWARD_EXPORTED, FirearmOnwardExportedForm),
        (AttachFirearmToApplicationSteps.ONWARD_ALTERED_PROCESSED, FirearmOnwardAlteredProcessedForm),
        (AttachFirearmToApplicationSteps.ONWARD_INCORPORATED, FirearmOnwardIncorporatedForm),
        (AttachFirearmToApplicationSteps.IS_DEACTIVATED, FirearmIsDeactivatedForm),
        (AttachFirearmToApplicationSteps.IS_DEACTIVATED_TO_STANDARD, FirearmDeactivationDetailsForm),
        (AttachFirearmToApplicationSteps.QUANTITY_AND_VALUE, FirearmQuantityAndValueForm),
        (AttachFirearmToApplicationSteps.SERIAL_IDENTIFICATION_MARKING, FirearmSerialIdentificationMarkingsForm),
        (AttachFirearmToApplicationSteps.SERIAL_NUMBERS, FirearmSerialNumbersForm),
    ]
    condition_dict = {
        AttachFirearmToApplicationSteps.CATEGORY: has_firearm_category,
        AttachFirearmToApplicationSteps.IS_RFD_CERTIFICATE_VALID: (
            (
                ~C(
                    is_certificate_required(
                        FirearmsActSections.SECTION_1,
                    )
                )
                & ~C(
                    is_certificate_required(
                        FirearmsActSections.SECTION_2,
                    )
                )
            )
            & C(has_organisation_rfd_certificate)
            & ~C(has_application_rfd_certificate)
        ),
        AttachFirearmToApplicationSteps.RFD_CERTIFICATE_INVALID: has_user_marked_rfd_as_invalid,
        AttachFirearmToApplicationSteps.ATTACH_FIREARM_CERTIFICATE: ~C(has_user_marked_rfd_as_invalid)
        & C(
            is_certificate_required(
                FirearmsActSections.SECTION_1,
            )
        ),
        AttachFirearmToApplicationSteps.ATTACH_SHOTGUN_CERTIFICATE: ~C(has_user_marked_rfd_as_invalid)
        & C(
            is_certificate_required(
                FirearmsActSections.SECTION_2,
            )
        ),
        AttachFirearmToApplicationSteps.MADE_BEFORE_1938: ~C(has_user_marked_rfd_as_invalid),
        AttachFirearmToApplicationSteps.YEAR_OF_MANUFACTURE: ~C(has_user_marked_rfd_as_invalid)
        & C(is_product_made_before_1938),
        AttachFirearmToApplicationSteps.ONWARD_EXPORTED: ~C(has_user_marked_rfd_as_invalid),
        AttachFirearmToApplicationSteps.ONWARD_ALTERED_PROCESSED: ~C(has_user_marked_rfd_as_invalid)
        & C(is_onward_exported),
        AttachFirearmToApplicationSteps.ONWARD_INCORPORATED: ~C(has_user_marked_rfd_as_invalid) & C(is_onward_exported),
        AttachFirearmToApplicationSteps.IS_DEACTIVATED: ~C(has_user_marked_rfd_as_invalid),
        AttachFirearmToApplicationSteps.IS_DEACTIVATED_TO_STANDARD: ~C(has_user_marked_rfd_as_invalid)
        & C(is_deactivated),
        AttachFirearmToApplicationSteps.QUANTITY_AND_VALUE: ~C(has_user_marked_rfd_as_invalid),
        AttachFirearmToApplicationSteps.SERIAL_IDENTIFICATION_MARKING: ~C(has_user_marked_rfd_as_invalid),
        AttachFirearmToApplicationSteps.SERIAL_NUMBERS: ~C(has_user_marked_rfd_as_invalid)
        & C(is_serial_numbers_available),
    }

    def get_form_kwargs(self, step=None):
        kwargs = super().get_form_kwargs(step)

        if step == AttachFirearmToApplicationSteps.IS_RFD_CERTIFICATE_VALID:
            kwargs["rfd_certificate"] = get_rfd_certificate(self.application)

        if step == AttachFirearmToApplicationSteps.SERIAL_NUMBERS:
            quantity_step_data = self.get_cleaned_data_for_step(AttachFirearmToApplicationSteps.QUANTITY_AND_VALUE)
            kwargs["number_of_items"] = quantity_step_data["number_of_items"]

        return kwargs

    def get_success_url(self):
        return reverse(
            "applications:attach_product_on_application_summary",
            kwargs={
                "pk": self.kwargs["pk"],
                "good_on_application_pk": self.good_on_application["id"],
            },
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

    def get_edit_firearm_payload(self, form_dict):
        return AttachFirearmToApplicationGoodPayloadBuilder().build(form_dict)

    @expect_status(
        HTTPStatus.OK,
        "Error updating firearm",
        "Unexpected error updating firearm",
    )
    def edit_firearm(self, good_pk, form_dict):
        payload = self.get_edit_firearm_payload(form_dict)
        return edit_firearm_for_attaching(self.request, good_pk, payload)

    def is_rfd_invalid(self, form_dict):
        if AttachFirearmToApplicationSteps.IS_RFD_CERTIFICATE_VALID not in form_dict:
            return False

        form = form_dict[AttachFirearmToApplicationSteps.IS_RFD_CERTIFICATE_VALID]
        is_rfd_certificate_data = form.cleaned_data

        return is_rfd_certificate_data.get("is_rfd_certificate_valid") is False

    def get_firearm_to_application_payload(self, form_dict):
        good_payload = AttachFirearmToApplicationGoodOnApplicationPayloadBuilder().build(form_dict)
        firearms_act_payload = FirearmsActPayloadBuilder(
            self.application,
            good_payload["firearm_details"],
        ).build(form_dict)

        payload = always_merger.merge(good_payload, firearms_act_payload)

        return payload

    @expect_status(
        HTTPStatus.CREATED,
        "Error adding firearm to application",
        "Unexpected error adding firearm to application",
    )
    def post_firearm_to_application(self, form_dict):
        payload = self.get_firearm_to_application_payload(form_dict)
        return post_firearm_good_on_application(
            self.request,
            self.application["id"],
            self.good["id"],
            payload,
        )

    def get_context_data(self, form, **kwargs):
        ctx = super().get_context_data(form, **kwargs)

        ctx["back_link_url"] = reverse(
            "applications:preexisting_good",
            kwargs={
                "pk": self.kwargs["pk"],
            },
        )
        ctx["title"] = form.Layout.TITLE

        return ctx

    def get_query_params(self, form_dict):
        params = {}

        if AttachFirearmToApplicationSteps.CATEGORY in form_dict:
            params["added_firearm_category"] = True

        if AttachFirearmToApplicationSteps.IS_RFD_CERTIFICATE_VALID in form_dict:
            params["confirmed_rfd_validity"] = True

        return params

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

    def has_existing_valid_organisation_rfd_certificate(self, application):
        if not has_valid_organisation_rfd_certificate(application):
            return False

        is_rfd_certificate_valid_cleaned_data = self.get_cleaned_data_for_step(
            AttachFirearmToApplicationSteps.IS_RFD_CERTIFICATE_VALID,
        )
        return is_rfd_certificate_valid_cleaned_data.get("is_rfd_certificate_valid", False)

    def done(self, form_list, form_dict, **kwargs):
        if self.is_rfd_invalid(form_dict):
            # This is an error state, we shouldn't have been able to submit if
            # the RFD is invalid so throw an error
            return error_page(self.request, "RFD invalid. Cannot submit.")

        try:
            self.edit_firearm(self.good["id"], form_dict)

            if self.has_existing_valid_organisation_rfd_certificate(self.application):
                self.attach_rfd_certificate_to_application(self.application)

            good_on_application, _ = self.post_firearm_to_application(form_dict)
            good_on_application = good_on_application["good"]

            GoodOnApplicationFirearmActCertificateAction(
                self.request,
                FirearmsActDocumentType.SECTION_1,
                self.application,
                self.good,
                good_on_application,
                self.get_cleaned_data_for_step(AttachFirearmToApplicationSteps.ATTACH_FIREARM_CERTIFICATE),
            ).run()

            GoodOnApplicationFirearmActCertificateAction(
                self.request,
                FirearmsActDocumentType.SECTION_2,
                self.application,
                self.good,
                good_on_application,
                self.get_cleaned_data_for_step(AttachFirearmToApplicationSteps.ATTACH_SHOTGUN_CERTIFICATE),
            ).run()
        except ServiceError as e:
            return self.handle_service_error(e)

        self.good_on_application = good_on_application

        success_url = self.get_success_url()
        qs = ""
        params = self.get_query_params(form_dict)
        if params:
            qs = f"?{urlencode(params)}"

        return redirect(f"{success_url}{qs}")
