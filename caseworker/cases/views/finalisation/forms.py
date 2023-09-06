from django import forms
from core.common.forms import BaseForm


class SelectInformLetterTemplateForm(BaseForm):
    class Layout:
        TITLE = "Select a template"

    select_template = forms.ChoiceField(
        label="",
        choices=(),
        widget=forms.RadioSelect,
        error_messages={
            "required": "please select a template",
        },
    )

    def __init__(self, *args, **kwargs):
        inform_pargraphs = kwargs.pop("inform_paragraphs")
        super().__init__(*args, **kwargs)

        self.fields["select_template"].choices = inform_pargraphs

    def get_layout_fields(self):
        return ("select_template",)


class LetterEditTextForm(BaseForm):
    class Layout:
        TITLE = "Edit inform letter header"
        SUBMIT_BUTTON_TEXT = "Preview"

    text = forms.CharField(
        widget=forms.Textarea(attrs={"rows": "30"}),
        error_messages={"required": "Edit text is Required"},
        label="",
    )

    def get_layout_fields(self):
        return ("text",)
