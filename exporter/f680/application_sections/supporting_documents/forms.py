from core.common.forms import BaseForm
from django import forms

from core.file_handler import validate_mime_type
from exporter.core.constants import FileUploadFileTypes
from exporter.core.forms import PotentiallyUnsafeClearableFileInput
from django.template.loader import render_to_string


class F680AttachSupportingDocument(BaseForm):
    class Layout:
        TITLE = "Attach a supporting document"
        SUBTITLE = render_to_string("f680/forms/subtitle_add_supporting_document.html")

    file = forms.FileField(
        label=FileUploadFileTypes.UPLOAD_GUIDANCE_TEXT,
        error_messages={
            "required": "Select a supporting document",
        },
        validators=[
            validate_mime_type,
        ],
        widget=PotentiallyUnsafeClearableFileInput,
    )

    description = forms.CharField(
        widget=forms.Textarea(attrs={"rows": "5"}),
        label="Description (optional)",
        required=False,
    )

    def get_layout_fields(self):
        return (
            "file",
            "description",
        )
