import pytest
from exporter.applications.forms.hcsat import HCSATminiform, HCSATApplicationForm


@pytest.mark.parametrize(
    "data, is_valid, errors",
    (
        (
            {"satisfaction_rating": "NEITHER"},
            True,
            {},
        ),
        (
            {},
            False,
            {"satisfaction_rating": ["Star rating is required"]},
        ),
    ),
)
def test_hcsatmini_form(data, is_valid, errors):
    form = HCSATminiform(data=data)
    assert form.is_valid() is is_valid
    assert form.errors == errors


@pytest.mark.parametrize(
    "data, is_valid, errors",
    (
        (
            {"satisfaction_rating": "NEITHER"},
            True,
            {},
        ),
        (
            {},
            False,
            {"satisfaction_rating": ["Star rating is required"]},
        ),
    ),
)
def test_hcsat_form(data, is_valid, errors):
    form = HCSATApplicationForm(data=data)
    assert form.is_valid() is is_valid
    assert form.errors == errors
