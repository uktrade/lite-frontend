from django import forms

from core.common.forms import BaseForm


class ChangeSubStatusForm(BaseForm):
    class Layout:
        TITLE = "Change case sub status"
        SUBMIT_BUTTON_TEXT = "Save"

    sub_status = forms.ChoiceField(
        choices=[
            ("", ""),
        ],  # updated in init
        label="",
        required=False,
    )

    def __init__(self, *args, sub_statuses, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["sub_status"].choices += sub_statuses

    def get_layout_fields(self):
        return ("sub_status",)
