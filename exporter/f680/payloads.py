from deepmerge import always_merger

from core.wizard.payloads import MergingPayloadBuilder, get_cleaned_data
from .constants import ApplicationFormSteps


class F680CreatePayloadBuilder(MergingPayloadBuilder):
    payload_dict = {
        ApplicationFormSteps.APPLICATION_NAME: get_cleaned_data,
    }

    def build(self, form_dict):
        payload = super().build(form_dict)
        return {"application": payload}


class F680PatchPayloadBuilder:
    def build(self, section, application_data, form_dict):
        payload = {}
        for step_name, form in form_dict.items():
            if form:
                always_merger.merge(payload, get_cleaned_data(form))
        application_data[section] = payload
        return {"application": application_data}
