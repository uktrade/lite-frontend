from exporter.core.wizard.payloads import MergingPayloadBuilder
from exporter.core.common.forms import get_cleaned_data

from .constants import CompleteProductSteps
from exporter.applications.views.goods.add_good_firearm.views.payloads import (
    get_pv_grading_payload,
    get_pv_grading_good_payload,
)


class AddGoodCompleteProductPayloadBuilder(MergingPayloadBuilder):
    payload_dict = {
        CompleteProductSteps.NAME: get_cleaned_data,
        CompleteProductSteps.PV_GRADING: get_pv_grading_payload,
        CompleteProductSteps.PV_GRADING_DETAILS: get_pv_grading_good_payload,
    }
