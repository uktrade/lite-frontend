import pytest

from caseworker.advice.templatetags.advice_tags import get_clc, get_case_value, is_case_pv_graded


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
        ([{"good": {"is_pv_graded": "no"}}, {"good": {"is_pv_graded": "no"}},], False,),
        ([{"good": {"is_pv_graded": "yes"}}, {"good": {"is_pv_graded": "no"}},], True,),
        ([{"good": {"is_pv_graded": "yes"}}, {"good": {"is_pv_graded": "yes"}},], True,),
    ),
)
def test_is_case_pv_graded(goods, expected_value):
    result = is_case_pv_graded(goods)
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
