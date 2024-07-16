from exporter.applications.forms.common import ApplicationMajorEditConfirmationForm


def test_application_major_edit_confirm_form():
    form = ApplicationMajorEditConfirmationForm(
        data={},
        application_reference="your reference",
        cancel_url="",
    )
    assert form.is_valid() is True
    assert form.errors == {}
