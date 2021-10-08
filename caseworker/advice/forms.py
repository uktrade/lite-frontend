from django import forms

from crispy_forms_gds.helper import FormHelper
from crispy_forms_gds.layout import Submit


class TextInputForm(forms.Form):

    name = forms.CharField(
        label="Name",
        help_text="Your full name.",
        widget=forms.TextInput(),
        error_messages={
            "required": "Enter your name as it appears on your passport"
        }
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.add_input(Submit("submit", "Submit"))
