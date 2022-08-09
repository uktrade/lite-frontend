from exporter.core.wizard.payloads import MergingPayloadBuilder
from exporter.core.common.forms import get_cleaned_data

from .constants import AddGoodPlatformSteps, AddGoodPlatformToApplicationSteps
from exporter.applications.views.goods.common.payloads import (
    get_pv_grading_payload,
    get_pv_grading_good_payload,
)


def get_quantity_and_value_payload(form):
    return {
        "unit": "NAR",
        "quantity": form.cleaned_data["number_of_items"],
        "value": str(form.cleaned_data["value"]),
    }


class AddGoodPlatformPayloadBuilder(MergingPayloadBuilder):
    payload_dict = {
        AddGoodPlatformSteps.NAME: get_cleaned_data,
        AddGoodPlatformSteps.PRODUCT_CONTROL_LIST_ENTRY: get_cleaned_data,
        AddGoodPlatformSteps.PV_GRADING: get_pv_grading_payload,
        AddGoodPlatformSteps.PV_GRADING_DETAILS: get_pv_grading_good_payload,
        AddGoodPlatformSteps.PRODUCT_USES_INFORMATION_SECURITY: get_cleaned_data,
        AddGoodPlatformSteps.PRODUCT_DOCUMENT_AVAILABILITY: get_cleaned_data,
        AddGoodPlatformSteps.PRODUCT_DOCUMENT_SENSITIVITY: get_cleaned_data,
        AddGoodPlatformSteps.PRODUCT_MILITARY_USE: get_cleaned_data,
    }


class AddGoodPlatformToApplicationPayloadBuilder(MergingPayloadBuilder):
    payload_dict = {
        AddGoodPlatformToApplicationSteps.ONWARD_EXPORTED: get_cleaned_data,
        AddGoodPlatformToApplicationSteps.ONWARD_ALTERED_PROCESSED: get_cleaned_data,
        AddGoodPlatformToApplicationSteps.ONWARD_INCORPORATED: get_cleaned_data,
        AddGoodPlatformToApplicationSteps.QUANTITY_AND_VALUE: get_quantity_and_value_payload,
    }
