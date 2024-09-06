import pytest
import re

from bs4 import BeautifulSoup

from django.template import (
    RequestContext,
    Template,
)

from exporter.applications.forms.common import ApplicationMajorEditConfirmationForm


def test_application_major_edit_confirm_form():
    form = ApplicationMajorEditConfirmationForm(
        data={},
        application_reference="your reference",
        cancel_url="",
    )
    assert form.is_valid() is True
    assert form.errors == {}


@pytest.fixture()
def render_form(rf):
    def _render_form(form, request=None):
        if not request:
            request = rf.get("/")
        template = Template("{% load crispy_forms_tags crispy_forms_gds %}{% crispy form %}")
        context = RequestContext(request, {"form": form})
        rendered = template.render(context)
        rendered = [l for l in rendered.split("\n")]
        rendered = re.sub("\s+", " ", "".join(rendered))
        return rendered

    return _render_form


def test_disabling_button_data_module(render_form):
    form = ApplicationMajorEditConfirmationForm(
        data={},
        application_reference="your reference",
        cancel_url="",
    )
    rendered = render_form(form)
    soup = BeautifulSoup(rendered, "html.parser")
    submit_button = soup.find("input", {"id": "submit-id-submit"})
    assert submit_button.attrs["data-module"] == "disabling-button"
