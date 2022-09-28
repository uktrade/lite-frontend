import pytest

from django import forms
from django.template import RequestContext, Template

from crispy_forms_gds.helper import FormHelper
from crispy_forms_gds.layout import Layout

from core.forms.layouts import (
    ConditionalCheckboxes,
    ConditionalRadios,
)


def test_conditional_radios_error_handling(mocker):
    class ConditionalRadiosForm(forms.Form):
        radio = forms.BooleanField()
        text = forms.CharField()

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)

            self.helper = FormHelper()
            self.helper.layout = Layout(
                ConditionalRadios(
                    mocker.Mock(),
                    "text",
                ),
            )

    with pytest.raises(TypeError):
        ConditionalRadiosForm()


def test_conditional_radios_question_error_handling(mocker, rf):
    class ConditionalRadiosForm(forms.Form):
        radio = forms.BooleanField()
        text = forms.CharField()

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)

            self.helper = FormHelper()
            self.helper.layout = Layout(
                ConditionalRadios(
                    "radio",
                    mocker.Mock(),
                ),
            )

    request = rf.get("/")
    request.session = {}
    form = ConditionalRadiosForm()
    t = Template("{% load crispy_forms_tags %}{% crispy form %}")
    c = RequestContext(request, {"form": form})
    with pytest.raises(TypeError):
        t.render(c)


def test_conditional_checkboxes_error_handling(mocker):
    class ConditionalCheckboxesForm(forms.Form):
        checkbox = forms.BooleanField()
        text = forms.CharField()

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)

            self.helper = FormHelper()
            self.helper.layout = Layout(
                ConditionalCheckboxes(
                    mocker.Mock(),
                    "text",
                ),
            )

    with pytest.raises(TypeError):
        ConditionalCheckboxesForm()


def test_conditional_checkboxes_question_error_handling(mocker, rf):
    class ConditionalCheckboxesForm(forms.Form):
        checkbox = forms.BooleanField()
        text = forms.CharField()

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)

            self.helper = FormHelper()
            self.helper.layout = Layout(
                ConditionalCheckboxes(
                    "checkbox",
                    mocker.Mock(),
                ),
            )

    request = rf.get("/")
    request.session = {}
    form = ConditionalCheckboxesForm()
    t = Template("{% load crispy_forms_tags %}{% crispy form %}")
    c = RequestContext(request, {"form": form})
    with pytest.raises(TypeError):
        t.render(c)
