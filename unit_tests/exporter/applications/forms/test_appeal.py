import pytest

from exporter.applications.forms.appeal import AppealForm


@pytest.mark.parametrize(
    "data, is_valid, errors",
    (
        (
            {},
            False,
            {
                "grounds_for_appeal": ["This field is required."],
            },
        ),
        (
            {"grounds_for_appeal": "These are my grounds for appeal"},
            True,
            {},
        ),
    ),
)
def test_appeal_form(data, is_valid, errors):
    form = AppealForm(
        cancel_url="http://example.com",
        data=data,
    )
    assert form.is_valid() is is_valid
    assert form.errors == errors
