from crispy_forms_gds.helper import FormHelper
from crispy_forms_gds.layout import Layout, Submit

from django import forms

from core.forms.utils import coerce_str_to_bool


class ApplicationCopyConfirmationForm(forms.Form):
    DOCUMENT_TITLE = "Review and countersign this case"
    CONFIRMATION_CHOICES = [(True, "Yes"), (False, "No")]
    help_text = """Selecting Yes creates an exact copy of the current application which can be used
    to make amendments. You can still view current application but cannot modify it.
    The new application will need to be submitted again after all amendments."""

    confirm_copy = forms.TypedChoiceField(
        choices=CONFIRMATION_CHOICES,
        widget=forms.RadioSelect,
        coerce=coerce_str_to_bool,
        help_text=help_text,
        label="Confirm to create a copy of this application for amending it",
        error_messages={"required": "Confirmation required to copy application or not"},
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            "confirm_copy",
            Submit("submit", "Submit"),
        )
