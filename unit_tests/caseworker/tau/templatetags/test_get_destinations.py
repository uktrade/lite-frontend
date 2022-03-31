from unittest.mock import Mock

import pytest

from caseworker.tau.templatetags.tau_tags import get_destinations


@pytest.mark.parametrize(
    "case, expected_result",
    (
        (
            {
                "destinations": [
                    {"country": {"name": "test1"}},
                    {"country": {"name": "test2"}},
                ],
            },
            ["test1", "test2"],
        ),
        (
            {
                "destinations": [
                    {"country": {"name": "test2"}},
                    {"country": {"name": "test1"}},
                ],
            },
            ["test1", "test2"],
        ),
        (
            {
                "destinations": [
                    {"country": {"name": "test1"}},
                    {"country": {"name": "test1"}},
                ],
            },
            ["test1"],
        ),
        (
            {
                "destinations": [
                    {"country": {"name": "test"}},
                ],
            },
            ["test"],
        ),
        (
            {
                "destinations": [
                    {"country": {"name": None}},
                ]
            },
            [],
        ),
        (
            {
                "destinations": [{"country": None}],
            },
            [],
        ),
        (
            {
                "destinations": [],
            },
            [],
        ),
    ),
)
def test_get_destinations(case, expected_result):
    assert get_destinations(Mock(**case)) == expected_result
