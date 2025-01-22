from core.wizard.payloads import MergingPayloadBuilder

from exporter.f680.constants import ApplicationFormSteps


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
    }

    def build(self, form_dict):
        payload = super().build(form_dict)
        return {"application": payload}
