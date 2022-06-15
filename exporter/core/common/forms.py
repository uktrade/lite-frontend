from crispy_forms_gds.helper import FormHelper
from crispy_forms_gds.layout import HTML, Layout, Submit
from django import forms


class BaseForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = FormHelper()
        for field in self.fields.values():
            if isinstance(field, forms.FileField):
                self.helper.attrs = {"enctype": "multipart/form-data"}
                break

        self.helper.layout = Layout(HTML.h1(self.Layout.TITLE), *self.get_layout_fields(), *self.get_layout_actions())

    def get_layout_fields(self):  # pragma: no cover
        raise NotImplementedError(f"Implement `get_layout_fields` on {self.__class__.__name__}")

    def get_layout_actions(self):
        return [
            Submit("submit", getattr(self.Layout, "SUBMIT_BUTTON", "Continue")),
        ]
