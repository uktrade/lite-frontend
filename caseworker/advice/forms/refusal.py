from django import forms
from django.utils.html import format_html

from caseworker.advice.forms.approval import PicklistAdviceForm
from crispy_forms_gds.helper import FormHelper
from crispy_forms_gds.layout import Field, Layout, Submit

from core.forms.layouts import (
    RadioTextArea,
)
from core.forms.widgets import GridmultipleSelect


def get_refusal_advice_form_factory(advice, denial_reasons_choices, refusal_reasons, data=None):
    data = data or {
        "refusal_reasons": advice["text"],
        "denial_reasons": [r for r in advice["denial_reasons"]],
    }
    return RefusalAdviceForm(data=data, choices=denial_reasons_choices, refusal_reasons=refusal_reasons)


class RefusalAdviceForm(PicklistAdviceForm):
    # The class name is used in js to convert this field into an autocomplete
    denial_reasons = forms.MultipleChoiceField(
        widget=forms.SelectMultiple(attrs={"class": "lite-refusal-reasons-autocomplete"}),
        label="What is the refusal criteria?",
        help_text=format_html(
            f'Select all <a class="govuk-link" '
            f'href="https://questions-statements.parliament.uk/written-statements/detail/2021-12-08/hcws449" '
            f'target="_blank">refusal criteria (opens in a new tab)</a> that apply'
        ),
        error_messages={"required": "Select at least one refusal criteria"},
    )
    refusal_reasons_radios = forms.ChoiceField(
        label="What are your reasons for this refusal?",
        widget=forms.RadioSelect,
        required=False,
        choices=(),
    )
    refusal_reasons = forms.CharField(
        widget=forms.Textarea(attrs={"rows": 7, "class": "govuk-!-margin-top-4"}),
        label="",
        error_messages={"required": "Enter a reason for refusing"},
    )

    def __init__(self, choices, *args, **kwargs):
        refusal_reasons = kwargs.pop("refusal_reasons")
        super().__init__(*args, **kwargs)
        self.fields["denial_reasons"].choices = choices
        label_size = {"label_size": "govuk-label--s"}

        refusal_reasons_choices, refusal_text = self._picklist_to_choices(refusal_reasons)
        self.refusal_text = refusal_text

        self.fields["refusal_reasons_radios"].choices = refusal_reasons_choices

        self.helper = FormHelper()
        self.helper.layout = Layout(
            Field("denial_reasons", context=label_size),
            RadioTextArea("refusal_reasons_radios", "refusal_reasons", refusal_text),
            Submit("submit", "Submit recommendation"),
        )


class FCDORefusalAdviceForm(RefusalAdviceForm):
    def __init__(self, choices, countries, *args, **kwargs):
        super().__init__(choices, *args, **kwargs)
        self.fields["countries"] = forms.MultipleChoiceField(
            choices=countries.items(),
            widget=GridmultipleSelect(),
            label="Select countries for which you want to give advice",
            error_messages={"required": "Select the destinations you want to make recommendations for"},
        )
        self.helper.layout = Layout(
            "countries",
            "denial_reasons",
            RadioTextArea("refusal_reasons_radios", "refusal_reasons", self.refusal_text),
            Submit("submit", "Submit recommendation"),
        )
