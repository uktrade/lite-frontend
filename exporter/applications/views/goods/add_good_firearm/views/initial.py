from datetime import datetime

from exporter.core.forms import CurrentFile
from exporter.core.helpers import (
    get_organisation_firearm_act_document,
    has_organisation_firearm_act_document,
)
from exporter.goods.forms.firearms import (
    FirearmFirearmAct1968Form,
    FirearmSection5Form,
)

from .helpers import (
    get_good_on_application_document_url,
    get_organisation_document_url,
)


def get_is_covered_by_section_5_initial_data(firearm_details):
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

    return {}


def get_attach_organisation_certificate_initial_data(document_type, application, good):
    if not has_organisation_firearm_act_document(application, document_type):
        return {}

    document = get_organisation_firearm_act_document(application, document_type)
    firearm_details = good["firearm_details"]
    section_certificate_date_of_expiry = firearm_details.get("section_certificate_date_of_expiry")
    if section_certificate_date_of_expiry:
        section_certificate_date_of_expiry = datetime.fromisoformat(section_certificate_date_of_expiry).date()
    return {
        "section_certificate_missing": firearm_details.get("section_certificate_missing"),
        "section_certificate_number": firearm_details.get("section_certificate_number"),
        "section_certificate_date_of_expiry": section_certificate_date_of_expiry,
        "section_certificate_missing_reason": firearm_details.get("section_certificate_missing_reason"),
        "file": CurrentFile(
            document["document"]["name"],
            get_organisation_document_url(document),
            document["document"]["safe"],
        ),
    }


def get_attach_good_on_application_certificate_initial_data(document, application, good, good_on_application):
    firearm_details = good_on_application["firearm_details"]
    section_certificate_date_of_expiry = firearm_details.get("section_certificate_date_of_expiry")
    if section_certificate_date_of_expiry:
        section_certificate_date_of_expiry = datetime.fromisoformat(section_certificate_date_of_expiry).date()
    return {
        "section_certificate_missing": firearm_details.get("section_certificate_missing"),
        "section_certificate_number": firearm_details.get("section_certificate_number"),
        "section_certificate_date_of_expiry": section_certificate_date_of_expiry,
        "section_certificate_missing_reason": firearm_details.get("section_certificate_missing_reason"),
        "file": CurrentFile(
            document["name"],
            get_good_on_application_document_url(application, good, document),
            document["safe"],
        ),
    }


def get_firearm_act_1968_initial_data(firearm_details):
    is_covered_by_firearm_act_section_one_two_or_five = firearm_details.get(
        "is_covered_by_firearm_act_section_one_two_or_five"
    )
    if not is_covered_by_firearm_act_section_one_two_or_five:
        return {}

    if is_covered_by_firearm_act_section_one_two_or_five == "No":
        return {}

    if is_covered_by_firearm_act_section_one_two_or_five == "Unsure":
        return {
            "firearms_act_section": FirearmFirearmAct1968Form.SectionChoices.DONT_KNOW,
            "not_covered_explanation": firearm_details["is_covered_by_firearm_act_section_one_two_or_five_explanation"],
        }

    return {
        "firearms_act_section": firearm_details["firearms_act_section"],
    }


def get_year_of_manufacture_initial_data(firearm_details):
    year_of_manufacture = firearm_details.get("year_of_manufacture")
    if not year_of_manufacture:
        return {}

    return {
        "year_of_manufacture": year_of_manufacture,
    }


def get_onward_altered_processed_initial_data(firearm_details):
    return {
        "is_onward_altered_processed": firearm_details["is_onward_altered_processed"],
        "is_onward_altered_processed_comments": firearm_details["is_onward_altered_processed_comments"],
    }


def get_onward_incorporated_initial_data(firearm_details):
    return {
        "is_onward_incorporated": firearm_details["is_onward_incorporated"],
        "is_onward_incorporated_comments": firearm_details["is_onward_incorporated_comments"],
    }


def get_is_deactivated_to_standard_initial_data(firearm_details):
    date_of_deactivation = firearm_details["date_of_deactivation"]
    if date_of_deactivation:
        date_of_deactivation = datetime.fromisoformat(firearm_details["date_of_deactivation"]).date()

    return {
        "date_of_deactivation": date_of_deactivation,
        "is_deactivated_to_standard": firearm_details["is_deactivated_to_standard"],
        "not_deactivated_to_standard_comments": firearm_details["not_deactivated_to_standard_comments"],
    }


def get_serial_numbers_initial_data(firearm_details):
    return {
        "serial_numbers": firearm_details["serial_numbers"],
    }
