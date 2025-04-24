from django import forms

from crispy_forms_gds.choices import Choice
from crispy_forms_gds.layout import HTML, Submit

from caseworker.f680.recommendation.constants import RecommendationSecurityGrading

from core.common.forms import BaseForm
from core.forms.layouts import (
    ConditionalCheckboxes,
    ConditionalCheckboxesQuestion,
    ConditionalRadios,
    ConditionalRadiosQuestion,
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


class PicklistRefusalForm(forms.Form):
    def _picklist_to_choices(self, picklist_data):
        reasons_choices = []
        reasons_text = {}

        for result in picklist_data:
            key = "_".join(result.get("display_value").lower().split())
            choice = Choice(key, result.get("display_value"))
            reasons_choices.append(choice)
            reasons_text[key] = result.get("description")
        return reasons_choices, reasons_text


class EntitySelectionAndDecisionForm(BaseForm):
    class Layout:
        TITLE = "Select entities and decision"

    CHOICES = [
        ("approve", "Approve"),
        ("refuse", "Refuse"),
    ]

    release_requests = forms.MultipleChoiceField(
        label="",
        widget=forms.CheckboxSelectMultiple,
        choices=(),
        error_messages={"required": "Select entities to add recommendations"},
    )
    recommendation = forms.ChoiceField(
        choices=CHOICES,
        widget=forms.RadioSelect,
        label="Select recommendation type",
        error_messages={"required": "Select if you approve or refuse"},
    )

    def __init__(self, release_requests, *args, **kwargs):
        release_requests_choices = [
            Choice(rr["id"], f'{rr["recipient"]["name"]}, {rr["recipient"]["country"]["name"]}')
            for rr in release_requests
        ]

        super().__init__(*args, **kwargs)

        self.fields["release_requests"].choices = release_requests_choices

    def get_layout_fields(self):
        return ("release_requests", "recommendation")


class BasicRecommendationForm(BaseForm):
    class Layout:
        TITLE = "Add conditions"

    security_grading = forms.ChoiceField(
        choices="",
        label="Select security classification",
        widget=forms.RadioSelect,
        error_messages={"required": "Select the security classification"},
    )
    security_grading_other = forms.CharField(label="Enter the security classification", required=False)

    conditions = forms.CharField(
        widget=forms.Textarea(attrs={"rows": 7}),
        label="Provisos",
        required=False,
    )

    def __init__(self, *args, **kwargs):
        self.conditional_radio_choices = [
            (
                ConditionalRadiosQuestion(choice.label, "security_grading_other")
                if choice.value == "other"
                else choice.label
            )
            for choice in RecommendationSecurityGrading.choices
        ]

        super().__init__(*args, **kwargs)

        self.fields["security_grading"].choices = RecommendationSecurityGrading.choices

    def get_layout_fields(self):
        return (
            ConditionalRadios("security_grading", *self.conditional_radio_choices),
            "conditions",
        )


class BasicRecommendationRefusalReasonsForm(BaseForm):
    class Layout:
        TITLE = "Add refusal reasons"

    refusal_reasons = forms.CharField(
        widget=forms.Textarea(attrs={"rows": 7}),
        label="Refusal reasons",
        required=False,
    )

    def get_layout_fields(self):
        return ("refusal_reasons",)


class EntityConditionsForm(BasicRecommendationForm, PicklistAdviceForm):
    class Layout:
        TITLE = "Add conditions for entities"

    conditions = forms.MultipleChoiceField(
        label="Provisos",
        required=False,
        widget=forms.CheckboxSelectMultiple,
        choices=(),
    )

    def __init__(self, conditions, *args, **kwargs):
        conditions_choices, conditions_text = self._picklist_to_choices(conditions)
        self.conditional_checkbox_choices = (
            ConditionalCheckboxesQuestion(choices.label, choices.value) for choices in conditions_choices
        )

        super().__init__(*args, **kwargs)

        self.fields["conditions"].choices = conditions_choices
        for choices in conditions_choices:
            self.fields[choices.value] = forms.CharField(
                widget=forms.Textarea(attrs={"rows": 10}),
                label="Description",
                required=False,
                initial=conditions_text[choices.value],
            )

    def clean(self):
        cleaned_data = super().clean()
        return {
            "security_grading": cleaned_data.get("security_grading", ""),
            "security_grading_other": cleaned_data.get("security_grading_other", ""),
            "conditions": "\n\n--------\n".join([cleaned_data[selected] for selected in cleaned_data["conditions"]]),
        }

    def get_layout_fields(self):
        return (
            ConditionalRadios("security_grading", *self.conditional_radio_choices),
            ConditionalCheckboxes("conditions", *self.conditional_checkbox_choices),
        )


class EntityRefusalReasonsForm(BaseForm, PicklistRefusalForm):
    class Layout:
        TITLE = "Add refusal reasons for entities"

    refusal_reasons = forms.MultipleChoiceField(
        label="Refusal reasons",
        widget=forms.CheckboxSelectMultiple,
        choices=(),
        error_messages={"required": "Select refusal reasons"},
    )

    def clean(self):
        cleaned_data = super().clean()
        return {
            "refusal_reasons": "\n\n--------\n".join(
                [cleaned_data[selected] for selected in cleaned_data.get("refusal_reasons", [])]
            ),
        }

    def __init__(self, refusal_reasons, *args, **kwargs):
        refusal_reasons_choices, refusal_reasons_text = self._picklist_to_choices(refusal_reasons)

        self.conditional_checkbox_choices = (
            ConditionalCheckboxesQuestion(choices.label, choices.value) for choices in refusal_reasons_choices
        )

        super().__init__(*args, **kwargs)

        self.fields["refusal_reasons"].choices = refusal_reasons_choices
        for choices in refusal_reasons_choices:
            self.fields[choices.value] = forms.CharField(
                widget=forms.Textarea(attrs={"rows": 3}),
                label="Description",
                required=False,
                initial=f"Criteria {choices.value}: {refusal_reasons_text[choices.value]}",
            )

    def get_layout_fields(self):
        return (ConditionalCheckboxes("refusal_reasons", *self.conditional_checkbox_choices),)


class ClearRecommendationForm(BaseForm):
    class Layout:
        TITLE = ""

    def get_layout_fields(self):
        return []

    def get_layout_actions(self):
        return [
            Submit("submit", "Confirm"),
            HTML(
                """<a role="button" draggable="false" class="govuk-button govuk-button--secondary"
                    href="{% url 'cases:f680:view_my_recommendation' queue_pk case.id %}">
                    Cancel
                </a>"""
            ),
        ]
