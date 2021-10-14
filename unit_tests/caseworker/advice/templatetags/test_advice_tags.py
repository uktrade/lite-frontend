import pytest

from caseworker.advice.templatetags.advice_tags import get_clc, get_case_value, get_security_grading


@pytest.mark.parametrize(
    "goods, expected_value",
    (
        # Base case
        (
            [
                {"good": {"control_list_entries": [{"rating": "a"}]}},
                {"good": {"control_list_entries": [{"rating": "b"}]}},
            ],
            ["a", "b"],
        ),
        # One of the CLC is empty
        ([{"good": {"control_list_entries": [{"rating": "a"}]}}, {"good": {"control_list_entries": []}}], ["a"],),
        # Same control_list_entry
        (
            [
                {"good": {"control_list_entries": [{"rating": "a"}]}},
                {"good": {"control_list_entries": [{"rating": "a"}]}},
            ],
            ["a"],
        ),
        # One of the CLC has more than one entry
        (
            [
                {"good": {"control_list_entries": [{"rating": "a"}, {"rating": "b"}]}},
                {"good": {"control_list_entries": [{"rating": "c"}]}},
            ],
            ["a", "b", "c"],
        ),
        # One of the CLC has a None entry
        (
            [
                {"good": {"control_list_entries": [{"rating": "a"}, None]}},
                {"good": {"control_list_entries": [{"rating": "b"}]}},
            ],
            ["a", "b"],
        ),
        # Missing control_list_entries key
        ([{"good": {"control_list_entries": [{"rating": "a"}]}}, {"good": {}}], ["a"],),
        # Missing good key
        ([{"good": {"control_list_entries": [{"rating": "a"}]}}, {}], ["a"],),
    ),
)
def test_get_clc(goods, expected_value):
    result = get_clc(goods)
    assert result == expected_value


@pytest.mark.parametrize(
    "goods, expected_value",
    (
        # Base case
        ([{"good": {"pv_grading_details": "a"}}, {"good": {"pv_grading_details": "b"}}], ["a", "b"],),
        # One of the pv_grading_details is None
        ([{"good": {"pv_grading_details": "a"}}, {"good": {"pv_grading_details": None}}], ["a"],),
        # Same pv_grading_details
        ([{"good": {"pv_grading_details": "a"}}, {"good": {"pv_grading_details": "a"}}], ["a"],),
        # Missing pv_grading_details key
        ([{"good": {"pv_grading_details": "a"}}, {"good": {}}], ["a"],),
        # Missing good key
        ([{"good": {"pv_grading_details": "a"}}, {}], ["a"],),
    ),
)
def test_get_security_grading(goods, expected_value):
    result = get_security_grading(goods)
    assert result == expected_value


@pytest.mark.parametrize(
    "goods, expected_value",
    (
        # Base case
        ([{"value": "10"}, {"value": "10"}], 20.0,),
        # One of the values is None
        ([{"value": "10"}, {"value": None}], 10.0,),
        # Missing value key
        ([{"value": "10"}, {}], 10.0,),
        # Missing good key
        ([{"value": "10"}, {}], 10.0,),
    ),
)
def test_get_value(goods, expected_value):
    result = get_case_value(goods)
    assert result == expected_value
