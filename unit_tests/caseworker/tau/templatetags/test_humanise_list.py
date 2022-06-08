import pytest

from caseworker.tau.templatetags import tau_tags


@pytest.mark.parametrize(
    "input, expected",
    (
        ([], ""),
        (["test"], "test"),
        (["test1", "test2"], "test1 and test2"),
        (["test1", "test2", "test3"], "test1, test2 and test3"),
    ),
)
def test_humanise_list(input, expected):
    assert tau_tags.humanise_list(input) == expected
