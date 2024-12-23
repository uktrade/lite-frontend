from django import forms

from core.common.forms import BaseForm
from crispy_forms_gds.helper import FormHelper
from crispy_forms_gds.layout import Layout, Submit
from crispy_forms_gds.choices import Choice

from core.forms.layouts import (
    ConditionalCheckboxes,
    ConditionalCheckboxesQuestion,
    ExpandingFieldset,
    RadioTextArea,
)


class PicklistAdviceForm(forms.Form):
    def _picklist_to_choices(self, picklist_data):
        reasons_choices = []
        reasons_text = {"other": ""}

        for result in picklist_data["results"]:
            key = "_".join(result.get("name").lower().split())
            choice = Choice(key, result.get("name"))
            if result == picklist_data["results"][-1]:
                choice = Choice(key, result.get("name"), divider="or")
            reasons_choices.append(choice)
            reasons_text[key] = result.get("text")
        reasons_choices.append(Choice("other", "Other"))
        return reasons_choices, reasons_text


class RecommendBulkApprovalForm(PicklistAdviceForm, BaseForm):
    class Layout:
        TITLE = "Recommend an approval"
        SUBMIT_BUTTON_TEXT = "Submit recommendation"

    approval_reasons = forms.CharField(
        widget=forms.Textarea(attrs={"rows": 7, "class": "govuk-!-margin-top-4"}),
        label="",
        error_messages={"required": "Enter a reason for approving"},
    )
    proviso = forms.CharField(
        widget=forms.Textarea(attrs={"rows": 7, "class": "govuk-!-margin-top-4"}),
        label="",
        required=False,
    )
    instructions_to_exporter = forms.CharField(
        widget=forms.Textarea(attrs={"rows": "3"}),
        label="Add any instructions for the exporter (optional)",
        help_text="These may be added to the licence cover letter, subject to review by the Licensing Unit.",
        required=False,
    )

    footnote_details_radios = forms.ChoiceField(
        label="Add a reporting footnote (optional)",
        required=False,
        widget=forms.RadioSelect,
        choices=(),
    )
    footnote_details = forms.CharField(
        widget=forms.Textarea(attrs={"rows": 3, "class": "govuk-!-margin-top-4"}),
        label="",
        required=False,
    )

    approval_radios = forms.ChoiceField(
        label="What is your reason for approving?",
        required=False,
        widget=forms.RadioSelect,
        choices=(),
    )
    proviso_radios = forms.ChoiceField(
        label="Add a licence condition (optional)",
        required=False,
        widget=forms.RadioSelect,
        choices=(),
    )

    def __init__(self, *args, **kwargs):
        approval_reason = kwargs.pop("approval_reason")
        proviso = kwargs.pop("proviso")
        footnote_details = kwargs.pop("footnote_details")
        # this follows the same pattern as denial_reasons.
        approval_choices, approval_text = self._picklist_to_choices(approval_reason)
        self.approval_text = approval_text
        proviso_choices, proviso_text = self._picklist_to_choices(proviso)
        self.proviso_text = proviso_text
        footnote_details_choices, footnote_text = self._picklist_to_choices(footnote_details)
        self.footnote_text = footnote_text
        super().__init__(*args, **kwargs)

        self.fields["approval_radios"].choices = approval_choices
        self.fields["proviso_radios"].choices = proviso_choices
        self.fields["footnote_details_radios"].choices = footnote_details_choices

    def get_layout_fields(self):
        return (
            RadioTextArea("approval_radios", "approval_reasons", self.approval_text),
            ExpandingFieldset(
                RadioTextArea("proviso_radios", "proviso", self.proviso_text),
                "instructions_to_exporter",
                RadioTextArea("footnote_details_radios", "footnote_details", self.footnote_text),
                legend="Add a licence condition, instruction to exporter or footnote",
                summary_css_class="supplemental-approval-fields",
            ),
        )
