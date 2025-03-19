from core.wizard.payloads import MergingPayloadBuilder


def get_cleaned_data(form):
    return form.cleaned_data


class RecommendationPayloadBuilder(MergingPayloadBuilder):

    def build(self, form_dict):
        payload = []
        for _, form in form_dict.items():
            if form:
                payload.append(get_cleaned_data(form))

        return payload
