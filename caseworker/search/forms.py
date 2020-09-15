from collections import defaultdict
import re

from django import forms

from caseworker.spire.forms import StyledCharField


filter_names = "|".join(
    [
        "case_officer_email",
        "case_officer_username",
        "case_reference",
        "case_status",
        "clc_category",
        "clc_rating",
        "created",
        "created",
        "organisation",
        "part",
        "party_country",
        "party_type",
        "queue",
        "team",
        "created",
        "updated",
    ]
)

filter_lookups = "|".join(["__gte", "__lte", "__gt", "__lt", "__range"])

filters_regex_pattern = re.compile(f'({filter_names}(?:{filter_lookups})?):"(.*?)"')


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
