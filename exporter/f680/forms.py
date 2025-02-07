from django import forms
from crispy_forms_gds.choices import Choice

from core.common.forms import BaseForm, FieldsetForm
from core.forms.layouts import ConditionalCheckboxes, ConditionalCheckboxesQuestion


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

    choice_list = [
        "initial discussions or promoting products",
        "demonstration in the United Kingdom to overseas customers",
        "demonstration overseas",
        "training",
        "through life support",
        "supply",
    ]

    def _get_choices(self, choice_list):
        approval_choices = []
        approval_text = {}

        approval_list = choice_list
        breakpoint()
        for result in approval_list:
            key = "_".join(result.lower().split())
            choice = Choice(key, result)
            if result == approval_list[-1]:
                choice = Choice(key, result, divider="or")
            approval_choices.append(choice)
            approval_text[key] = result.capitalize()
        breakpoint()
        return approval_choices, approval_text

    approval_choices = forms.MultipleChoiceField(
        label="",
        required=False,
        widget=forms.CheckboxSelectMultiple,
        choices=(),
    )

    def __init__(self, *args, **kwargs):

        approval_choices, approval_text = self._get_choices(self.choice_list)

        self.conditional_checkbox_choices = (
            ConditionalCheckboxesQuestion(choices.label, choices.value) for choices in approval_choices
        )

        super().__init__(*args, **kwargs)

        self.fields["approval_choices"].choices = approval_choices
        for choices in approval_choices:
            self.fields[choices.value] = forms.CharField(
                widget=forms.Textarea(attrs={"rows": 3}),
                label="Description",
                required=False,
                initial=approval_text[choices.value],
            )

    def get_layout_fields(self):

        return (ConditionalCheckboxes("approval_choices", *self.conditional_checkbox_choices),)
