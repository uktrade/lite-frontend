from exporter.core.wizard.payloads import MergingPayloadBuilder

from .constants import AddGoodComponentSteps, AddGoodComponentToApplicationSteps
from exporter.applications.views.goods.common.payloads import (
    get_cleaned_data,
    get_pv_grading_payload,
    get_pv_grading_good_payload,
)


def get_quantity_and_value_payload(form):
    return {
        "unit": "NAR",
        "quantity": form.cleaned_data["number_of_items"],
        "value": str(form.cleaned_data["value"]),
    }


class AddGoodComponentPayloadBuilder(MergingPayloadBuilder):
    payload_dict = {
        AddGoodComponentSteps.NAME: get_cleaned_data,
        AddGoodComponentSteps.PRODUCT_CONTROL_LIST_ENTRY: get_cleaned_data,
        AddGoodComponentSteps.PV_GRADING: get_pv_grading_payload,
        AddGoodComponentSteps.PV_GRADING_DETAILS: get_pv_grading_good_payload,
        AddGoodComponentSteps.PRODUCT_USES_INFORMATION_SECURITY: get_cleaned_data,
        AddGoodComponentSteps.PRODUCT_DOCUMENT_AVAILABILITY: get_cleaned_data,
        AddGoodComponentSteps.PRODUCT_DOCUMENT_SENSITIVITY: get_cleaned_data,
        AddGoodComponentSteps.PRODUCT_MILITARY_USE: get_cleaned_data,
    }


class AddGoodComponentToApplicationPayloadBuilder(MergingPayloadBuilder):
    payload_dict = {
        AddGoodComponentToApplicationSteps.ONWARD_EXPORTED: get_cleaned_data,
        AddGoodComponentToApplicationSteps.ONWARD_ALTERED_PROCESSED: get_cleaned_data,
        AddGoodComponentToApplicationSteps.ONWARD_INCORPORATED: get_cleaned_data,
        AddGoodComponentToApplicationSteps.QUANTITY_AND_VALUE: get_quantity_and_value_payload,
    }
