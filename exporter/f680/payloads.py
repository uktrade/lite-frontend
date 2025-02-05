from core.wizard.payloads import MergingPayloadBuilder


def get_cleaned_data_with_label(form):
    return {
        field_name: {
            "label": form.get_field_label(field_name),
            "value": value,
        }
        for field_name, value in form.cleaned_data.items()
    }


class BasePayloadBuilder(MergingPayloadBuilder):
    def __init__(self, wizard_view):
        self.wizard_view = wizard_view

    def get_payload_dict(self):
        return {step_name: get_cleaned_data_with_label for step_name in self.wizard_view.steps.all}


class F680CreatePayloadBuilder(BasePayloadBuilder):  # PS-IGNORE
    def build(self, form_dict):
        payload = super().build(form_dict)
        return {"application": payload}
