from django import forms
from django.forms.formsets import formset_factory

from crispy_forms_gds.helper import FormHelper
from crispy_forms_gds.layout import Layout, Submit
from crispy_forms_gds.choices import Choice
from core.forms.layouts import (
    ExpandingFieldset,
    RadioTextArea,
)
from core.forms.widgets import GridmultipleSelect


def get_formset(form_class, num=1, data=None, initial=None):
    factory = formset_factory(form_class, extra=num, min_num=num, max_num=num)
    return factory(data=data, initial=initial)


def get_approval_advice_form_factory(advice, approval_reason, proviso, footnote_details, data=None):
    data = data or {
        "proviso": advice["proviso"],
        "approval_reasons": advice["text"],
        "instructions_to_exporter": advice["note"],
        "footnote_details": advice["footnote"],
    }
    return GiveApprovalAdviceForm(
        approval_reason=approval_reason, proviso=proviso, footnote_details=footnote_details, data=data
    )


class PicklistAdviceForm(forms.Form):
    def _picklist_to_choices(self, picklist_data, include_other=True):
        reasons_choices = []
        reasons_text = {}

        for result in picklist_data["results"]:
            key = "_".join(result.get("name").lower().split())
            choice = Choice(key, result.get("name"))
            if result == picklist_data["results"][-1]:
                choice = Choice(key, result.get("name"), divider="or")
            reasons_choices.append(choice)
            reasons_text[key] = result.get("text")
        picklist_choices = len(reasons_choices) > 0
        if include_other and picklist_choices:
            reasons_text["other"] = ""
            reasons_choices.append(Choice("other", "Other"))
        return reasons_choices, reasons_text


class GiveApprovalAdviceForm(PicklistAdviceForm):
    DOCUMENT_TITLE = "Recommend approval for this case"
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
        super().__init__(*args, **kwargs)
        # this follows the same pattern as denial_reasons.
        approval_choices, approval_text = self._picklist_to_choices(approval_reason)
        self.approval_text = approval_text

        proviso_choices, proviso_text = self._picklist_to_choices(proviso)
        self.proviso_text = proviso_text

        footnote_details_choices, footnote_text = self._picklist_to_choices(footnote_details)
        self.footnote_text = footnote_text

        self.fields["approval_radios"].choices = approval_choices
        self.fields["proviso_radios"].choices = proviso_choices
        self.fields["footnote_details_radios"].choices = footnote_details_choices

        self.helper = FormHelper()
        self.helper.layout = Layout(
            RadioTextArea("approval_radios", "approval_reasons", self.approval_text),
            ExpandingFieldset(
                RadioTextArea("proviso_radios", "proviso", self.proviso_text),
                "instructions_to_exporter",
                RadioTextArea("footnote_details_radios", "footnote_details", self.footnote_text),
                legend="Add a licence condition, instruction to exporter or footnote",
                summary_css_class="supplemental-approval-fields",
            ),
            Submit("submit", "Submit recommendation"),
        )


class FCDOApprovalAdviceForm(GiveApprovalAdviceForm):
    def __init__(self, countries, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["countries"] = forms.MultipleChoiceField(
            choices=countries.items(),
            widget=GridmultipleSelect(),
            label="Select countries for which you want to give advice",
            error_messages={"required": "Select the destinations you want to make recommendations for"},
        )
        parent_layout = self.helper.layout
        self.helper = FormHelper()
        self.helper.layout = Layout(
            "countries",
            parent_layout,
        )
