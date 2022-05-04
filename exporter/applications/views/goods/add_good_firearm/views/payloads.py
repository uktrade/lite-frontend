from functools import wraps

from exporter.core.constants import (
    FirearmsActDocumentType,
    FirearmsActSections,
)
from exporter.core.helpers import (
    convert_api_date_string_to_date,
    get_organisation_documents,
)
from exporter.core.wizard.payloads import MergingPayloadBuilder
from exporter.goods.forms.firearms import (
    FirearmFirearmAct1968Form,
    FirearmSection5Form,
)

from .constants import AddGoodFirearmSteps, AddGoodFirearmToApplicationSteps


def firearm_details_payload(f):
    @wraps(f)
    def wrapper(form):
        return {"firearm_details": f(form)}

    return wrapper


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


def get_cleaned_data(form):
    return form.cleaned_data


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
            "is_covered_by_firearm_act_section_one_two_or_five_explanation": "",
        }

    if is_covered_by_section_5 == FirearmSection5Form.Section5Choices.DONT_KNOW:
        return {
            "is_covered_by_firearm_act_section_one_two_or_five": "Unsure",
        }

    return {
        "is_covered_by_firearm_act_section_one_two_or_five": "Yes",
        "is_covered_by_firearm_act_section_one_two_or_five_explanation": "",
        "firearms_act_section": "firearms_act_section5",
    }


def get_onward_incorporated_payload(form):
    firearm_details = get_firearm_details_cleaned_data(form)

    # We copy the value back to the original field as well as populating the new
    # field.
    # Because we are going to have firearm products coming from the new wizard
    # and the old wizard we want to make sure that we synchronise this value
    # back to the old field.
    return {
        "is_good_incorporated": form.cleaned_data["is_onward_incorporated"],
        **firearm_details,
    }


@firearm_details_payload
def get_deactivation_details_payload(form):
    firearm_deactivation_details_data = form.cleaned_data
    return {
        "date_of_deactivation": firearm_deactivation_details_data["date_of_deactivation"].isoformat(),
        "is_deactivated_to_standard": firearm_deactivation_details_data["is_deactivated_to_standard"],
        "not_deactivated_to_standard_comments": firearm_deactivation_details_data[
            "not_deactivated_to_standard_comments"
        ],
    }


def get_quantity_and_value_payload(form):
    return {
        "unit": "NAR",
        "quantity": form.cleaned_data["number_of_items"],
        "value": str(form.cleaned_data["value"]),
        "firearm_details": {
            "number_of_items": form.cleaned_data["number_of_items"],
        },
    }


@firearm_details_payload
def get_serial_numbers_payload(form):
    firearm_serial_numbers_data = form.cleaned_data

    def sort_key(key):
        return int(key.replace("serial_number_input_", ""))

    keys = [key for key in firearm_serial_numbers_data.keys() if key.startswith("serial_number_input_")]
    sorted_keys = sorted(keys, key=sort_key)
    data = [firearm_serial_numbers_data[k] for k in sorted_keys]
    return {"serial_numbers": data}


class AddGoodFirearmPayloadBuilder(MergingPayloadBuilder):
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
        AddGoodFirearmSteps.ATTACH_SECTION_5_LETTER_OF_AUTHORITY: get_attach_firearm_act_certificate_payload,
    }


class FirearmEditProductDocumentAvailabilityPayloadBuilder(MergingPayloadBuilder):
    payload_dict = {
        AddGoodFirearmSteps.PRODUCT_DOCUMENT_AVAILABILITY: get_cleaned_data,
        AddGoodFirearmSteps.PRODUCT_DOCUMENT_SENSITIVITY: get_cleaned_data,
    }


class FirearmEditProductDocumentSensitivityPayloadBuilder(MergingPayloadBuilder):
    payload_dict = {
        AddGoodFirearmSteps.PRODUCT_DOCUMENT_SENSITIVITY: get_cleaned_data,
    }


class FirearmEditPvGradingPayloadBuilder(MergingPayloadBuilder):
    payload_dict = {
        AddGoodFirearmSteps.PV_GRADING: get_pv_grading_payload,
        AddGoodFirearmSteps.PV_GRADING_DETAILS: get_pv_grading_good_payload,
    }


class FirearmEditRegisteredFirearmsDealerPayloadBuilder(MergingPayloadBuilder):
    payload_dict = {
        AddGoodFirearmSteps.IS_REGISTERED_FIREARMS_DEALER: get_firearm_details_cleaned_data,
        AddGoodFirearmSteps.FIREARM_ACT_1968: get_firearm_act_1968_payload,
        AddGoodFirearmSteps.IS_COVERED_BY_SECTION_5: get_firearm_section_5_payload,
        AddGoodFirearmSteps.ATTACH_SECTION_5_LETTER_OF_AUTHORITY: get_attach_firearm_act_certificate_payload,
    }


class AddGoodFirearmToApplicationPayloadBuilder(MergingPayloadBuilder):
    payload_dict = {
        AddGoodFirearmToApplicationSteps.ATTACH_FIREARM_CERTIFICATE: get_attach_firearm_act_certificate_payload,
        AddGoodFirearmToApplicationSteps.ATTACH_SHOTGUN_CERTIFICATE: get_attach_firearm_act_certificate_payload,
        AddGoodFirearmToApplicationSteps.MADE_BEFORE_1938: get_firearm_details_cleaned_data,
        AddGoodFirearmToApplicationSteps.YEAR_OF_MANUFACTURE: get_firearm_details_cleaned_data,
        AddGoodFirearmToApplicationSteps.ONWARD_EXPORTED: get_firearm_details_cleaned_data,
        AddGoodFirearmToApplicationSteps.ONWARD_ALTERED_PROCESSED: get_firearm_details_cleaned_data,
        AddGoodFirearmToApplicationSteps.ONWARD_INCORPORATED: get_onward_incorporated_payload,
        AddGoodFirearmToApplicationSteps.IS_DEACTIVATED: get_firearm_details_cleaned_data,
        AddGoodFirearmToApplicationSteps.IS_DEACTIVATED_TO_STANDARD: get_deactivation_details_payload,
        AddGoodFirearmToApplicationSteps.QUANTITY_AND_VALUE: get_quantity_and_value_payload,
        AddGoodFirearmToApplicationSteps.SERIAL_IDENTIFICATION_MARKING: get_firearm_details_cleaned_data,
        AddGoodFirearmToApplicationSteps.SERIAL_NUMBERS: get_serial_numbers_payload,
    }


class FirearmsActPayloadBuilder:
    def __init__(self, application, firearm_details):
        self.application = application
        self.firearm_details = firearm_details

    def has_skipped_firearms_attach_step(self, form_dict, firearm_details, section_value, attach_step_name):
        firearms_act_section = firearm_details["firearms_act_section"]
        return firearms_act_section == section_value and attach_step_name not in form_dict

    def get_payload(self, form_dict):
        if not self.firearm_details.get("is_covered_by_firearm_act_section_one_two_or_five") == "Yes":
            return {}

        for section_value, attach_step_name, document_type in (
            (
                FirearmsActSections.SECTION_5,
                AddGoodFirearmSteps.ATTACH_SECTION_5_LETTER_OF_AUTHORITY,
                FirearmsActDocumentType.SECTION_5,
            ),
        ):
            if not self.has_skipped_firearms_attach_step(
                form_dict, self.firearm_details, section_value, attach_step_name
            ):
                continue

            certificate = get_organisation_documents(self.application)[document_type]
            return {
                "section_certificate_missing": False,
                "section_certificate_number": certificate["reference_code"],
                "section_certificate_date_of_expiry": convert_api_date_string_to_date(
                    certificate["expiry_date"]
                ).isoformat(),
            }

        return {}

    def build(self, form_dict):
        return {"firearm_details": self.get_payload(form_dict)}


class FirearmEditSection5FirearmsAct1968PayloadBuilder(MergingPayloadBuilder):
    payload_dict = {
        AddGoodFirearmSteps.IS_COVERED_BY_SECTION_5: get_firearm_section_5_payload,
        AddGoodFirearmSteps.ATTACH_SECTION_5_LETTER_OF_AUTHORITY: get_attach_firearm_act_certificate_payload,
    }


class FirearmEditFirearmsAct1968PayloadBuilder(MergingPayloadBuilder):
    payload_dict = {
        AddGoodFirearmSteps.FIREARM_ACT_1968: get_firearm_act_1968_payload,
        AddGoodFirearmSteps.ATTACH_SECTION_5_LETTER_OF_AUTHORITY: get_attach_firearm_act_certificate_payload,
    }
