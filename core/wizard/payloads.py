from deepmerge import always_merger


class MergingPayloadBuilder:
    def build(self, form_dict):
        payload = {}
        for step_name, payload_func in self.payload_dict.items():
            form = form_dict.get(step_name)
            if form:
                always_merger.merge(payload, payload_func(form))
        return payload


def get_cleaned_data(form):
    return form.cleaned_data


def get_questions_data(form):
    if not form.cleaned_data:
        return {}
    questions = {}
    for field_name, field in form.declared_fields.items():
        questions[field_name] = field.label
    return questions
