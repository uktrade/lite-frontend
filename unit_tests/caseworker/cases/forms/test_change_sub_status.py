import pytest

from caseworker.cases.forms.change_sub_status import ChangeSubStatusForm


@pytest.mark.parametrize(
    "data, is_valid, errors",
    (
        (
            {},
            True,
            {},
        ),
        (
            {"sub_status": "status-1"},
            True,
            {},
        ),
        (
            {"sub_status": "madeup"},
            False,
            {"sub_status": ["Select a valid choice. madeup is not one of the available choices."]},
        ),
    ),
)
def test_change_sub_status_form(data, is_valid, errors):
    form = ChangeSubStatusForm(
        sub_statuses=[("status-1", "Status 1"), ("status-2", "Status 2")],
        data=data,
    )
    assert form.is_valid() == is_valid
    assert form.errors == errors
