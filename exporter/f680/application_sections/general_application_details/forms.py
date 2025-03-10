from django import forms
from django.template.loader import render_to_string

from crispy_forms_gds.fields import DateInputField
from crispy_forms_gds.layout.content import HTML

from core.common.forms import BaseForm
from core.forms.utils import coerce_str_to_bool

from exporter.core.validators import (
    FutureDateValidator,
    RelativeDeltaDateValidator,
)


class ApplicationNameForm(BaseForm):
    class Layout:
        TITLE = "Name the application"
        TITLE_AS_LABEL_FOR = "name"
        SUBMIT_BUTTON_TEXT = "Continue"

    name = forms.CharField(
        label=Layout.TITLE,
        help_text="Give the application a reference name so you can refer back to it when needed",
    )

    def get_layout_fields(self):
        return ("name",)


class PreviousApplicationConfirm(BaseForm):
    class Layout:
        TITLE = "Have you made a previous application?"
        TITLE_AS_LABEL_FOR = "has_made_previous_application"
        SUBMIT_BUTTON_TEXT = "Continue"

    has_made_previous_application = forms.TypedChoiceField(
        choices=(
            (True, "Yes"),
            (False, "No"),
        ),
        label=Layout.TITLE,
        widget=forms.RadioSelect,
        coerce=coerce_str_to_bool,
    )

    def get_layout_fields(self):
        return ("has_made_previous_application",)


class PreviousApplicationsForm(BaseForm):
    class Layout:
        TITLE = "Previous applications"
        SUBMIT_BUTTON_TEXT = "Continue"

    previous_application_ecju_reference = forms.CharField(label="What is the ECJU reference number?")
    previous_application_details = forms.CharField(
        label="Can you provide more detail?",
        help_text="For example if the products have been previously agreed or refused to the "
        "end-user or country.  Or if its for the same goods but to different destinations.  "
        "If possible provide the export trade licence number",
        widget=forms.Textarea(attrs={"rows": "5"}),
    )

    def get_layout_fields(self):
        return ("previous_application_ecju_reference", "previous_application_details")


class ExceptionalCircumstancesForm(BaseForm):
    class Layout:
        TITLE = "Do you have exceptional circumstances that mean you need F680 approval in less than 30 days?"
        TITLE_AS_LABEL_FOR = "is_exceptional_circumstances"
        SUBMIT_BUTTON_TEXT = "Continue"

    is_exceptional_circumstances = forms.TypedChoiceField(
        choices=(
            (True, "Yes"),
            (False, "No"),
        ),
        label="Do you have exceptional circumstances that mean you need F680 approval in less than 30 days?",
        widget=forms.RadioSelect,
        coerce=coerce_str_to_bool,
    )

    def get_layout_fields(self):
        return (
            "is_exceptional_circumstances",
            HTML.details(
                "Help with exceptional circumstances",
                render_to_string("f680/forms/help_exceptional_circumstances.html"),
            ),
        )


class ExplainExceptionalCircumstancesForm(BaseForm):
    class Layout:
        TITLE = "Explain your exceptional circumstances"
        SUBMIT_BUTTON_TEXT = "Save and continue"

    exceptional_circumstances_date = DateInputField(
        label="When do you need your F680 approval?",
        validators=[
            FutureDateValidator("Date must be in the future"),
            RelativeDeltaDateValidator("Date must be within 30 days", days=30),
        ],
    )
    exceptional_circumstances_reason = forms.CharField(
        label="Why do you need approval in less than 30 days?",
        widget=forms.Textarea(attrs={"rows": "5"}),
    )

    def get_layout_fields(self):
        return (
            "exceptional_circumstances_date",
            "exceptional_circumstances_reason",
        )
