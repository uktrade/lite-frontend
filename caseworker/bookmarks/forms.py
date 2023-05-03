from crispy_forms.layout import Field
from crispy_forms_gds.helper import FormHelper
from crispy_forms_gds.layout import Layout, Submit, Fieldset, Div
from django import forms
from django.forms.widgets import HiddenInput


class AddBookmark(forms.Form):
    return_to = forms.CharField(widget=HiddenInput)
    name = forms.CharField(
        label="Name",
        required=True,
    )
    description = forms.CharField(
        label="Description",
        required=False,
    )

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Fieldset(
                "Save current filter",
                "return_to",
                Field("name", wrapper_class="bookmark-field"),
                Field("description", wrapper_class="bookmark-field"),
                Div(Submit("submit", "Save current filter")),
            )
        )


class DeleteBookmark(forms.Form):
    id = forms.CharField(widget=HiddenInput)
    return_to = forms.CharField(widget=HiddenInput)
    name = forms.CharField(required=False)
    submit = forms.CharField()
