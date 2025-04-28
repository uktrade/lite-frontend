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
        label="",
        help_text="Give the application a reference name so you can refer back to it when"
        " needed. The name does not need to be long or descriptive - it’s only for you.",
        error_messages={"required": "Enter an application name"},
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
        label="",
        widget=forms.RadioSelect,
        coerce=coerce_str_to_bool,
        error_messages={"required": "Select yes if you have made F680 applications before"},
    )

    def get_layout_fields(self):
        return ("has_made_previous_application",)


class PreviousApplicationsForm(BaseForm):
    class Layout:
        TITLE = "Previous applications"
        SUBMIT_BUTTON_TEXT = "Continue"

    previous_application_ecju_reference = forms.CharField(
        label="What are the ECJU reference numbers?",
        widget=forms.Textarea(attrs={"rows": "2"}),
        help_text="You can add multiple reference numbers. Separate them with a comma. For example, MODF2025/0001, MODF2025/0002, F680/2025/0001234.",
        error_messages={"required": "Enter a reference number"},
    )
    previous_application_details = forms.CharField(
        label="Describe any differences in this application",
        help_text="We need to know if anything has changed from your previous applications to this one.",
        widget=forms.Textarea(attrs={"rows": "5"}),
        error_messages={"required": "Enter details about the previous applications"},
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
        label="",
        widget=forms.RadioSelect,
        coerce=coerce_str_to_bool,
        error_messages={"required": "Select yes if you have exceptional circumstances"},
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
        error_messages={"required": "Enter details about why you need approval in less than 30 days"},
    )

    def get_layout_fields(self):
        return (
            "exceptional_circumstances_date",
            "exceptional_circumstances_reason",
        )
