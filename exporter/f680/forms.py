from django import forms
from django.template.loader import render_to_string

from crispy_forms_gds.layout import HTML

from core.common.forms import BaseForm
from core.forms.utils import coerce_str_to_bool
from core.forms.layouts import (
    ConditionalRadios,
    ConditionalRadiosQuestion,
)


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

    # This follows the same structure as the SIELs applcation here exporter/applications/forms/declaration.py
    agreed_to_foi = forms.TypedChoiceField(
        choices=(
            (False, "Yes"),
            (True, "No"),
        ),
        label="Do you agree to make the application details publicly available?",
        widget=forms.RadioSelect,
        error_messages={"required": "If you agree to make the application details publicly available click yes"},
        coerce=coerce_str_to_bool,
        required=True,
    )

    foi_reason = forms.CharField(
        widget=forms.Textarea,
        label=(
            "Explain why the disclosure of information would be harmful to your interests. "
            "While the Export Control Joint Unit (ECJU) will take your views into account, "
            "they cannot guarantee that the information will not be made public."
        ),
        required=False,
    )

    def clean(self):
        return self.add_required_to_conditional_text_field(
            parent_field="agreed_to_foi",
            parent_field_response=True,
            required_field="foi_reason",
            error_message="Non disclosure explanation cannot be blank",
        )

    def get_layout_fields(self):
        return (
            ConditionalRadios(
                "agreed_to_foi",
                "Yes",
                ConditionalRadiosQuestion("No", "foi_reason"),
            ),
            HTML(render_to_string("f680/forms/declaration.html")),
        )
