from deepmerge import always_merger


def get_cleaned_data(form):
    return form.cleaned_data


class MergingPayloadBuilder:
    def get_payload_dict(self):
        return self.payload_dict

    def build(self, form_dict, initial_payload=None):
        payload = {}
        if initial_payload:
            payload = initial_payload

        payload_dict = self.get_payload_dict()
        for step_name, payload_func in payload_dict.items():
            form = form_dict.get(step_name)
            if form:
                always_merger.merge(payload, payload_func(form))

        return payload
