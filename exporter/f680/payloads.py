from core.wizard.payloads import MergingPayloadBuilder
from exporter.applications.views.goods.common.payloads import get_cleaned_data
from .constants import ApplicationFormSteps  # /PS-IGNORE


class F680CreatePayloadBuilder(MergingPayloadBuilder):  # /PS-IGNORE
    payload_dict = {
        ApplicationFormSteps.APPLICATION_NAME: get_cleaned_data,  # /PS-IGNORE
    }

    def build(self, form_dict):
        payload = super().build(form_dict)
        return {"application": payload}
