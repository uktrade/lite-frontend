from core.wizard.payloads import MergingPayloadBuilder, get_cleaned_data
from exporter.core.constants import (
    SetPartyFormSteps,
)


class SetConsigneePayloadBuilder(MergingPayloadBuilder):
    payload_dict = {
        SetPartyFormSteps.PARTY_SUB_TYPE: get_cleaned_data,
        SetPartyFormSteps.PARTY_NAME: get_cleaned_data,
        SetPartyFormSteps.PARTY_WEBSITE: get_cleaned_data,
        SetPartyFormSteps.PARTY_ADDRESS: get_cleaned_data,
    }
