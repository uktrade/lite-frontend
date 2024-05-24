from crispy_forms_gds.helper import FormHelper
from crispy_forms_gds.layout import (
    Div,
    Field,
    Layout,
    Button,
    HTML,
)

from django import forms
from django.template.loader import render_to_string


class DenialSearchForm(forms.Form):

    search_string = forms.CharField(
        widget=forms.Textarea(attrs={"rows": "2"}),
        label="",
        required=False,
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            HTML.p("Or manually edit the query."),
            HTML.details(
                "To build your query",
                render_to_string("external_data/help-build-query.html"),
            ),
            Field("search_string"),
            Div(
                Button.secondary("submit", "Search"),
            ),
        )
