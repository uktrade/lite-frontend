from caseworker.cases.helpers import advice
from caseworker.cases.objects import Case


def test_convert_advice_item_to_base64():
    """
    Asserts that advice comparison is case and space insensitive
    """
    item_1 = {
        "text": "I Am Easy to Find",
        "note": "I Am Easy to Find",
        "type": "I Am Easy to Find",
        "level": "I Am Easy to Find",
    }
    item_2 = {
        "text": "Iameasytofind",
        "note": "I Am Easy to Find",
        "type": "I Am Easy to Find",
        "level": "I Am Easy to Find",
    }
    assert advice.convert_advice_item_to_base64(item_1) == advice.convert_advice_item_to_base64(item_2)


def test_order_grouped_advice():
    """
    Asserts ordering of conflicting, approve, proviso, no_licence_required,
    not_applicable, refuse, no_advice
    """
    initial_order = {
        1: {"type": {"key": "refuse"}},
        2: {"type": {"key": "approve"}},
        3: {"type": {"key": "no_licence_required"}},
        4: {"type": {"key": "refuse"}},
        5: {"type": {"key": "conflicting"}},
        6: {"type": {"key": "no_advice"}},
        7: {"type": {"key": "not_applicable"}},
    }

    ordered = list(advice.order_grouped_advice(initial_order).keys())

    assert ordered[0] == 5
    assert ordered[1] == 2
    assert ordered[2] == 3
    assert ordered[3] == 7
    assert ordered[4] == 1
    assert ordered[5] == 4
    assert ordered[6] == 6


def test_flatten_goods_data_open_application(data_open_case, rf):
    good_ids = [good["id"] for good in data_open_case["case"]["data"]["goods_types"]]

    request = rf.get("/", {"goods": good_ids})
    param_goods = advice.get_param_goods(request, Case(data_open_case["case"]))

    actual = advice.flatten_goods_data(param_goods)

    assert actual == {
        "is_good_controlled": "False",
        "control_list_entries": [{"key": "ML1a", "value": "ML1a"}],
        "report_summary": None,
        "comment": None,
    }
