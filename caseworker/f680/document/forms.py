from crispy_forms_gds.layout import Button
from django import forms

from core.common.forms import BaseForm


class DocumentGenerationForm(BaseForm):

    class Layout:
        TITLE = ""
        SUBMIT_BUTTON_TEXT = "Save and publish to exporter"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def get_layout_fields(self):
        return ()

    def get_layout_actions(self):
        # Prevent the standard submit button being shown
        return []


class GenerateDocumentForm(BaseForm):
    class Layout:
        TITLE = "Generate document"

    text = forms.CharField(
        label="Customisation text",
        widget=forms.Textarea(attrs={"rows": 3}),
        required=False,
    )

    def get_layout_fields(self):
        return (
            "text",
            Button(name="preview", value="Preview"),
            Button(name="generate", value="Generate"),
        )

    def get_layout_actions(self):
        # Prevent the standard submit button being shown
        return []
