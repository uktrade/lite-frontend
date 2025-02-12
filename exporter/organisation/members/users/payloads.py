from core.wizard.payloads import MergingPayloadBuilder, get_cleaned_data

from .constants import AddUserSteps


class AddMemberPayloadBuilder(MergingPayloadBuilder):
    payload_dict = {
        AddUserSteps.SELECT_ROLE: get_cleaned_data,
        AddUserSteps.ADD_MEMBER: get_cleaned_data,
    }
