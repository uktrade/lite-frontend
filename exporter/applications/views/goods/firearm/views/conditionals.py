from core.constants import (
    FirearmsActSections,
    OrganisationDocumentType,
    SerialChoices,
)
from core.goods.helpers import is_product_category_made_before_1938 as _is_product_category_made_before_1938
from exporter.core.helpers import (
    has_organisation_firearm_act_document as _has_organisation_firearm_act_document,
    has_valid_rfd_certificate as has_valid_organisation_rfd_certificate,
)
from exporter.goods.forms.firearms import FirearmSection5Form

from .constants import (
    AddGoodFirearmSteps,
    AddGoodFirearmToApplicationSteps,
    AttachFirearmToApplicationSteps,
)


def has_organisation_rfd_certificate(wizard):
    return has_valid_organisation_rfd_certificate(wizard.application)


def has_application_rfd_certificate(wizard):
    additional_documents = wizard.application.get("additional_documents")
    if not additional_documents:
        return False

    for additional_document in additional_documents:
        if additional_document.get("document_type") == OrganisationDocumentType.RFD_CERTIFICATE:
            return True

    return False


def has_organisation_firearm_act_document(document_type):
    def check_has_organisation_firearm_act_document(wizard):
        return _has_organisation_firearm_act_document(wizard.application, document_type)

    return check_has_organisation_firearm_act_document


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

        try:
            is_covered_by_section_5_cleaned_data = wizard.get_cleaned_data_for_step(
                AddGoodFirearmSteps.IS_COVERED_BY_SECTION_5
            )
        except TypeError:
            return False

        if is_covered_by_section_5_cleaned_data and section == FirearmsActSections.SECTION_5:
            return (
                is_covered_by_section_5_cleaned_data.get("is_covered_by_section_5")
                == FirearmSection5Form.Section5Choices.YES
            )

        return False

    return _is_product_covered_by_section


def is_product_category_made_before_1938(wizard):
    return _is_product_category_made_before_1938(wizard.good["firearm_details"])


def is_product_made_before_1938(wizard):
    is_made_before_1938_cleaned_data = wizard.get_cleaned_data_for_step(
        AddGoodFirearmToApplicationSteps.MADE_BEFORE_1938
    )
    return is_made_before_1938_cleaned_data.get("is_made_before_1938", False)


def is_deactivated(wizard):
    is_deactivated = wizard.get_cleaned_data_for_step(AddGoodFirearmToApplicationSteps.IS_DEACTIVATED)
    return is_deactivated.get("is_deactivated", False)


def is_serial_numbers_available(wizard):
    serial_numbers_available_data = wizard.get_cleaned_data_for_step(
        AddGoodFirearmToApplicationSteps.SERIAL_IDENTIFICATION_MARKING
    )
    return serial_numbers_available_data.get("serial_numbers_available") == SerialChoices.AVAILABLE


def is_certificate_required(document_type):
    def _is_certificate_required(wizard):
        return wizard.good["firearm_details"].get("firearms_act_section") == document_type

    return _is_certificate_required


def has_firearm_category(wizard):
    return wizard.good["firearm_details"].get("category") is None


def is_firearm_certificate_invalid(wizard):
    is_rfd_valid_data = wizard.get_cleaned_data_for_step(
        AttachFirearmToApplicationSteps.IS_RFD_CERTIFICATE_VALID,
    )

    return is_rfd_valid_data.get("is_rfd_certificate_valid") is False


def has_quantity_and_value(wizard):
    quantity_and_value_data = wizard.get_cleaned_data_for_step(AddGoodFirearmToApplicationSteps.QUANTITY_AND_VALUE)
    return not quantity_and_value_data.get("no_set_quantities_or_value", False)
