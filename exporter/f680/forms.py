from django import forms
from django.db.models import TextChoices
from django.template.loader import render_to_string
from crispy_forms_gds.layout import HTML

from core.common.forms import BaseForm, TextChoice
from core.forms.layouts import F680ConditionalCheckboxes, F680ConditionalCheckboxesQuestion


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
            "initial_discussion_or_promoting",
            "Initial discussions or promoting products",
        )
        DEMONSTRATION_IN_THE_UK = (
            "demonstration_in_uk",
            "Demonstration in the United Kingdom to overseas customers",
        )
        DEMONSTRATION_OVERSEAS = "demonstration_overseas", "Demonstration overseas"
        TRAINING = "training", "Training"
        THROUGH_LIFE_SUPPORT = "through_life_support", "Through life support"
        SUPPLY = "supply", "Supply"

    ApprovalTypeChoices = (
        TextChoice(ApprovalTypeChoices.INITIAL_DISCUSSIONS_OR_PROMOTING),
        TextChoice(ApprovalTypeChoices.DEMONSTRATION_IN_THE_UK),
        TextChoice(ApprovalTypeChoices.DEMONSTRATION_OVERSEAS),
        TextChoice(ApprovalTypeChoices.TRAINING),
        TextChoice(ApprovalTypeChoices.THROUGH_LIFE_SUPPORT),
        TextChoice(ApprovalTypeChoices.SUPPLY),
    )

    approval_choices = forms.MultipleChoiceField(
        choices=(),
        error_messages={
            "required": "Select an approval choice",
        },
        widget=forms.CheckboxSelectMultiple(),
    )

    demonstration_in_uk = forms.CharField(
        label="Explain what you are demonstrating and why",
        widget=forms.Textarea(attrs={"rows": 5}),
        required=False,
    )

    demonstration_overseas = forms.CharField(
        label="Explain what you are demonstrating and why",
        widget=forms.Textarea(attrs={"rows": 5}),
        required=False,
    )

    def __init__(self, *args, **kwargs):
        self.conditional_checkbox_choices = (
            F680ConditionalCheckboxesQuestion(choices.label, choices.value) for choices in self.ApprovalTypeChoices
        )
        super().__init__(*args, **kwargs)
        self.fields["approval_choices"].choices = self.ApprovalTypeChoices

    def get_layout_fields(self):
        return (
            F680ConditionalCheckboxes("approval_choices", *self.conditional_checkbox_choices),
            HTML.details(
                "Help with exceptional circumstances",
                render_to_string("f680/forms/help_with_approval_type.html"),
            ),
        )
