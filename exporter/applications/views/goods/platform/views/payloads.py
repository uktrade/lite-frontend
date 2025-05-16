from core.wizard.payloads import MergingPayloadBuilder

from .constants import AddGoodCompleteItemSteps, AddGoodCompleteItemToApplicationSteps
from exporter.applications.views.goods.common.payloads import (
    get_cleaned_data,
    get_pv_grading_payload,
    get_pv_grading_details_payload,
    get_part_number_payload,
    get_quantity_and_value_payload,
)


class AddGoodCompleteItemPayloadBuilder(MergingPayloadBuilder):
    payload_dict = {
        AddGoodCompleteItemSteps.NAME: get_cleaned_data,
        AddGoodCompleteItemSteps.PRODUCT_CONTROL_LIST_ENTRY: get_cleaned_data,
        AddGoodCompleteItemSteps.PART_NUMBER: get_part_number_payload,
        AddGoodCompleteItemSteps.PV_GRADING: get_pv_grading_payload,
        AddGoodCompleteItemSteps.PV_GRADING_DETAILS: get_pv_grading_details_payload,
        AddGoodCompleteItemSteps.PRODUCT_USES_INFORMATION_SECURITY: get_cleaned_data,
        AddGoodCompleteItemSteps.PRODUCT_DESCRIPTION: get_cleaned_data,
        AddGoodCompleteItemSteps.PRODUCT_DOCUMENT_AVAILABILITY: get_cleaned_data,
        AddGoodCompleteItemSteps.PRODUCT_DOCUMENT_SENSITIVITY: get_cleaned_data,
        AddGoodCompleteItemSteps.PRODUCT_MILITARY_USE: get_cleaned_data,
    }


class AddGoodCompleteItemToApplicationPayloadBuilder(MergingPayloadBuilder):
    payload_dict = {
        AddGoodCompleteItemToApplicationSteps.ONWARD_EXPORTED: get_cleaned_data,
        AddGoodCompleteItemToApplicationSteps.ONWARD_ALTERED_PROCESSED: get_cleaned_data,
        AddGoodCompleteItemToApplicationSteps.ONWARD_INCORPORATED: get_cleaned_data,
        AddGoodCompleteItemToApplicationSteps.QUANTITY_AND_VALUE: get_quantity_and_value_payload,
    }


def get_onward_incorporated_payload(form):
    cleaned_data = get_cleaned_data(form)

    return {
        "is_good_incorporated": form.cleaned_data["is_onward_incorporated"],
        **cleaned_data,
    }


class CompleteItemProductOnApplicationSummaryEditOnwardExportedPayloadBuilder(MergingPayloadBuilder):
    payload_dict = {
        AddGoodCompleteItemToApplicationSteps.ONWARD_EXPORTED: get_cleaned_data,
        AddGoodCompleteItemToApplicationSteps.ONWARD_ALTERED_PROCESSED: get_cleaned_data,
        AddGoodCompleteItemToApplicationSteps.ONWARD_INCORPORATED: get_onward_incorporated_payload,
    }
