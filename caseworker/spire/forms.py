from django import forms


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


class SpireLicenseSearchForm(forms.Form):
    input_css_classname = "govuk-input"
    label_css_classname = "lite-filter-bar__label"

    page_size = 30

    licence_ref = StyledCharField(label="Filter by license reference number", label_suffix="", required=False)
    part_no = StyledCharField(label="Filter by product part number", label_suffix="", required=False)
    description = StyledCharField(label="Filter by product description", label_suffix="", required=False)
    page = forms.IntegerField(widget=forms.HiddenInput(), required=False, initial=1)

    def clean(self):
        super().clean()
        # pagination
        self.cleaned_data["limit"] = self.page_size
        self.cleaned_data["page"] = self.cleaned_data["page"] or 1
        self.cleaned_data["offset"] = (self.cleaned_data["page"] - 1) * self.page_size


class SpireApplicationSearchForm(forms.Form):
    input_css_classname = "govuk-input"
    label_css_classname = "lite-filter-bar__label"

    page_size = 30

    application_ref = StyledCharField(label="Filter by application reference number", label_suffix="", required=False)
    part_no = StyledCharField(label="Filter by product part number", label_suffix="", required=False)
    description = StyledCharField(label="Filter by product description", label_suffix="", required=False)
    page = forms.IntegerField(widget=forms.HiddenInput(), required=False, initial=1)

    def clean(self):
        super().clean()
        # pagination
        self.cleaned_data["limit"] = self.page_size
        self.cleaned_data["page"] = self.cleaned_data["page"] or 1
        self.cleaned_data["offset"] = (self.cleaned_data["page"] - 1) * self.page_size
