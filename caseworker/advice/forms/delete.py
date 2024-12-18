from django import forms

from crispy_forms_gds.helper import FormHelper
from crispy_forms_gds.layout import Submit


class DeleteAdviceForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.add_input(Submit("confirm", "Confirm"))
