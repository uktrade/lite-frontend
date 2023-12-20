from collections import defaultdict
import re

from django import forms


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


def update_css_class(attrs, css_class):
    attrs = attrs or {}
    attrs.setdefault("class", "")
    attrs["class"] += f" {css_class}"
    return attrs


class StyledBoundField(forms.BoundField):
    def label_tag(self, contents=None, attrs=None, label_suffix=None):
        attrs = update_css_class(attrs=attrs, css_class=self.form.label_css_classname)
        return super().label_tag(contents=contents, attrs=attrs, label_suffix=label_suffix)

    def build_widget_attrs(self, attrs=None, widget=None):
        attrs = update_css_class(attrs=attrs, css_class=self.form.input_css_classname)
        return super().build_widget_attrs(attrs=attrs, widget=widget)


class StyledCharField(forms.CharField):
    def get_bound_field(self, form, field_name):
        return StyledBoundField(form, self, field_name)


class GoodDetailsForm(forms.Form):
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
