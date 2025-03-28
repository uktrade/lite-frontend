from django import forms

from crispy_forms_gds.choices import Choice
from crispy_forms_gds.layout import HTML, Submit

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
        error_messages={"required": "Select the security classification"},
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

    def clean(self):
        cleaned_data = super().clean()

        return {
            **cleaned_data,
            "security_release_request": self.release_request["id"],
        }

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
        return {
            "recommendation": cleaned_data.get("recommendation", ""),
            "security_grading": cleaned_data.get("security_grading", ""),
            "security_grading_other": cleaned_data.get("security_grading_other", ""),
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
