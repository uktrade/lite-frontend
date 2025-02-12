from exporter.applications.views.goods.common import constants
from core.wizard.payloads import MergingPayloadBuilder, get_cleaned_data


def get_pv_grading_payload(form):
    return {
        "is_pv_graded": "yes" if form.cleaned_data["is_pv_graded"] else "no",
    }


def get_pv_grading_details_payload(form):
    payload = form.cleaned_data.copy()
    payload["date_of_issue"] = payload["date_of_issue"].isoformat()
    return {
        "pv_grading_details": payload,
    }


def get_part_number_payload(form):
    if form.cleaned_data["part_number_missing"]:
        return {
            "part_number": "",
            "no_part_number_comments": form.cleaned_data["no_part_number_comments"],
        }
    else:
        return {
            "part_number": form.cleaned_data["part_number"],
            "no_part_number_comments": "",
        }


def get_quantity_and_value_payload(form):
    return {
        "unit": "NAR",
        "quantity": str(form.cleaned_data["number_of_items"]),
        "value": str(form.cleaned_data["value"]),
    }


def get_unit_quantity_and_value_payload(form):
    return {
        "unit": form.cleaned_data["unit"],
        "quantity": str(form.cleaned_data["quantity"]),
        "value": str(form.cleaned_data["value"]),
    }


class ProductEditPVGradingPayloadBuilder(MergingPayloadBuilder):
    payload_dict = {
        constants.PV_GRADING: get_pv_grading_payload,
        constants.PV_GRADING_DETAILS: get_pv_grading_details_payload,
    }


class ProductEditProductDocumentAvailabilityPayloadBuilder(MergingPayloadBuilder):
    payload_dict = {
        constants.PRODUCT_DOCUMENT_AVAILABILITY: get_cleaned_data,
        constants.PRODUCT_DESCRIPTION: get_cleaned_data,
        constants.PRODUCT_DOCUMENT_SENSITIVITY: get_cleaned_data,
    }


class ProductEditProductDocumentSensitivityPayloadBuilder(MergingPayloadBuilder):
    payload_dict = {
        constants.PRODUCT_DOCUMENT_SENSITIVITY: get_cleaned_data,
    }
