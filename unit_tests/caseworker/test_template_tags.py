from core.builtins import custom_tags

import pytest


@pytest.mark.parametrize(
    "value, other, expected",
    (
        (1, 2, 0.5),
        (None, None, None),
        (0, 1, 0),
        (1, 0, None),
        (1, None, None),
        (None, 1, None),
        ("1", 2, 0.5),
        ("1", "2", 0.5),
        ("1", None, None),
        (None, "1", None),
        ("a", 2, None),
        ("1.2", 2, 0.6),
        ("1.0", "2.0", 0.5),
    ),
)
def test_divide(value, other, expected):
    assert custom_tags.divide(value, other) == expected
