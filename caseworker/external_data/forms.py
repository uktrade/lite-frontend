from django import forms
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

from storages.backends.s3boto3 import S3Boto3StorageFile


denial_filters = {
    "name": "Name",
    "address": "Address",
}

denial_filter_names = "|".join(denial_filters.keys())
denial_filters_regex_pattern = re.compile(f'({denial_filter_names}?):"(.*?)"')


class DenialUploadForm(forms.Form):

    csv_file = forms.FileField(label="Upload a file")

    # the CreateView expects `instance` to be passed in here
    def __init__(self, instance, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def clean_csv_file(self):
        value = self.cleaned_data["csv_file"]
        if isinstance(value, S3Boto3StorageFile):
            s3_obj = value.obj.get()["Body"]
            return s3_obj.read().decode("utf-8")

        return value.read().decode("utf-8")

    def save(self):
        # the CreateView expects this method
        pass


class DenialRevoke(forms.Form):
    comment = forms.CharField(label="Enter a reason why this denial should be revoked", widget=forms.Textarea)


class DenialSearchForm(forms.Form):
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
        self.helper.form_class = "denial-search__form"
        self.helper.form_method = "GET"
        self.helper.attrs = {
            "data-denial-filter-labels": json.dumps(denial_filters),
            "data-search-url": reverse("external_data:api-search-suggest-denial"),
        }
        self.helper.layout = Layout(
            Field("search_string", css_class="denial-search__search-field input-force-default-width"),
            Div(
                Submit("submit", "Search"),
                css_class="denial-search__actions",
            ),
        )

    def clean(self):
        super().clean()
        # pagination
        self.cleaned_data["limit"] = self.page_size
        self.cleaned_data["page"] = self.cleaned_data["page"] or 1
        self.cleaned_data["offset"] = (self.cleaned_data["page"] - 1) * self.page_size


class DenialSearchSuggestForm(forms.Form):
    q = forms.CharField()

    def clean_q(self):
        return denial_filters_regex_pattern.sub("", self.cleaned_data["q"])
