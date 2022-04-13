from functools import wraps

from exporter.core.wizard.payloads import MergingPayloadBuilder
from exporter.goods.forms.firearms import (
    FirearmFirearmAct1968Form,
    FirearmSection5Form,
)

from .constants import AddGoodFirearmSteps


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
        AddGoodFirearmSteps.ATTACH_FIREARM_CERTIFICATE: get_attach_firearm_act_certificate_payload,
        AddGoodFirearmSteps.ATTACH_SHOTGUN_CERTIFICATE: get_attach_firearm_act_certificate_payload,
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
