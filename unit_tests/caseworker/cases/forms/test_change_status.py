import pytest

from caseworker.cases.forms.change_status import ChangeStatusForm


@pytest.mark.parametrize(
    "data, is_valid, errors",
    (
        (
            {},
            False,
            {"status": ["Select a status to save"]},
        ),
        (
            {"status": "under_review"},
            True,
            {},
        ),
        (
            {"status": "madeup"},
            False,
            {"status": ["Select a valid choice. madeup is not one of the available choices."]},
        ),
    ),
)
def test_change_status_form(data, is_valid, errors):
    form = ChangeStatusForm(
        statuses=[("submitted", "Submitted"), ("under_review", "Under review")],
        data=data,
    )
    assert form.is_valid() == is_valid
    assert form.errors == errors
