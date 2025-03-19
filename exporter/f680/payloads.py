from uuid import uuid4
from datetime import date


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
        fields = {}
        fields_sequence = []
        for field_name, value in form.cleaned_data.items():
            serialized_answer, datatype = self.serialize(value)
            answer = serialized_answer
            if hasattr(form.fields[field_name], "choices"):
                answer = self.get_display_answer(form, field_name, answer)
            fields_sequence.append(field_name)
            fields[field_name] = {
                "key": field_name,
                "answer": answer,
                "raw_answer": serialized_answer,
                "question": form.get_field_label(field_name),
                "datatype": datatype,
            }
        return fields, fields_sequence

    def get_all_fields(self, forms):
        fields = {}
        fields_sequence = []
        for form in forms:
            form_fields, form_fields_sequence = self.get_fields(form)
            fields.update(form_fields)
            fields_sequence.extend(form_fields_sequence)
        return fields, fields_sequence

    def build(self, section, section_label, application_data, form_dict):
        fields, fields_sequence = self.get_all_fields(form_dict.values())
        section_payload = {
            "label": section_label,
            "fields": fields,
            "fields_sequence": fields_sequence,
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

        fields, fields_sequence = self.get_all_fields(form_dict.values())

        all_items = {}
        if application_data.get("sections", {}).get(section, {}).get("items"):
            flat_items = application_data["sections"][section]["items"]
            all_items = {item["id"]: item for item in flat_items}
        item = {"id": item_id, "fields": fields, "fields_sequence": fields_sequence}
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


class F680DictPayloadBuilder(F680PatchPayloadBuilder):
    def build(self, section, section_label, application_data, dict_data):
        all_items = {}
        for item in dict_data:
            item_id = item.pop("id")
            fields = {}
            fields_sequence = []
            for key, value in item.items():
                serialized_answer, datatype = self.serialize(value)
                fields[key] = {
                    "key": key,
                    "answer": value,
                    "raw_answer": serialized_answer,
                    "question": key,
                    "datatype": datatype,
                }
                fields_sequence.append(key)
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
