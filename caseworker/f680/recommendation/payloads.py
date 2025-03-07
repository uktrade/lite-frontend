from caseworker.f680.recommendation.constants import RecommendationSteps
from core.wizard.payloads import MergingPayloadBuilder


def get_cleaned_data(form):
    return form.cleaned_data


class RecommendationPayloadBuilder(MergingPayloadBuilder):

    def build(self, form_dict, countries):
        self.payload_dict = {}
        for item in countries:
            name = item["answer"].replace(" ", "-")
            key = f"destination_{item['raw_answer']}_{name}_provisos"
            self.payload_dict[key] = get_cleaned_data

        return super().build(form_dict)
