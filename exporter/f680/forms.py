from django import forms
from crispy_forms_gds.layout import HTML
from crispy_forms_gds.choices import Choice

from core.common.forms import BaseForm, TextChoice
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


class ApprovalTypeForm(BaseForm):
    class Layout:
        TITLE = "Select the types of approvals you need"
        TITLE_AS_LABEL_FOR = "approval_choices"
        SUBMIT_BUTTON_TEXT = "Save and continue"

    class ApprovalTypeChoices(TextChoices):
        INITIAL_DISCUSSIONS_OR_PROMOTING = (
            "INITIAL_DISCUSSIONS_OR_PROMOTING",
            "Initial discussions or promoting products",
        )
        demonstration_in_uk = (
            "demonstration_in_uk",
            "Demonstration in the United Kingdom to overseas customers",
        )
        demonstration_overseas = "demonstration_overseas", "Demonstration overseas"
        TRAINING = "TRAINING", "Training"
        THROUGH_LIFE_SUPPORT = "THROUGH_LIFE_SUPPORT", "Through life support"
        SUPPLY = "SUPPLY", "Supply"

    ApprovalTypeChoices = (
        TextChoice(ApprovalTypeChoices.INITIAL_DISCUSSIONS_OR_PROMOTING),
        TextChoice(ApprovalTypeChoices.demonstration_in_uk),
        TextChoice(ApprovalTypeChoices.demonstration_overseas),
        TextChoice(ApprovalTypeChoices.TRAINING),
        TextChoice(ApprovalTypeChoices.THROUGH_LIFE_SUPPORT),
        TextChoice(ApprovalTypeChoices.SUPPLY),
    )

    approval_choices = forms.MultipleChoiceField(
        choices=(),
        error_messages={
            "required": 'Select an approval choice"',
        },
        widget=forms.CheckboxSelectMultiple(),
    )

    demonstration_in_uk = forms.CharField(
        label="Explain what you are demonstrating and why",
        widget=forms.Textarea(attrs={"rows": 5}),
    )

    demonstration_overseas = forms.CharField(
        label="Explain what you are demonstrating and why",
        widget=forms.Textarea(attrs={"rows": 5}),
    )

    def __init__(self, *args, **kwargs):
        self.conditional_checkbox_choices = (
            ConditionalCheckboxesQuestion(choices.label, choices.value) for choices in self.ApprovalTypeChoices
        )
        super().__init__(*args, **kwargs)
        self.fields["approval_choices"].choices = self.ApprovalTypeChoices

    def get_layout_fields(self):
        return (
            ConditionalCheckboxes("approval_choices", *self.conditional_checkbox_choices),
            HTML.details(
                "Help with exceptional circumstances",
                render_to_string("applications/forms/help_with_approval_type.html"),
            ),
        )
