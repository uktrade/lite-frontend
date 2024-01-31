from django import forms

from crispy_forms_gds.helper import FormHelper
from crispy_forms_gds.layout import Layout, Button


class CloseQueryForm(forms.Form):
    reason_for_closing_query = forms.CharField(
        label="",
        widget=forms.Textarea,
        help_text="Why are you closing the query? This will not be visible to the exporter.",
        required=False,
    )

    def use_hint_as_aria_labelledby(self, field_name):
        """
        :param field_name: Name of the field to add an aria-labelledby attribute to.

        Add an aria-labelledby attribute to a field's widget referencing the field's hint widget.
        """
        field = self.fields[field_name]
        label_id = (self.auto_id % self.prefix) + f"-{field_name}_hint"
        field.widget.attrs["aria-labelledby"] = label_id

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout("reason_for_closing_query", Button("submit", "Submit"))
        self.use_hint_as_aria_labelledby("reason_for_closing_query")
