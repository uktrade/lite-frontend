from django import forms
from django.template.loader import render_to_string

from crispy_forms_gds.layout import HTML

from core.common.forms import BaseForm


class ApplicationPresubmissionForm(BaseForm):
    class Layout:
        TITLE = ""
        SUBMIT_BUTTON_TEXT = "Save and continue"

    def get_layout_fields(self):
        return []


class ApplicationSubmissionForm(BaseForm):
    class Layout:
        TITLE = "Submit your application"
        SUBTITLE = render_to_string("f680/forms/subtitle_declaration.html")
        SUBMIT_BUTTON_TEXT = "Accept and submit"

    foi_choice = forms.TypedChoiceField(
        choices=(
            ("yes", "Yes"),
            ("no", "No"),
        ),
        label="Do you agree to make the application details publicly available?",
        widget=forms.RadioSelect,
        error_messages={"required": "If you agree to make the application details publicly available click yes"},
        required=True,
    )

    def get_layout_fields(self):
        return (
            "foi_choice",
            HTML(render_to_string("f680/forms/declaration.html")),
        )
