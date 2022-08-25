from exporter.core.wizard.payloads import MergingPayloadBuilder

from .constants import AddGoodMaterialSteps, AddGoodMaterialToApplicationSteps
from exporter.applications.views.goods.common.payloads import (
    get_cleaned_data,
    get_pv_grading_payload,
    get_pv_grading_details_payload,
    get_part_number_payload,
)


def get_quantity_and_value_payload(form):
    return {
        "unit": "NAR",
        "quantity": form.cleaned_data["number_of_items"],
        "value": str(form.cleaned_data["value"]),
    }


class AddGoodMaterialPayloadBuilder(MergingPayloadBuilder):
    payload_dict = {
        AddGoodMaterialSteps.NAME: get_cleaned_data,
        AddGoodMaterialSteps.PRODUCT_CONTROL_LIST_ENTRY: get_cleaned_data,
        AddGoodMaterialSteps.PART_NUMBER: get_part_number_payload,
        AddGoodMaterialSteps.PV_GRADING: get_pv_grading_payload,
        AddGoodMaterialSteps.PV_GRADING_DETAILS: get_pv_grading_details_payload,
        AddGoodMaterialSteps.PRODUCT_USES_INFORMATION_SECURITY: get_cleaned_data,
        AddGoodMaterialSteps.PRODUCT_DOCUMENT_AVAILABILITY: get_cleaned_data,
        AddGoodMaterialSteps.PRODUCT_DOCUMENT_SENSITIVITY: get_cleaned_data,
        AddGoodMaterialSteps.PRODUCT_MILITARY_USE: get_cleaned_data,
    }


class AddGoodMaterialToApplicationPayloadBuilder(MergingPayloadBuilder):
    payload_dict = {
        AddGoodMaterialToApplicationSteps.ONWARD_EXPORTED: get_cleaned_data,
        AddGoodMaterialToApplicationSteps.ONWARD_ALTERED_PROCESSED: get_cleaned_data,
        AddGoodMaterialToApplicationSteps.ONWARD_INCORPORATED: get_cleaned_data,
        AddGoodMaterialToApplicationSteps.QUANTITY_AND_VALUE: get_quantity_and_value_payload,
    }
