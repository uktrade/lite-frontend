from collections import defaultdict
import re

from django import forms

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
        *build_filter_lookups("created"),
        *build_filter_lookups("updated"),
    ]
)

filters_regex_pattern = re.compile(f'({filter_names}?):"(.*?)"')


class CasesSearchForm(forms.Form):
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
        self.cleaned_data["search_string"] = filters_regex_pattern.sub("", self.cleaned_data["search_string"]).strip()


class AutocompleteForm(forms.Form):
    q = forms.CharField()

    def clean_q(self):
        return filters_regex_pattern.sub("", self.cleaned_data["q"])
