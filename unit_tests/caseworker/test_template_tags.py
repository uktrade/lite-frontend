from core.builtins import custom_tags

from caseworker.core.constants import SLA_CIRCUMFERENCE

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


@pytest.mark.parametrize(
    "elapsed, total, expected",
    (
        (50, 25, SLA_CIRCUMFERENCE),
        (1, 25, SLA_CIRCUMFERENCE - (1 / 25 * SLA_CIRCUMFERENCE)),
    ),
)
def test_sla_ratio(elapsed, total, expected):
    actual = custom_tags.sla_ratio(elapsed, total)
    assert actual == expected


@pytest.mark.parametrize(
    "remaining, unit, colour",
    (
        (50, "hours", "red"),
        (48, "hours", "red"),
        (10, "hours", "orange"),
        (10, "days", "green"),
        (5, "days", "green"),
        (4, "days", "orange"),
        (0, "days", "red"),
        (-1, "days", "red"),
    ),
)
def test_sla_colour(remaining, unit, colour):
    actual = custom_tags.sla_colour(remaining, unit)
    assert actual == colour


def test_sla_colour_missing_unit():
    with pytest.raises(ValueError):
        custom_tags.sla_colour(10, "")
