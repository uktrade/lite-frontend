import pytest
from django.template import Context
from caseworker.advice.templatetags.advice_tags import (
    get_clc,
    get_case_value,
    group_advice,
    is_case_pv_graded,
    get_denial_reason_display_values,
)
from caseworker.cases.objects import Case


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
        (
            [{"good": {"control_list_entries": [{"rating": "a"}]}}, {"good": {"control_list_entries": []}}],
            ["a"],
        ),
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
        (
            [{"good": {"control_list_entries": [{"rating": "a"}]}}, {"good": {}}],
            ["a"],
        ),
        # Missing good key
        (
            [{"good": {"control_list_entries": [{"rating": "a"}]}}, {}],
            ["a"],
        ),
    ),
)
def test_get_clc(goods, expected_value):
    result = get_clc(goods)
    assert result == expected_value


@pytest.mark.parametrize(
    "good, expected_value",
    (
        (
            {"good": {"control_list_entries": [{"rating": "a"}]}},
            ["a"],
        ),
    ),
)
def test_get_clc_single_good(good, expected_value):
    result = get_clc(good)
    assert result == expected_value


@pytest.mark.parametrize(
    "goods, expected_value",
    (
        (
            [
                {"good": {"is_pv_graded": "no"}},
                {"good": {"is_pv_graded": "no"}},
            ],
            False,
        ),
        (
            [
                {"good": {"is_pv_graded": "yes"}},
                {"good": {"is_pv_graded": "no"}},
            ],
            True,
        ),
        (
            [
                {"good": {"is_pv_graded": "yes"}},
                {"good": {"is_pv_graded": "yes"}},
            ],
            True,
        ),
    ),
)
def test_is_case_pv_graded(goods, expected_value):
    result = is_case_pv_graded(goods)
    assert result == expected_value


@pytest.mark.parametrize(
    "goods, expected_value",
    (
        # Base case
        (
            [{"value": "10"}, {"value": "10"}],
            "20.00",
        ),
        # One of the values is None
        (
            [{"value": "10"}, {"value": None}],
            "10.00",
        ),
        # Missing value key
        (
            [{"value": "10"}, {}],
            "10.00",
        ),
        # Missing good key
        (
            [{"value": "10"}, {}],
            "10.00",
        ),
    ),
)
def test_get_value(goods, expected_value):
    result = get_case_value(goods)
    assert result == expected_value


def test_group_advice(
    data_standard_case,
    team1,
    team2,
    john_smith,
    jane_doe,
    end_user_advice1,
    end_user_advice2,
    consignee_advice1,
    consignee_advice2,
    third_party_advice1,
    third_party_advice2,
    goods_advice1,
    goods_advice2,
):

    case_data = {**data_standard_case}
    case_data["case"]["advice"] = [
        end_user_advice1,
        end_user_advice2,
        consignee_advice1,
        consignee_advice2,
        third_party_advice1,
        third_party_advice2,
        goods_advice1,
        goods_advice2,
    ]

    exp_advice = [
        {
            "team": team1,
            "advice": [
                {
                    "user": john_smith,
                    "advice": [
                        {
                            "decision": "Approve",
                            "decision_verb": "approved",
                            "advice": [
                                {
                                    "name": "Consignee",
                                    "address": "44",
                                    "licence_condition": None,
                                    "country": "Abu Dhabi",
                                    "denial_reasons": None,
                                    "advice": consignee_advice1,
                                },
                                {
                                    "name": "End User",
                                    "address": "44",
                                    "licence_condition": None,
                                    "country": "United Kingdom",
                                    "denial_reasons": None,
                                    "advice": end_user_advice1,
                                },
                            ],
                        },
                        {
                            "decision": "Refuse",
                            "decision_verb": "refused",
                            "advice": [
                                {
                                    "name": "Third party",
                                    "address": "44",
                                    "licence_condition": None,
                                    "country": "United Kingdom",
                                    "denial_reasons": None,
                                    "advice": third_party_advice1,
                                }
                            ],
                        },
                    ],
                    "decision": "has approved and refused",
                }
            ],
        },
        {
            "team": team2,
            "advice": [
                {
                    "user": jane_doe,
                    "advice": [
                        {
                            "decision": "Approve",
                            "decision_verb": "approved",
                            "advice": [
                                {
                                    "name": "Consignee",
                                    "address": "44",
                                    "licence_condition": None,
                                    "country": "Abu Dhabi",
                                    "denial_reasons": None,
                                    "advice": consignee_advice2,
                                },
                                {
                                    "name": "End User",
                                    "address": "44",
                                    "licence_condition": None,
                                    "country": "United Kingdom",
                                    "denial_reasons": None,
                                    "advice": end_user_advice2,
                                },
                                {
                                    "name": "Third party",
                                    "address": "44",
                                    "licence_condition": None,
                                    "country": "United Kingdom",
                                    "denial_reasons": None,
                                    "advice": third_party_advice2,
                                },
                            ],
                        },
                    ],
                    "decision": "has approved",
                }
            ],
        },
    ]

    ctx = Context({"case": Case(case_data["case"])})
    grouped_advice = group_advice(ctx)["grouped_advice"]
    assert grouped_advice == exp_advice

    # we sort teams by name so these should be alphabetical
    assert grouped_advice[0]["team"] == team1
    assert grouped_advice[1]["team"] == team2

    team1_advice = grouped_advice[0]
    team2_advice = grouped_advice[1]
    john_smith_advice = team1_advice["advice"][0]
    jane_doe_advice = team2_advice["advice"][0]

    # team1 gave 2 different decisions, team2 only gave 1
    assert len(john_smith_advice["advice"]) == 2
    assert len(jane_doe_advice["advice"]) == 1

    # team1 approved 2 destinations
    assert john_smith_advice["advice"][0]["decision"] == "Approve"
    assert len(john_smith_advice["advice"][0]["advice"]) == 2
    assert john_smith_advice["advice"][0]["advice"][0]["name"] == "Consignee"
    assert john_smith_advice["advice"][0]["advice"][1]["name"] == "End User"

    # team1 refused 1 destination
    assert john_smith_advice["advice"][1]["decision"] == "Refuse"
    assert len(john_smith_advice["advice"][1]["advice"]) == 1
    assert john_smith_advice["advice"][1]["advice"][0]["name"] == "Third party"

    # team2 approved all three destinations
    assert jane_doe_advice["advice"][0]["decision"] == "Approve"
    assert len(jane_doe_advice["advice"][0]["advice"]) == 3
    assert jane_doe_advice["advice"][0]["advice"][0]["name"] == "Consignee"
    assert jane_doe_advice["advice"][0]["advice"][1]["name"] == "End User"
    assert jane_doe_advice["advice"][0]["advice"][2]["name"] == "Third party"


def test_get_denial_reason_display_values():
    display_dict = {"m": "military", "d": "destruction"}

    assert "military, destruction" == get_denial_reason_display_values(["m", "d"], display_dict)
