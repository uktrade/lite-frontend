from crispy_forms_gds.layout import Button, HTML
from django import forms
from django.template.loader import render_to_string

from core.common.forms import BaseForm


class DocumentGenerationForm(BaseForm):

    class Layout:
        TITLE = "Generate decision documents"
        SUBMIT_BUTTON_TEXT = "Save and publish to exporter"

    def __init__(self, approval_templates, *args, **kwargs):
        self.approval_templates = approval_templates
        super().__init__(*args, **kwargs)

    def get_layout_fields(self):
        document_table = HTML(
            render_to_string("f680/document/document-generation.html", {"approval_templates": self.approval_templates})
        )
        return (document_table,)

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
