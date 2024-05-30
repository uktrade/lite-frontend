from django import forms

from core.common.forms import BaseForm
from core.forms.utils import coerce_str_to_bool


class ApplicationCopyConfirmationForm(BaseForm):
    CONFIRMATION_CHOICES = [(True, "Yes"), (False, "No")]
    help_text = """Selecting Yes creates an exact copy of the current application which can be used
    to make amendments. The new application will need to be submitted again after all amendments.
     You can still view current application but cannot modify it."""

    class Layout:
        TITLE = "Confirm to create a copy of this application for making amendments"

    confirm_copy = forms.TypedChoiceField(
        choices=CONFIRMATION_CHOICES,
        widget=forms.RadioSelect,
        coerce=coerce_str_to_bool,
        help_text=help_text,
        label="",
        error_messages={"required": "Confirmation required to copy application or not"},
    )

    def get_layout_fields(self):
        return ("confirm_copy",)
