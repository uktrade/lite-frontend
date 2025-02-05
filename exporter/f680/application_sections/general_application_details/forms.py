from django import forms

from core.common.forms import BaseForm


class ApplicationNameForm(BaseForm):
    class Layout:
        TITLE = "Name the application"
        TITLE_AS_LABEL_FOR = "name"
        SUBMIT_BUTTON_TEXT = "Continue"

    name = forms.CharField(
        label="",
        help_text="Give the application a reference name so you can refer back to it when needed",
    )

    def get_layout_fields(self):
        return ("name",)


class ExceptionalCircumstancesForm(BaseForm):
    class Layout:
        TITLE = "Do you have exceptional circumstances that mean you need F680 approval in less than 30 days?"
        TITLE_AS_LABEL_FOR = "is_exceptional_circumstances"
        SUBMIT_BUTTON_TEXT = "Continue"

    is_exceptional_circumstances = forms.TypedChoiceField(
        choices=(
            (True, "Yes"),
            (False, "No"),
        ),
        label="",
        widget=forms.RadioSelect,
    )

    def get_layout_fields(self):
        return ("is_exceptional_circumstances",)
