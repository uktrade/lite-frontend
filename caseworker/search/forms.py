from collections import defaultdict
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

from caseworker.spire.forms import StyledCharField


def build_filter_lookups(field_name):
    return [f"{field_name}__{suffix}" for suffix in ["gte", "lte", "gt", "lt", "range"]]


filter_names = "|".join(
    [
        "case_officer_email",
        "case_officer_username",
        "case_reference",
        "case_status",
        "clc_category",
        "clc_rating",
        "organisation",
        "part",
        "party_country",
        "party_type",
        "queue",
        "team",
        "database",
        "report_summary",
        "incorporated",
        "case_type",
        "case_subtype",
        "destination",  # for products
        *build_filter_lookups("created"),
        *build_filter_lookups("updated"),
    ]
)

filters_regex_pattern = re.compile(f'({filter_names}?):"(.*?)"')


class SearchForm(forms.Form):
    input_css_classname = "govuk-input"
    label_css_classname = "lite-filter-bar__label"

    page_size = 25

    search_string = StyledCharField(label="Search keyword", label_suffix="", required=False)
    page = forms.IntegerField(widget=forms.HiddenInput(), required=False, initial=1)

    @staticmethod
    def extract_filters(search_string):
        filters = defaultdict(list)
        for key, value in filters_regex_pattern.findall(search_string):
            filters[key].append(value)
        return filters

    def clean(self):
        super().clean()
        # pagination
        self.cleaned_data["limit"] = self.page_size
        self.cleaned_data["page"] = self.cleaned_data["page"] or 1
        self.cleaned_data["offset"] = (self.cleaned_data["page"] - 1) * self.page_size
        self.cleaned_data["filters"] = self.extract_filters(self.cleaned_data["search_string"])
        self.cleaned_data["search"] = filters_regex_pattern.sub("", self.cleaned_data["search_string"]).strip()


class AutocompleteForm(forms.Form):
    q = forms.CharField()

    def clean_q(self):
        return filters_regex_pattern.sub("", self.cleaned_data["q"])


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
