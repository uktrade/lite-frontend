from core.wizard.payloads import MergingPayloadBuilder
from exporter.applications.views.goods.common.payloads import get_cleaned_data
from exporter.core.constants import AddF680FormSteps


class AddF680PayloadBuilder(MergingPayloadBuilder):
    payload_dict = {
        AddF680FormSteps.F680INITIAL: get_cleaned_data,
    }
