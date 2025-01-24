from core.wizard.payloads import MergingPayloadBuilder

from exporter.f680.constants import (
    ApplicationFormSteps,
    ProductFormSteps,
)


def get_cleaned_data_with_label(form):
    return {
        field_name: {
            "label": form.get_field_label(field_name),
            "value": value,
        }
        for field_name, value in form.cleaned_data.items()
    }


class F680CreatePayloadBuilder(MergingPayloadBuilder):
    payload_dict = {
        ApplicationFormSteps.APPLICATION_NAME: get_cleaned_data_with_label,
        ApplicationFormSteps.PREVIOUS_APPLICATION: get_cleaned_data_with_label,
    }

    def build(self, form_dict):
        payload = super().build(form_dict)
        return {"application": {"application": payload}}


class F680CreateProductPayloadBuilder(MergingPayloadBuilder):
    payload_dict = {
        ProductFormSteps.NAME_AND_DESCRIPTION: get_cleaned_data_with_label,
    }

    def build(self, form_dict, initial_payload):
        payload = super().build(form_dict)
        initial_payload["application"]["products"].append(payload)
        return initial_payload
