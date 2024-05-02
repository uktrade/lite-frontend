import pytest

from caseworker.flags.helpers import has_flag


@pytest.mark.parametrize(
    ("item", "flag_id", "expected"),
    (
        ({}, "12345", False),
        ({"flags": []}, "12345", False),
        ({"flags": [{"id": "12345"}]}, "12345", True),
    ),
)
def test_has_flag(item, flag_id, expected):
    assert has_flag(item, flag_id) == expected
