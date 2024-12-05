from django import forms

from core.common.forms import BaseForm


class PicklistApprovalAdviceEditForm(BaseForm):
    class Layout:
        TITLE = "Add licence conditions, instructions to exporter or footnotes (optional)"

    proviso = forms.CharField(
        widget=forms.Textarea(attrs={"rows": 30, "class": "govuk-!-margin-top-4"}),
        label="",
        required=False,
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def get_layout_fields(self):
        return ("proviso",)
