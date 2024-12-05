from django import forms
from django.utils.html import format_html

from caseworker.advice.forms.approval import SelectAdviceForm
from caseworker.advice.forms.forms import GiveApprovalAdviceForm
from crispy_forms_gds.helper import FormHelper
from crispy_forms_gds.layout import Layout, Submit

from core.forms.layouts import (
    RadioTextArea,
)


class ConsolidateSelectAdviceForm(SelectAdviceForm):
    DOCUMENT_TITLE = "Recommend and combine case recommendation case"
    CHOICES = [("approve", "Approve"), ("refuse", "Refuse")]
    recommendation = forms.ChoiceField(
        choices=CHOICES,
        widget=forms.RadioSelect,
        label="",
        error_messages={"required": "Select if you approve or refuse"},
    )

    def __init__(self, team_name, *args, **kwargs):
        super().__init__(*args, **kwargs)

        recommendation_label = "What is the combined recommendation"
        if team_name:
            recommendation_label = f"{recommendation_label} for {team_name}"
        self.fields["recommendation"].label = f"{recommendation_label}?"


class ConsolidateApprovalForm(GiveApprovalAdviceForm):
    """Approval form minus some fields."""

    def __init__(self, team_alias, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.layout = Layout(
            RadioTextArea("approval_radios", "approval_reasons", self.approval_text),
            RadioTextArea("proviso_radios", "proviso", self.proviso_text),
            Submit("submit", "Submit recommendation"),
        )


class LUConsolidateRefusalForm(forms.Form):
    refusal_note = forms.CharField(
        widget=forms.Textarea(attrs={"rows": "7"}),
        label="Enter the refusal note as agreed in the refusal meeting",
        error_messages={"required": "Enter the refusal meeting note"},
    )

    denial_reasons = forms.MultipleChoiceField(
        widget=forms.SelectMultiple(),
        label="What is the refusal criteria?",
        help_text=format_html(
            f'Select all <a class="govuk-link" '
            f'href="https://questions-statements.parliament.uk/written-statements/detail/2021-12-08/hcws449" '
            f'target="_blank">refusal criteria (opens in a new tab)</a> that apply'
        ),
        error_messages={"required": "Select at least one refusal criteria"},
    )

    def __init__(self, choices, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["denial_reasons"].choices = choices
        self.helper = FormHelper()
        self.helper.layout = Layout("denial_reasons", "refusal_note", Submit("submit", "Submit recommendation"))
