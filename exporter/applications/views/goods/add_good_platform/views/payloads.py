from exporter.core.wizard.payloads import MergingPayloadBuilder
from exporter.core.common.forms import get_cleaned_data

from .constants import AddGoodPlatformSteps
from exporter.applications.views.goods.common.payloads import (
    get_pv_grading_payload,
    get_pv_grading_good_payload,
)


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
