from core.wizard.payloads import MergingPayloadBuilder
from exporter.applications.views.goods.common.payloads import get_cleaned_data
from .constants import ApplicationFormSteps


class F680CreatePayloadBuilder(MergingPayloadBuilder):
    payload_dict = {
        ApplicationFormSteps.APPLICATION_NAME: get_cleaned_data,
    }

    def build(self, form_dict):
        payload = super().build(form_dict)
        return {"application": payload}
