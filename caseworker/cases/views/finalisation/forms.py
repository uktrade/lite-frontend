from django import forms
from crispy_forms_gds.helper import FormHelper
from crispy_forms_gds.layout import Layout, Submit


class SelectInformLetterTemplateForm(forms.Form):
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


class LetterEditTextForm(forms.Form):
    text = forms.CharField(
        widget=forms.Textarea(attrs={"rows": "30"}),
        error_messages={"required": "Edit text is Required"},
        label="Add a case note",
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            "text",
            Submit("submit", "Preview"),
        )
