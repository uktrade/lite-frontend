from exporter.core.wizard.payloads import MergingPayloadBuilder

from .constants import AddGoodSoftwareSteps, AddGoodSoftwareToApplicationSteps
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


class AddGoodSoftwarePayloadBuilder(MergingPayloadBuilder):
    payload_dict = {
        AddGoodSoftwareSteps.NAME: get_cleaned_data,
        AddGoodSoftwareSteps.PRODUCT_CONTROL_LIST_ENTRY: get_cleaned_data,
        AddGoodSoftwareSteps.PV_GRADING: get_pv_grading_payload,
        AddGoodSoftwareSteps.PV_GRADING_DETAILS: get_pv_grading_good_payload,
        AddGoodSoftwareSteps.PRODUCT_USES_INFORMATION_SECURITY: get_cleaned_data,
        AddGoodSoftwareSteps.PRODUCT_DOCUMENT_AVAILABILITY: get_cleaned_data,
        AddGoodSoftwareSteps.PRODUCT_DOCUMENT_SENSITIVITY: get_cleaned_data,
        AddGoodSoftwareSteps.PRODUCT_MILITARY_USE: get_cleaned_data,
    }


class AddGoodSoftwareToApplicationPayloadBuilder(MergingPayloadBuilder):
    payload_dict = {
        AddGoodSoftwareToApplicationSteps.ONWARD_EXPORTED: get_cleaned_data,
        AddGoodSoftwareToApplicationSteps.ONWARD_ALTERED_PROCESSED: get_cleaned_data,
        AddGoodSoftwareToApplicationSteps.ONWARD_INCORPORATED: get_cleaned_data,
        AddGoodSoftwareToApplicationSteps.QUANTITY_AND_VALUE: get_quantity_and_value_payload,
    }
