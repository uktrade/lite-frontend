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

    # As per the SIELs applcation here exporter/applications/forms/declaration.py

    # An old pplication question asked if the exporter would find an FOI harmful to their
    # interests, but the variable name agreed_to_foi suggests the opposite,
    # that they agree to have their application be made public under FOI.
    # Maybe agreed_that_foi_harmful would be less confusing. Also,
    # the new question asks if the exporter agrees to make their application
    # publicly available, and the variable name should reflect that.

    # False equating to Yes and True equating to No reflects the current SIELs functionality
    # so it is presumed that some kind of upstream functionality relied on this so best to
    # replicate rather than change at this point
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
