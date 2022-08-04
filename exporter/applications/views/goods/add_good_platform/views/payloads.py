from exporter.core.wizard.payloads import MergingPayloadBuilder
from exporter.core.common.forms import get_cleaned_data

from .constants import AddGoodPlatformSteps
from exporter.applications.views.goods.add_good_firearm.views.payloads import (
    get_pv_grading_payload,
    get_pv_grading_good_payload,
)


class AddGoodPlatformPayloadBuilder(MergingPayloadBuilder):
    payload_dict = {
        AddGoodPlatformSteps.NAME: get_cleaned_data,
        AddGoodPlatformSteps.PRODUCT_CONTROL_LIST_ENTRY: get_cleaned_data,
        AddGoodPlatformSteps.PV_GRADING: get_pv_grading_payload,
        AddGoodPlatformSteps.PV_GRADING_DETAILS: get_pv_grading_good_payload,
    }
