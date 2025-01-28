from core.wizard.payloads import MergingPayloadBuilder
from exporter.applications.views.goods.common.payloads import get_cleaned_data
from exporter.core.constants import AddF680FormSteps  # /PS-IGNORE


class AddF680PayloadBuilder(MergingPayloadBuilder):  # /PS-IGNORE
    payload_dict = {
        AddF680FormSteps.F680INITIAL: get_cleaned_data,  # /PS-IGNORE
    }

    def build(self, form_dict):
        payload = super().build(form_dict)
        return {"data": payload}
