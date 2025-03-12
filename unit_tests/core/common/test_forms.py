import pytest

from django import forms

from core.common.forms import BaseForm


class NoFileFieldForm(BaseForm):
    class Layout:
        TITLE = "NO FILE FIELD"

    def get_layout_fields(self):
        return []


class FileFieldForm(BaseForm):
    class Layout:
        TITLE = "FILE FIELD"

    file = forms.FileField()

    def get_layout_fields(self):
        return ["file"]


class BaseFormWithoutTitleAndTitleAsLabelFor(BaseForm):
    class Layout:
        TITLE = "title_for_BaseFormWithTitleAndTitleAsLabelFor"

    char_field = forms.CharField(label="")

    def get_layout_fields(self):
        return ("char_field",)


class BaseFormWithTitleAndTitleAsLabelFor(BaseForm):
    class Layout:
        TITLE = "title_for_BaseFormWithTitleAndTitleAsLabelFor"
        TITLE_AS_LABEL_FOR = "char_field"

    char_field = forms.CharField(label="")

    def get_layout_fields(self):
        return ("char_field",)


@pytest.mark.parametrize(
    "form_class,has_enctype",
    (
        (NoFileFieldForm, False),
        (FileFieldForm, True),
    ),
)
def test_base_form_enctype(form_class, has_enctype, render_form):
    rendered = render_form(form_class())
    assert ('enctype="multipart/form-data' in rendered) is has_enctype


def test_layout_title(render_form):
    class TitleForm(BaseForm):
        class Layout:
            TITLE = "title"

        def get_layout_fields(self):
            return []

    rendered = render_form(TitleForm())
    assert '<h1 class="govuk-heading-xl">title</h1>' in rendered


def test_layout_title_as_legend(render_form):
    class TitleAsLegendForm(BaseForm):
        class Layout:
            TITLE = "title"
            TITLE_AS_LABEL_FOR = "char_field"

        char_field = forms.CharField()

        def get_layout_fields(self):
            return []

    rendered = render_form(TitleAsLegendForm())
    assert '<h1 class="govuk-heading-xl"><label for="id_char_field">title</label></h1>' in rendered


def test_layout_title_and_subtitle(render_form):
    class TitleAndSubtitleForm(BaseForm):
        class Layout:
            TITLE = "title"
            SUBTITLE = "subtitle"

        def get_layout_fields(self):
            return []

    rendered = render_form(TitleAndSubtitleForm())
    assert '<h1 class="govuk-heading-xl govuk-!-margin-bottom-0">title</h1>' in rendered
    assert '<p class="govuk-hint">subtitle</p>' in rendered


def test_layout_title_as_legend_and_subtitle(render_form):
    class TitleAsLegendAndSubtitleForm(BaseForm):
        class Layout:
            TITLE = "title"
            SUBTITLE = "subtitle"
            TITLE_AS_LABEL_FOR = "char_field"

        char_field = forms.CharField()

        def get_layout_fields(self):
            return []

    rendered = render_form(TitleAsLegendAndSubtitleForm())
    assert (
        '<h1 class="govuk-heading-xl govuk-!-margin-bottom-0"><label for="id_char_field">title</label></h1>' in rendered
    )
    assert '<p class="govuk-hint">subtitle</p>' in rendered


class DefaultSubmitButton(BaseForm):
    class Layout:
        TITLE = "Default submit button"

    def get_layout_fields(self):
        return []


class OverriddenSubmitButton(BaseForm):
    class Layout:
        TITLE = "Overridden submit button"
        SUBMIT_BUTTON = "Overridden"

    def get_layout_fields(self):
        return []


@pytest.mark.parametrize(
    "form_class,submit_button_text",
    (
        (DefaultSubmitButton, "Continue"),
        (OverriddenSubmitButton, "Overridden"),
    ),
)
def test_submit_button(form_class, submit_button_text, render_form):
    rendered = render_form(form_class())
    assert (
        f'<input type="submit" name="submit" value="{submit_button_text}" class="govuk-button" id="submit-id-submit" />'
        in rendered
    )


def test_actions_wrapped_in_button_group(render_form):
    class ButtonGroupForm(BaseForm):
        class Layout:
            TITLE = "Button group form"

        def get_layout_fields(self):
            return []

    rendered = render_form(ButtonGroupForm())
    assert (
        f'<div class="govuk-button-group" > <input type="submit" name="submit" value="Continue" class="govuk-button" id="submit-id-submit" /></div>'
        in rendered
    )


def test_no_get_layout_fields(render_form):
    class NoGetLayoutFields(BaseForm):
        class Layout:
            TITLE = "No get layout fields"

    with pytest.raises(NotImplementedError):
        render_form(NoGetLayoutFields())


def test_get_field_label_with_title_as_label_for_produces_correct_label():
    form = BaseFormWithTitleAndTitleAsLabelFor()
    title_with_label_tag = form.get_field_label("char_field")

    assert form.Layout.TITLE == "title_for_BaseFormWithTitleAndTitleAsLabelFor"
    assert title_with_label_tag == "title_for_BaseFormWithTitleAndTitleAsLabelFor"


def test_get_field_label_without_title_as_label_has_no_label():
    form = BaseFormWithoutTitleAndTitleAsLabelFor()
    title_without_label_tag = form.get_field_label("char_field")

    assert form.Layout.TITLE == "title_for_BaseFormWithTitleAndTitleAsLabelFor"
    assert title_without_label_tag == ""
