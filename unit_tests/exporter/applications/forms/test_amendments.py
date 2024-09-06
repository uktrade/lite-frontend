from bs4 import BeautifulSoup

from exporter.applications.forms.common import ApplicationMajorEditConfirmationForm


def test_application_major_edit_confirm_form():
    form = ApplicationMajorEditConfirmationForm(
        data={},
        application_reference="your reference",
        cancel_url="",
    )
    assert form.is_valid() is True
    assert form.errors == {}


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
