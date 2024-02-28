import pytest
import re

from django import forms
from django.template import RequestContext, Template

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


def render_form(request, form_class):
    template = Template("{% load crispy_forms_tags crispy_forms_gds %}{% crispy form %}")
    context = RequestContext(request, {"form": form_class()})
    rendered = template.render(context)
    rendered = [l for l in rendered.split("\n")]
    rendered = re.sub("\s+", " ", "".join(rendered))
    return rendered


@pytest.mark.parametrize(
    "form_class,has_enctype",
    (
        (NoFileFieldForm, False),
        (FileFieldForm, True),
    ),
)
def test_base_form_enctype(form_class, has_enctype, rf):
    rendered = render_form(rf.get("/"), form_class)
    assert ('enctype="multipart/form-data' in rendered) is has_enctype


def test_layout_title(rf):
    class TitleForm(BaseForm):
        class Layout:
            TITLE = "title"

        def get_layout_fields(self):
            return []

    rendered = render_form(rf.get("/"), TitleForm)
    assert '<h1 class="govuk-heading-xl">title</h1>' in rendered


def test_layout_title_as_legend(rf):
    class TitleAsLegendForm(BaseForm):
        class Layout:
            TITLE = "title"
            TITLE_AS_LABEL_FOR = "char_field"

        char_field = forms.CharField()

        def get_layout_fields(self):
            return []

    rendered = render_form(rf.get("/"), TitleAsLegendForm)
    assert '<h1 class="govuk-heading-xl"><label for="id_char_field">title</label></h1>' in rendered


def test_layout_title_and_subtitle(rf):
    class TitleAndSubtitleForm(BaseForm):
        class Layout:
            TITLE = "title"
            SUBTITLE = "subtitle"

        def get_layout_fields(self):
            return []

    rendered = render_form(rf.get("/"), TitleAndSubtitleForm)
    assert '<h1 class="govuk-heading-xl govuk-!-margin-bottom-0">title</h1>' in rendered
    assert '<p class="govuk-hint">subtitle</p>' in rendered


def test_layout_title_as_legend_and_subtitle(rf):
    class TitleAsLegendAndSubtitleForm(BaseForm):
        class Layout:
            TITLE = "title"
            SUBTITLE = "subtitle"
            TITLE_AS_LABEL_FOR = "char_field"

        char_field = forms.CharField()

        def get_layout_fields(self):
            return []

    rendered = render_form(rf.get("/"), TitleAsLegendAndSubtitleForm)
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
def test_submit_button(form_class, submit_button_text, rf):
    rendered = render_form(rf.get("/"), form_class)
    assert (
        f'<input type="submit" name="submit" value="{submit_button_text}" class="govuk-button" id="submit-id-submit" />'
        in rendered
    )


def test_actions_wrapped_in_button_group(rf):
    class ButtonGroupForm(BaseForm):
        class Layout:
            TITLE = "Button group form"

        def get_layout_fields(self):
            return []

    rendered = render_form(rf.get("/"), ButtonGroupForm)
    assert (
        f'<div class="govuk-button-group" > <input type="submit" name="submit" value="Continue" class="govuk-button" id="submit-id-submit" /></div>'
        in rendered
    )


def test_no_get_layout_fields(rf):
    class NoGetLayoutFields(BaseForm):
        class Layout:
            TITLE = "No get layout fields"

    with pytest.raises(NotImplementedError):
        render_form(rf.get("/"), NoGetLayoutFields)
