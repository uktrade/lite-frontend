from django import forms

from crispy_forms_gds.helper import FormHelper
from crispy_forms_gds.layout import Layout, Button


class CloseQueryForm(forms.Form):
    reason_for_closing_query = forms.CharField(
        label="Why are you closing the query? This will not be visible to the exporter.",
        widget=forms.Textarea,
        error_messages={"required": "Enter a reason why you are closing the query"},
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            "reason_for_closing_query", Button("submit", "Submit", css_class="govuk-!-margin-bottom-0")
        )
