from deepmerge import always_merger

from core.wizard.payloads import MergingPayloadBuilder, get_cleaned_data, get_questions_data
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
        answer_payload = {}
        question_payload = {}
        for form in form_dict.values():
            if form:
                always_merger.merge(answer_payload, get_cleaned_data(form))
                always_merger.merge(question_payload, get_questions_data(form))
        application_data[section] = {"answers": answer_payload, "questions": question_payload}
        return {"application": application_data}
