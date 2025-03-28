from core.common.forms import BaseForm
from django import forms


class NewECJUQueryForm(BaseForm):
    class Layout:
        TITLE = "New standard query"
        SUBMIT_BUTTON_TEXT = "Send"

    question = forms.CharField(
        help_text="Enter a full description. If your question is related to goods, then include technical details if appropriate.",
        label=False,
        widget=forms.Textarea(attrs={"rows": "5"}),
        max_length=5000,
    )

    def get_layout_fields(self):
        return ("question",)
