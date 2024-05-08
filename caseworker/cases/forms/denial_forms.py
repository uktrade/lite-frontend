from crispy_forms_gds.helper import FormHelper
from crispy_forms_gds.layout import (
    Div,
    Field,
    Layout,
    Button,
)

from django import forms


class DenialSearchForm(forms.Form):
    page_size = 25

    search_string = forms.CharField(
        widget=forms.Textarea(attrs={"rows": "2"}),
        label="Or manually edit the query.",
        required=False,
    )
    page = forms.IntegerField(widget=forms.HiddenInput(), required=False, initial=1)
    end_user = forms.CharField(widget=forms.HiddenInput(), required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_method = "GET"
        self.helper.layout = Layout(
            Field("search_string"),
            Field("end_user"),
            Div(
                Button.secondary("submit", "Search"),
            ),
        )
