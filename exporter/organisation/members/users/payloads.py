from exporter.applications.views.goods.common.payloads import get_cleaned_data
from core.wizard.payloads import MergingPayloadBuilder

from .constants import AddUserSteps


class AddMemberPayloadBuilder(MergingPayloadBuilder):
    payload_dict = {
        AddUserSteps.SELECT_ROLE: get_cleaned_data,
        AddUserSteps.ADD_MEMBER: get_cleaned_data,
    }
