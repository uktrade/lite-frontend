from crispy_forms_gds.layout import HTML

from core.common.forms import BaseForm
from django.template.loader import render_to_string


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
