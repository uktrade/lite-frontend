from crispy_forms_gds.helper import FormHelper
from crispy_forms_gds.choices import Choice
from crispy_forms_gds.layout import (
    Div,
    Fieldset,
    HTML,
    Layout,
    Size,
    Submit,
)
from django import forms


class TextChoice(Choice):
    def __init__(self, choice, **kwargs):
        super().__init__(choice.value, choice.label, **kwargs)


class BaseForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = FormHelper()
        for field in self.fields.values():
            if isinstance(field, forms.FileField):
                self.helper.attrs = {"enctype": "multipart/form-data"}
                break

        title = self.get_title()
        if hasattr(self.Layout, "TITLE_AS_LABEL_FOR"):
            id_for_label = self[self.Layout.TITLE_AS_LABEL_FOR].id_for_label
            title = f'<label for="{id_for_label}">{title}</label>'

        if not hasattr(self.Layout, "SUBTITLE"):
            headings = (HTML.h1(title),)
        else:
            headings = (
                HTML(f'<h1 class="govuk-heading-xl govuk-!-margin-bottom-0">{title}</h1>'),
                HTML(f'<p class="govuk-hint">{self.Layout.SUBTITLE}</p>'),
            )

        self.helper.layout = Layout(
            *headings,
            *self.get_layout_fields(),
            Div(
                *self.get_layout_actions(),
                css_class="govuk-button-group",
            ),
        )

    def get_title(self):
        return self.Layout.TITLE

    def get_layout_fields(self):
        raise NotImplementedError(f"Implement `get_layout_fields` on {self.__class__.__name__}")

    def get_layout_actions(self):
        if hasattr(self.Layout, "SUBMIT_BUTTON_TEXT"):
            submit_button_text = self.Layout.SUBMIT_BUTTON_TEXT
        else:
            submit_button_text = "Continue"
        return [
            Submit("submit", getattr(self.Layout, "SUBMIT_BUTTON", submit_button_text)),
        ]


class FieldsetForm(BaseForm):
    """This is a suitable layout for a single question form. By using a
    <fieldset> and <legend> it ensures that related inputs are grouped together
    with a common label to enable users to easily identify the group, as
    covered by WCAG Technique H71.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper.layout = Layout(
            Fieldset(
                *self.get_layout_fields(),
                legend=self.get_title(),
                legend_size=Size.EXTRA_LARGE,
                legend_tag="h1",
            ),
            Div(
                *self.get_layout_actions(),
                css_class="govuk-button-group",
            ),
        )


class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True


class MultipleFileField(forms.FileField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("widget", MultipleFileInput())
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        single_file_clean = super().clean
        result = [single_file_clean(d, initial) for d in data]
        return result
