from exporter.applications.views.goods.common import constants
from exporter.core.wizard.payloads import MergingPayloadBuilder


def get_cleaned_data(form):
    return form.cleaned_data


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


class ProductEditPVGradingPayloadBuilder(MergingPayloadBuilder):
    payload_dict = {
        constants.PV_GRADING: get_pv_grading_payload,
        constants.PV_GRADING_DETAILS: get_pv_grading_details_payload,
    }
