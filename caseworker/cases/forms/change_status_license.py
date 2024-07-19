from django import forms

from core.common.forms import BaseForm


class ChangeLicenseStatusForm(BaseForm):
    class Layout:
        TITLE = "Change license status"
        SUBMIT_BUTTON_TEXT = "Save"

    status = forms.ChoiceField(
        choices=[],
        label="",
        error_messages={"required": "Select a status to save"},
    )

    def get_layout_fields(self):
        return ("status",)

    def __init__(self, *args, statuses, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["status"].choices += statuses
