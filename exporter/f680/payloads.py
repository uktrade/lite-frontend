from core.wizard.payloads import get_cleaned_data, MergingPayloadBuilder

from exporter.f680.constants import ApplicationFormSteps


class F680CreatePayloadBuilder(MergingPayloadBuilder):
    payload_dict = {
        ApplicationFormSteps.APPLICATION_NAME: get_cleaned_data,
    }

    def build(self, form_dict):
        payload = super().build(form_dict)

        return {"application": payload}
