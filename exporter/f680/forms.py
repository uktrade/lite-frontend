from django import forms
from crispy_forms_gds.layout import HTML

from core.common.forms import BaseForm
from core.forms.layouts import ConditionalCheckboxes, ConditionalCheckboxesQuestion
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


class ApprovalTypeForm(BaseForm):
    class Layout:
        TITLE = "Select the types of approvals you need"
        TITLE_AS_LABEL_FOR = "approval_choices"
        SUBMIT_BUTTON_TEXT = "Save and continue"

    APPROVAL_CHOICES = [
        ("INITIAL_DISCUSSIONS_OR_PROMOTING", "Initial discussions or promoting products"),
        ("DEMO_IN_UK_TO_OVERSEAS", "Demonstration in the United Kingdom to overseas customers"),
        ("DEMO_OVERSEAS", "Demonstration overseas"),
        ("TRAINING", "Training"),
        ("THROUGH_LIFE_SUPPORT", "Through life support"),
        ("SUPPLY", "Supply"),
    ]
    approval_choices = forms.MultipleChoiceField(
        choices=APPROVAL_CHOICES,
        error_messages={
            "required": 'Select an approval choice"',
        },
        widget=forms.CheckboxSelectMultiple(),
    )

    demonstration_in_uk_text = forms.CharField(
        label="Explain what you are demonstrating and why",
        widget=forms.Textarea(attrs={"rows": 5}),
    )

    demonstration_overseas_text = forms.CharField(
        label="Explain what you are demonstrating and why",
        widget=forms.Textarea(attrs={"rows": 5}),
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
