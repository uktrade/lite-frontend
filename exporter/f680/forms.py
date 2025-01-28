from django import forms

from core.common.forms import BaseForm


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


class ApplicationPreviousApplicationForm(BaseForm):
    class Layout:
        TITLE = "Have you made a previous application?"
        TITLE_AS_LABEL_FOR = "previous_application"
        SUBMIT_BUTTON_TEXT = "Save"

    previous_application = forms.ChoiceField(
        label="",
        help_text="Some help text",
        widget=forms.RadioSelect,
        choices=(
            ("Yes", "Yes"),
            ("No", "No"),
        ),
    )

    def get_layout_fields(self):
        return ("previous_application",)
