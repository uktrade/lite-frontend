from datetime import datetime
from django import forms
from django.template.loader import render_to_string

from crispy_forms_gds.fields import DateInputField
from crispy_forms_gds.layout.content import HTML

from core.common.forms import BaseForm
from core.forms.utils import coerce_str_to_bool


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
    )
    exceptional_circumstances_reason = forms.CharField(
        label="Why do you need approval in less than 30 days?",
        widget=forms.Textarea(attrs={"rows": "5"}),
    )

    def __init__(self, *args, **kwargs):
        # We have to do some coercion from string to datetime object here due to JSON serialization
        if (
            "initial" in kwargs
            and "exceptional_circumstances_date" in kwargs["initial"]
            and isinstance(kwargs["initial"]["exceptional_circumstances_date"], str)
        ):
            kwargs["initial"]["exceptional_circumstances_date"] = datetime.fromisoformat(
                kwargs["initial"]["exceptional_circumstances_date"]
            )
        return super().__init__(*args, **kwargs)

    def clean(self):
        # We have to do some coercion from datetime object to string here due to JSON serialization
        cleaned_data = super().clean()
        cleaned_data["exceptional_circumstances_date"] = cleaned_data["exceptional_circumstances_date"].isoformat()
        return cleaned_data

    def get_layout_fields(self):
        return (
            "exceptional_circumstances_date",
            "exceptional_circumstances_reason",
        )
