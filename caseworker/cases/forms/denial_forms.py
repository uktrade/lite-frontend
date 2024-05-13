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
    consignee = forms.CharField(widget=forms.HiddenInput(), required=False)
    ultimate_end_user = forms.CharField(widget=forms.HiddenInput(), required=False)
    third_parties = forms.CharField(widget=forms.HiddenInput(), required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = "GET"
        self.helper.layout = Layout(
            Field("search_string"),
            Div(
                Button.secondary("submit", "Search"),
            ),
        )
        for party_type in ["end_user", "consignee", "ultimate_end_user", "third_parties"]:
            if party_type in kwargs["initial"] and kwargs["initial"][party_type]:
                self.helper.layout.append(Field(party_type))
