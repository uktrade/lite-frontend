import pytest

from caseworker.tau.templatetags.tau_tags import is_ultimate_end_user


@pytest.mark.parametrize(
    "destinations, expected_result",
    (
        ([{"type": "end_user"}, {"type": "ultimate_end_user"}], True),
        ([{"type": "ultimate_end_user"}], True),
        ([{"type": "end_user"}], False),
        ([{"type": None}], False),
        ([{}], False),
        ([], False),
    ),
)
def test_is_ultimate_end_user(destinations, expected_result):
    assert is_ultimate_end_user(destinations) == expected_result
