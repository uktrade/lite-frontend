from caseworker.advice.constants import AdviceSteps
from core.wizard.payloads import get_cleaned_data, MergingPayloadBuilder


class GiveApprovalAdvicePayloadBuilder(MergingPayloadBuilder):
    payload_dict = {
        AdviceSteps.RECOMMEND_APPROVAL: get_cleaned_data,
        AdviceSteps.LICENCE_CONDITIONS: get_cleaned_data,
        AdviceSteps.LICENCE_FOOTNOTES: get_cleaned_data,
    }
