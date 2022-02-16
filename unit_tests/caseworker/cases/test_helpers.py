import pytest

from caseworker.cases.helpers import advice
from caseworker.cases.objects import Case

nlr = {"key": "no_licence_required", "value": "No licence required"}
approve = {"key": "approve", "value": "Approve"}
proviso = {"key": "proviso", "value": "Approve with proviso"}
refuse = {"key": "refuse", "value": "Refuse"}
conflicting = {"key": "conflicting", "value": "Conflicting"}

john_smith = {
    "email": "john.smith@example.com",
    "first_name": "John",
    "id": "63c74ddd-c119-48cc-8696-d196218ca583",
    "last_name": "Smith",
    "role_name": "Super User",
    "status": "Active",
    "team": {"id": "136cbb1f-390b-4f78-bfca-86300edec300", "name": "team1", "part_of_ecju": None},
}


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


@pytest.mark.parametrize(
    "product_1_advice,product_2_advice,is_conflicting",
    (
        ([approve, refuse], refuse, True),
        ([approve, proviso], refuse, False),
        ([approve], refuse, False),
        ([approve], approve, False),
        ([refuse], approve, False),
        ([conflicting], approve, True),
        ([conflicting], refuse, True),
    ),
)
def test_case_goods_has_conflicting_advice(product_1_advice, product_2_advice, is_conflicting):
    product_1_id = "8b730c06-ab4e-401c-aeb0-32b3c92e912c"
    product_2_id = "13820c06-ab4e-401c-aeb0-32b3c92e912c"

    product_1_advice_1 = {
        "id": "8993476f-9849-49d1-973e-62b185085a64",
        "type": product_1_advice[0],
        "good": product_1_id,
    }
    product_2_advice = {
        "id": "8993476f-9849-49d1-973e-62b185085a64",
        "type": product_2_advice,
        "good": product_2_id,
    }

    product_1 = {
        "id": "0bedd1c3-cf97-4aad-b711-d5c9a9f4586e",
        "good": {
            "id": product_1_id,
        },
    }
    product_2 = {
        "id": "0bedd1c3-cf97-4aad-b711-d5c9a9f4586e",
        "good": {
            "id": product_2_id,
        },
    }

    goods = [product_1, product_2]
    advice_list = [product_1_advice_1, product_2_advice]

    if len(product_1_advice) > 1:
        product_1_advice_2 = {
            "id": "0099476f-9849-49d1-973e-62b185085a64",
            "type": product_1_advice[1],
            "good": product_1_id,
        }
        advice_list.append(product_1_advice_2)

    assert advice.case_goods_has_conflicting_advice(goods, advice_list) == is_conflicting


@pytest.mark.parametrize(
    "advice_types,can_finalise",
    (
        ([approve, refuse, refuse], True),
        ([approve, proviso, approve], True),
        ([refuse, proviso, refuse], True),
        ([refuse, refuse, nlr], True),
        ([refuse, refuse, refuse], False),
        ([refuse, conflicting, refuse], False),
    ),
)
def test_goods_list_can_finalise(advice_types, can_finalise):
    product_1_id = "8b730c06-ab4e-401c-aeb0-32b3c92e912c"
    product_2_id = "13820c06-ab4e-401c-aeb0-32b3c92e912c"
    product_3_id = "00020c06-ab4e-401c-aeb0-32b3c92e912c"

    product_1_advice = {
        "id": "8993476f-9849-49d1-973e-62b185085a64",
        "type": advice_types[0],
        "good": product_1_id,
    }
    product_2_advice = {
        "id": "8993476f-9849-49d1-973e-62b185085a64",
        "type": advice_types[1],
        "good": product_2_id,
    }
    product_3_advice = {
        "id": "8993476f-9849-49d1-973e-62b185085a64",
        "type": advice_types[2],
        "good": product_3_id,
    }

    product_1 = {
        "id": "0bedd1c3-cf97-4aad-b711-d5c9a9f4586e",
        "good": {
            "id": product_1_id,
        },
    }
    product_2 = {
        "id": "0bedd1c3-cf97-4aad-b711-d5c9a9f4586e",
        "good": {
            "id": product_2_id,
        },
    }
    product_3 = {
        "id": "0bedd1c3-cf97-4aad-b711-d5c9a9f4586e",
        "good": {
            "id": product_3_id,
        },
    }

    goods = [product_1, product_2, product_3]
    advice_list = [product_1_advice, product_2_advice, product_3_advice]

    assert advice.goods_can_finalise(goods, advice_list) == can_finalise


advice_stub = {
    "good": None,
    "goods_type": None,
    "country": None,
    "end_user": None,
    "ultimate_end_user": None,
    "consignee": None,
    "third_party": None,
}
product_advice = {**advice_stub}
product_advice["good"] = "foo"
country_advice = {**advice_stub}
country_advice["country"] = "foo"
end_user_advice = {**advice_stub}
end_user_advice["end_user"] = "foo"


@pytest.mark.parametrize(
    "advice_list,target,exp_length",
    (
        ([product_advice, product_advice, product_advice], "good", 3),
        ([country_advice, product_advice, product_advice], "good", 2),
        ([country_advice, product_advice, product_advice], "country", 1),
        ([country_advice, product_advice, end_user_advice], "country", 1),
        ([country_advice, product_advice, end_user_advice], "end_user", 1),
    ),
)
def test_filter_advice_by_target(advice_list, target, exp_length):
    assert len(advice.filter_advice_by_target(advice_list, target)) == exp_length
