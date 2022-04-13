from deepmerge import always_merger


class MergingPayloadBuilder:
    def build(self, form_dict):
        payload = {}
        for step_name, payload_func in self.payload_dict.items():
            form = form_dict.get(step_name)
            if form:
                always_merger.merge(payload, payload_func(form))
        return payload
