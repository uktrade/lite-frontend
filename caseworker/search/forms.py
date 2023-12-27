import json
import re

from crispy_forms_gds.helper import FormHelper
from crispy_forms_gds.layout import (
    Div,
    Field,
    Layout,
    Submit,
)
from django import forms
from django.urls import reverse


product_filters = {
    "name": "Name",
    "part_number": "Part number",
    "consignee_country": "Consignee country",
    "end_user_country": "End-user country",
    "ultimate_end_user_country": "Ultimate end-user country",
    "ratings": "Control list entry",
    "regimes": "Regime",
    "report_summary": "Report summary",
    "organisation": "Applicant",
    "assessed_by": "Assessor",
    "assessment_note": "Assessment note",
    "destination": "Destination",
}


product_filter_names = "|".join(product_filters.keys())

product_filters_regex_pattern = re.compile(f'({product_filter_names}?):"(.*?)"')


class ProductSearchForm(forms.Form):
    page_size = 25

    search_string = forms.CharField(
        widget=forms.TextInput(attrs={"autocomplete": "off"}),
        label="",
        required=False,
    )
    page = forms.IntegerField(widget=forms.HiddenInput(), required=False, initial=1)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_class = "product-search__form"
        self.helper.form_method = "GET"
        self.helper.attrs = {
            "data-product-filter-labels": json.dumps(product_filters),
            "data-search-url": reverse("search:api-search-suggest-product"),
        }
        self.helper.layout = Layout(
            Field("search_string", css_class="product-search__search-field input-force-default-width"),
            Div(
                Submit("submit", "Search"),
                css_class="product-search__actions",
            ),
        )

    def clean(self):
        super().clean()
        # pagination
        self.cleaned_data["limit"] = self.page_size
        self.cleaned_data["page"] = self.cleaned_data["page"] or 1
        self.cleaned_data["offset"] = (self.cleaned_data["page"] - 1) * self.page_size


class ProductSearchSuggestForm(forms.Form):
    q = forms.CharField()

    def clean_q(self):
        return product_filters_regex_pattern.sub("", self.cleaned_data["q"])
