from django import forms
from crispy_forms_gds.helper import FormHelper
from crispy_forms_gds.layout import Field, Layout, Submit
from crispy_forms_gds.choices import Choice
from core.forms.layouts import RadioTextArea

from crispy_forms_gds.choices import Choice
from django.urls import reverse_lazy
from django.db import models
from core.common.forms import TextChoice, BaseForm


class SelectInformLetterTemplateForm(BaseForm):
    class Layout:
        TITLE = "Select Inform Letter Template"

    select_template = forms.ChoiceField(
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
        return "select_template"


class TemplateTextForm(BaseForm):
    class Layout:
        TITLE = "Edit Text"

    text = forms.CharField(
        widget=forms.Textarea(attrs={"rows": "15"}),
        error_messages={"required": "Edit text is Required"},
        label="Add a case note",
    )

    def __init__(self, *args, **kwargs):
        text = kwargs.pop("text")
        super().__init__(*args, **kwargs)
        self.fields["text"].initial = text

        self.helper = FormHelper()
        self.helper.layout = Layout(
            "text",
            Submit("submit", "Preview"),
        )

    def get_layout_fields(self):
        return "text"
