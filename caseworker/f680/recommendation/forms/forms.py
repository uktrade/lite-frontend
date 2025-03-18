from django import forms

from crispy_forms_gds.choices import Choice
from crispy_forms_gds.helper import FormHelper
from crispy_forms_gds.layout import HTML, Submit

from core.common.forms import BaseForm
from core.forms.layouts import (
    ConditionalCheckboxes,
    ConditionalCheckboxesQuestion,
    ConditionalRadios,
    ConditionalRadiosQuestion,
    RadioTextArea,
)


class SelectRecommendationTypeForm(forms.Form):
    CHOICES = [
        ("approve_all", "Approve all"),
    ]

    recommendation = forms.ChoiceField(
        choices=CHOICES,
        widget=forms.RadioSelect,
        label="",
        error_messages={"required": "Select if you approve all or refuse all"},
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.add_input(Submit("submit", "Continue"))


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


class RecommendAnApprovalForm(PicklistAdviceForm, BaseForm):
    class Layout:
        TITLE = "Recommend an approval"

    approval_reasons = forms.CharField(
        widget=forms.Textarea(attrs={"rows": 7, "class": "govuk-!-margin-top-4", "name": "approval_reasons"}),
        label="",
        error_messages={"required": "Enter a reason for approving"},
    )
    approval_radios = forms.ChoiceField(
        label="What is your reason for approving?",
        required=False,
        widget=forms.RadioSelect,
        choices=(),
    )
    add_licence_conditions = forms.BooleanField(
        label="Add licence conditions, instructions to exporter or footnotes (optional)",
        required=False,
    )

    def __init__(self, *args, **kwargs):
        approval_reason = kwargs.pop("approval_reason")
        # this follows the same pattern as denial_reasons.
        approval_choices, approval_text = self._picklist_to_choices(approval_reason)
        self.approval_text = approval_text
        super().__init__(*args, **kwargs)
        self.fields["approval_radios"].choices = approval_choices

    def get_layout_fields(self):
        return (
            RadioTextArea("approval_radios", "approval_reasons", self.approval_text),
            "add_licence_conditions",
        )


class SimpleLicenceConditionsForm(BaseForm):
    class Layout:
        TITLE = "Add licence conditions (optional)"

    proviso = forms.CharField(
        widget=forms.Textarea(attrs={"rows": 7}),
        label="Licence condition",
        required=False,
    )

    def get_layout_fields(self):
        return ("proviso",)


class BaseRecommendationForm(BaseForm):
    class Layout:
        TITLE = ""

    CHOICES = [
        ("approve", "Approve"),
        ("refuse", "Refuse"),
    ]
    security_release_choices = (
        Choice("official", "Official"),
        Choice("official-sensitive", "Official-Sensitive"),
        Choice("secret", "Secret"),
        Choice("top-secret", "Top Secret", divider="Or"),
        Choice("other", "Other"),
    )
    recommendation = forms.ChoiceField(
        choices=CHOICES,
        widget=forms.RadioSelect,
        label="Select recommendation type",
        error_messages={"required": "Select if you approve or refuse"},
    )
    security_grading = forms.ChoiceField(
        choices="",
        label="Select security classification",
        widget=forms.RadioSelect,
    )
    security_grading_other = forms.CharField(label="Enter the security classification", required=False)
    conditions = forms.CharField(
        widget=forms.Textarea(attrs={"rows": 7}),
        label="Provisos",
        required=False,
    )

    def __init__(self, release_request, *args, **kwargs):
        self.conditional_radio_choices = [
            (
                ConditionalRadiosQuestion(choice.label, "security_grading_other")
                if choice.value == "other"
                else choice.label
            )
            for choice in self.security_release_choices
        ]

        self.release_request = release_request
        super().__init__(*args, **kwargs)

        self.fields["security_grading"].choices = self.security_release_choices

    def get_layout_fields(self):
        return (
            HTML.h1(f"Add recommendation for {self.release_request['recipient']['name']}"),
            "recommendation",
            ConditionalRadios("security_grading", *self.conditional_radio_choices),
            "conditions",
        )


class EntityConditionsRecommendationForm(PicklistAdviceForm, BaseRecommendationForm):
    conditions = forms.MultipleChoiceField(
        label="Provisos",
        required=False,
        widget=forms.CheckboxSelectMultiple,
        choices=(),
    )

    def clean(self):
        cleaned_data = super().clean()
        # only return proviso (text) for selected checkboxes, nothing else matters, join by 2 newlines
        return {
            "type": cleaned_data["recommendation"],
            "security_grading": cleaned_data["security_grading"],
            "security_grading_other": cleaned_data["security_grading_other"],
            "security_release_request": self.release_request["id"],
            "conditions": "\n\n--------\n".join([cleaned_data[selected] for selected in cleaned_data["conditions"]]),
        }

    def __init__(self, *args, **kwargs):
        conditions = kwargs.pop("proviso")

        conditions_choices, conditions_text = self._picklist_to_choices(conditions)

        self.conditional_checkbox_choices = (
            ConditionalCheckboxesQuestion(choices.label, choices.value) for choices in conditions_choices
        )

        super().__init__(*args, **kwargs)

        self.fields["conditions"].choices = conditions_choices
        for choices in conditions_choices:
            self.fields[choices.value] = forms.CharField(
                widget=forms.Textarea(attrs={"rows": 3}),
                label="Description",
                required=False,
                initial=conditions_text[choices.value],
            )

    def get_layout_fields(self):
        return (
            HTML.h1(f"Add recommendation for {self.release_request['recipient']['name']}"),
            "recommendation",
            ConditionalRadios("security_grading", *self.conditional_radio_choices),
            ConditionalCheckboxes("conditions", *self.conditional_checkbox_choices),
        )


class FootnotesApprovalAdviceForm(PicklistAdviceForm, BaseForm):
    class Layout:
        TITLE = "Add instructions to the exporter, or a reporting footnote (optional)"

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
        widget=forms.Textarea(attrs={"rows": 3}),
        label="",
        required=False,
    )

    def __init__(self, *args, **kwargs):
        footnote_details = kwargs.pop("footnote_details")
        footnote_details_choices, footnote_text = self._picklist_to_choices(footnote_details)
        self.footnote_text = footnote_text

        super().__init__(*args, **kwargs)

        self.fields["footnote_details_radios"].choices = footnote_details_choices

    def get_layout_fields(self):
        return (
            "instructions_to_exporter",
            RadioTextArea("footnote_details_radios", "footnote_details", self.footnote_text),
        )
