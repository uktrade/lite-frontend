from django import forms
from django.utils.html import format_html

from caseworker.advice.forms.approval import SelectAdviceForm
from caseworker.advice.forms.forms import PicklistAdviceForm
from crispy_forms_gds.helper import FormHelper
from crispy_forms_gds.layout import Layout, Submit

from core.forms.layouts import (
    RadioTextArea,
    CannedSnippetsTextArea,
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


class ConsolidateApprovalForm(PicklistAdviceForm):

    approval_reasons = forms.CharField(
        widget=forms.Textarea(attrs={"rows": 7, "class": "govuk-!-margin-top-4"}),
        label="",
        error_messages={"required": "Enter a reason for approving"},
    )
    approval_radios = forms.ChoiceField(
        label="What is your reason for approving?",
        required=False,
        widget=forms.RadioSelect,
        choices=(),
    )
    proviso = forms.CharField(
        widget=forms.Textarea(attrs={"rows": 7, "class": "govuk-!-margin-top-4"}),
        label="",
        required=False,
    )
    proviso_snippets = forms.ChoiceField(
        label="Add a licence condition (optional)",
        required=False,
        widget=forms.CheckboxSelectMultiple,
        choices=(),
    )

    def __init__(self, approval_reason, proviso, **kwargs):
        super().__init__(**kwargs)

        approval_choices, approval_text = self._picklist_to_choices(approval_reason, include_other=False)
        self.approval_text = approval_text
        self.fields["approval_radios"].choices = approval_choices

        proviso_choices, proviso_text = self._picklist_to_choices(proviso, include_other=False)
        self.proviso_text = proviso_text
        self.fields["proviso_snippets"].choices = proviso_choices

        self.helper = FormHelper()
        self.helper.layout = Layout(
            RadioTextArea("approval_radios", "approval_reasons", self.approval_text),
            CannedSnippetsTextArea("proviso_snippets", "proviso", self.proviso_text, add_label="Add licence condition"),
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
