from django import forms

from crispy_forms_gds.choices import Choice
from crispy_forms_gds.layout import HTML, Submit

from core.common.forms import BaseForm
from core.forms.layouts import (
    ConditionalCheckboxes,
    ConditionalCheckboxesQuestion,
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


class EntitySelectionForm(BaseForm):
    class Layout:
        TITLE = "Select entities"

    release_requests = forms.MultipleChoiceField(
        label="",
        widget=forms.CheckboxSelectMultiple,
        choices=(),
        error_messages={"required": "Select entities to add recommendations"},
    )

    def __init__(self, release_requests, *args, **kwargs):
        release_requests_choices = [
            Choice(rr["id"], f'{rr["recipient"]["name"]}, {rr["recipient"]["country"]["name"]}')
            for rr in release_requests
        ]

        super().__init__(*args, **kwargs)

        self.fields["release_requests"].choices = release_requests_choices

    def get_layout_fields(self):
        return ("release_requests",)


class BaseRecommendationForm(BaseForm):
    class Layout:
        TITLE = "Add recommendation"

    CHOICES = [
        ("approve", "Approve"),
        ("refuse", "Refuse"),
    ]
    recommendation = forms.ChoiceField(
        choices=CHOICES,
        widget=forms.RadioSelect,
        label="Select recommendation type",
        error_messages={"required": "Select if you approve or refuse"},
    )
    conditions = forms.CharField(
        widget=forms.Textarea(attrs={"rows": 7}),
        label="Provisos",
        required=False,
    )

    def get_layout_fields(self):
        return (
            "recommendation",
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
            "conditions": "\n\n--------\n".join([cleaned_data[selected] for selected in cleaned_data["conditions"]]),
        }

    def __init__(self, conditions, *args, **kwargs):
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
            "recommendation",
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
