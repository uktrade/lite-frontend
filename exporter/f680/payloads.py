from uuid import uuid4
from datetime import date

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
    def serialize(self, value):
        if isinstance(value, bool):
            return value, "boolean"
        elif isinstance(value, date):
            return value.isoformat(), "date"
        elif isinstance(value, str):
            return value, "string"
        elif isinstance(value, list):
            return value, "list"
        else:
            raise NotImplementedError(f"Must implement serialization for value {value} of type {type(value)}")

    def get_display_answer(self, form, field_name, answer):
        if isinstance(answer, list):
            return [self.get_display_answer(form, field_name, answer_value) for answer_value in answer]
        return dict(form.fields[field_name].choices)[answer]

    def get_fields(self, form):
        fields = []
        for field_name, value in form.cleaned_data.items():
            serialized_answer, datatype = self.serialize(value)
            answer = serialized_answer
            if hasattr(form.fields[field_name], "choices"):
                answer = self.get_display_answer(form, field_name, answer)
            fields.append(
                {
                    "key": field_name,
                    "answer": answer,
                    "raw_answer": serialized_answer,
                    "question": form[field_name].label,
                    "datatype": datatype,
                }
            )
        return fields

    def get_all_fields(self, forms):
        fields = []
        for form in forms:
            fields.extend(self.get_fields(form))
        return fields

    def build(self, section, section_label, application_data, form_dict):
        fields = self.get_all_fields(form_dict.values())
        section_payload = {
            "label": section_label,
            "fields": fields,
            "type": "single",
        }
        try:
            application_data["sections"][section] = section_payload
        except KeyError:
            application_data["sections"] = {section: section_payload}
        return {"application": application_data}


class F680AppendingPayloadBuilder(F680PatchPayloadBuilder):
    def build(self, section, section_label, application_data, form_dict, item_id=None):
        if not item_id:
            item_id = str(uuid4())

        fields = self.get_all_fields(form_dict.values())

        all_items = {}
        if application_data.get("sections", {}).get(section, {}).get("items"):
            flat_items = application_data["sections"][section]["items"]
            all_items = {item["id"]: item for item in flat_items}
        item = {"id": item_id, "fields": fields}
        all_items[item["id"]] = item

        section_payload = {
            "label": section_label,
            "items": list(all_items.values()),
            "type": "multiple",
        }
        try:
            application_data["sections"][section] = section_payload
        except KeyError:
            application_data["sections"] = {section: section_payload}

        return {"application": application_data}
