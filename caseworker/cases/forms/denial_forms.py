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
        widget=forms.Textarea(attrs={"rows": "1"}),
        label="",
        required=False,
    )

    def query_error(self):
        return HTML(
            """
                    {% if search_results.errors.search == "Invalid search string" %}
                    <div class="query-search__error">
                        <div class="govuk-error-summary" data-module="govuk-error-summary">
                            <div role="alert">
                                <h2 class="govuk-error-summary__title">
                                    There is a problem
                                </h2>
                                <div class="govuk-error-summary__body">
                                    <span class="govuk-!-font-weight-bold query-search__error__error-text">Enter a valid query string</span>
                                </div>
                            </div>
                        </div>
                    </div>
                    {% endif %}
                    """
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
            HTML(render_to_string("external_data/query-error.html")),
            HTML.details(
                "Help with building queries",
                render_to_string("external_data/help-build-query.html"),
            ),
        )
