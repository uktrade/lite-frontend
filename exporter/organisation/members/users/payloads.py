from exporter.core.wizard.payloads import MergingPayloadBuilder
from .constants import AddUserSteps


def get_cleaned_data(form):
    return form.cleaned_data


class AddMemberPayloadBuilder(MergingPayloadBuilder):
    payload_dict = {
        AddUserSteps.SELECT_ROLE: get_cleaned_data,
        AddUserSteps.ADD_MEMBER: get_cleaned_data,
    }
