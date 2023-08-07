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

    TEMPLATE_INFO_WMD = "WMD", "Weapons of mass destruction (WMD)"
    TEMPLATE_INFO_MAM = "MAM", "Military and military"
    TEMPLATE_INFO_MWMD = "MWMD", "Military and weapons of mass destruction (WMD)"

    INFORM_LETTER_CHOICES = [TEMPLATE_INFO_WMD, TEMPLATE_INFO_MAM, TEMPLATE_INFO_MWMD]

    select_template = forms.ChoiceField(
        choices=INFORM_LETTER_CHOICES,
        widget=forms.RadioSelect,
        error_messages={
            "required": "please select a template",
        },
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # select_template_choices = {"hello": "Hello"}

        ##elect_template_field = self.fields["select_template"]
        # select_template_field.choices = [("", "Select"), ("key1", "display1"), ("key2", "display2")]

    def get_layout_fields(self):
        return (
            "select_template",
            Submit("submit", "Submit recommendation"),
        )
