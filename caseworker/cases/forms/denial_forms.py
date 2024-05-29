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

from core.forms.layouts import RenderTemplate


class DenialSearchForm(forms.Form):

    search_string = forms.CharField(
        widget=forms.Textarea(attrs={"rows": "1"}),
        label="",
        required=False,
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()

        self.helper.layout = Layout(
            HTML.p("Or manually edit the query."),
            Field("search_string"),
            Div(
                Button("submit", "Search"),
            ),
            RenderTemplate("external_data/query-error.html"),
            HTML.details(
                "Help with building queries",
                render_to_string("external_data/help-build-query.html"),
            ),
        )
