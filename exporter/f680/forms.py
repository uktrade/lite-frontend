from django import forms
from crispy_forms_gds.layout import HTML

from core.common.forms import BaseForm, FieldsetForm, TextChoice
from core.forms.layouts import ConditionalCheckboxes, ConditionalCheckboxesQuestion
from django.db.models import TextChoices
from django.template.loader import render_to_string


class ApplicationNameForm(BaseForm):
    class Layout:
        TITLE = "Name of the application"
        TITLE_AS_LABEL_FOR = "name"
        SUBMIT_BUTTON_TEXT = "Continue"

    name = forms.CharField(
        label="",
        help_text="Give the application a reference name so you can refer back to it when needed",
    )

    def get_layout_fields(self):
        return ("name",)


class ApplicationSubmissionForm(BaseForm):
    class Layout:
        TITLE = ""
        SUBMIT_BUTTON_TEXT = "Submit"

    def get_layout_fields(self):
        return []


class ApprovalTypeForm(FieldsetForm):
    class Layout:
        TITLE = "Select the types of approvals you need"
        TITLE_AS_LABEL_FOR = "approval_choices"
        SUBMIT_BUTTON_TEXT = "Save and continue"

    class ApprovalTypeChoices(TextChoices):
        INITIAL_DISCUSSIONS_OR_PROMOTING = (
            "INITIAL_DISCUSSIONS_OR_PROMOTING",
            "Initial discussions or promoting products",
        )
        DEMO_IN_UK_TO_OVERSEAS = "DEMO_IN_UK_TO_OVERSEAS", "Demonstration in the United Kingdom to overseas customers"
        DEMO_OVERSEAS = "DEMO_OVERSEAS", "Demonstration overseas"
        TRAINING = "TRAINING", "Training"
        THROUGH_LIFE_SUPPORT = "THROUGH_LIFE_SUPPORT", "Through life support"
        SUPPLY = "SUPPLY", "Supply"

    ApprovalTypeChoices = (
        TextChoice(ApprovalTypeChoices.INITIAL_DISCUSSIONS_OR_PROMOTING),
        TextChoice(ApprovalTypeChoices.DEMO_IN_UK_TO_OVERSEAS),
        TextChoice(ApprovalTypeChoices.DEMO_OVERSEAS),
        TextChoice(ApprovalTypeChoices.TRAINING),
        TextChoice(ApprovalTypeChoices.THROUGH_LIFE_SUPPORT),
        TextChoice(ApprovalTypeChoices.SUPPLY),
    )

    approval_choices = forms.MultipleChoiceField(
        choices=ApprovalTypeChoices,
        error_messages={
            "required": 'Select an approval choice"',
        },
        widget=forms.CheckboxSelectMultiple(),
    )

    demonstration_in_uk_text = forms.MultipleChoiceField(
        label="Explain what you are demonstrating and why",
        choices=(),  # set in __init__
        required=False,
        # setting id for javascript to use
        widget=forms.SelectMultiple(
            attrs={
                "id": "demonstration_in_uk_text",
                "data-module": "multi-select",
            }
        ),
    )

    demonstration_overseas_text = forms.MultipleChoiceField(
        label="Explain what you are demonstrating and why",
        choices=(),  # set in __init__
        required=False,
        # setting id for javascript to use
        widget=forms.SelectMultiple(
            attrs={
                "id": "demonstration_text",
                "data-module": "multi-select",
            }
        ),
    )

    def get_layout_fields(self):
        return (
            ConditionalCheckboxes(
                "approval_choices",
                ConditionalCheckboxesQuestion(
                    "Initial discussions or promoting products",
                ),
                ConditionalCheckboxesQuestion(
                    "Demonstration in the United Kingdom to overseas customers",
                    "demonstration_in_uk_text",
                ),
                ConditionalCheckboxesQuestion(
                    "Demonstration overseas",
                    "demonstration_overseas_text",
                ),
                ConditionalCheckboxesQuestion(
                    "Training",
                ),
                ConditionalCheckboxesQuestion(
                    "Through life support",
                ),
                ConditionalCheckboxesQuestion(
                    "Supply",
                ),
            ),
            HTML.details(
                "Help with exceptional circumstances",
                render_to_string("applications/forms/help_with_approval_type.html"),
            ),
        )
