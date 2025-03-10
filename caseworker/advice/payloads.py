from caseworker.advice.constants import AdviceSteps
from core.wizard.payloads import MergingPayloadBuilder


def get_cleaned_data(form):
    return form.cleaned_data


class GiveApprovalAdvicePayloadBuilder(MergingPayloadBuilder):
    payload_dict = {
        AdviceSteps.LICENCE_CONDITIONS: get_cleaned_data,
    }
