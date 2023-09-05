from django import forms
from crispy_forms_gds.helper import FormHelper
from crispy_forms_gds.layout import Layout, Submit
from core.common.forms import BaseForm


class SelectInformLetterTemplateForm(BaseForm):
    class Layout:
        TITLE = "Select a template"
        SUBTITLE = "Select a template"

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

        self.helper = FormHelper()
        self.helper.layout = Layout(
            "select_template",
            Submit("submit", "Continue"),
        )

    def get_layout_fields(self):
        return ("select_template",)


class LetterEditTextForm(BaseForm):
    class Layout:
        TITLE = "Edit inform letter header"
        SUBTITLE = "Edit inform letter header"

    text = forms.CharField(
        widget=forms.Textarea(attrs={"rows": "30"}),
        error_messages={"required": "Edit text is Required"},
        label="",
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            "text",
            Submit("submit", "Preview"),
        )
