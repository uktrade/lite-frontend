import json
from base64 import b64encode
from collections import OrderedDict
from typing import List, Dict

from caseworker.cases.objects import Case
from caseworker.core.constants import APPLICATION_CASE_TYPES, Permission, CLEARANCE_CASE_TYPES, AdviceType
from core.builtins.custom_tags import filter_advice_by_level, filter_advice_by_id, filter_advice_by_user

SINGULAR_ENTITIES = ["end_user", "consignee"]
PLURAL_ENTITIES = ["ultimate_end_user", "third_party", "country", "good", "goods_type"]
ALL_ENTITIES = SINGULAR_ENTITIES + PLURAL_ENTITIES


def get_param_destinations(request, case: Case):
    """
    get a list of destinations dictionaries from the case, based on the destinations selected by the user
    """
    selected_destinations_ids = [
        *request.GET.getlist("ultimate_end_user"),
        *request.GET.getlist("countries"),
        *request.GET.getlist("third_party"),
        request.GET.get("end_user"),
        request.GET.get("consignee"),
    ]
    case_destinations = case.destinations
    destinations = []

    for case_destination in case_destinations:
        # contract types are unique to Country on applications, and not on entities.
        if case_destination.get("contract_types") and case_destination["country"]["id"] in selected_destinations_ids:
            destinations.append(case_destination["country"])
        elif case_destination["id"] in selected_destinations_ids:
            destinations.append(case_destination)

    return destinations


def get_param_goods(request, case: Case):
    selected_goods_ids = request.GET.getlist("goods", request.GET.getlist("goods_types"))
    goods = case.data.get("goods", case.data.get("goods_types"))
    return [good for good in goods if good["id"] in selected_goods_ids]


def same_value(dicts, key):
    original_value = dicts[0][key]

    for dict in dicts:
        if dict[key] != original_value:
            return

    return original_value


def flatten_goods_data(items: List[Dict]):
    if not items:
        return

    # with OIEL, `items` is the goods, but with SIEL items has key with goods in it
    try:
        goods = [x["good"] for x in items]
    except KeyError:
        goods = items

    # fallback to default control details on the good if there is no good-on-application control details
    if all(x["is_good_controlled"] is not None for x in items):
        control_review = items
    else:
        control_review = goods
    is_good_controlled = same_value(control_review, "is_good_controlled")
    report_summary = same_value(control_review, "report_summary")
    control_list_entries = None

    # If the control list entry values do not match, or when not all selected goods are controlled
    # do not pre-populate the form fields to avoid errors
    if same_value(control_review, "control_list_entries"):
        control_list_entries = [
            {"key": i["rating"], "value": i["rating"]} for i in same_value(control_review, "control_list_entries")
        ]

    return {
        "is_good_controlled": is_good_controlled["key"] if is_good_controlled else None,
        "control_list_entries": control_list_entries,
        "report_summary": report_summary,
        "comment": same_value(control_review, "comment"),
    }


def flatten_advice_data(request, case: Case, items: List[Dict], level):
    keys = ["proviso", "denial_reasons", "note", "text", "type"]

    if level == "user-advice":
        level = "user"
    elif level == "team-advice":
        level = "team"
    elif level == "final-advice":
        level = "final"

    pre_filtered_advice = filter_advice_by_user(
        filter_advice_by_level(case["advice"], level), request.session["lite_api_user_id"]
    )
    filtered_advice = []

    for item in items:
        item_id = item["good"]["id"] if "good" in item else item["id"]
        advice = filter_advice_by_id(pre_filtered_advice, item_id)
        if advice:
            filtered_advice.append(advice[0])

    for advice in filtered_advice:
        for key in keys:
            if advice.get(key) != filtered_advice[0].get(key):
                return

    if not filtered_advice:
        return

    return filtered_advice[0]


def check_user_permitted_to_give_final_advice(case_type, permissions):
    """Check if the user is permitted to give final advice on the case based on their
    permissions and the case type."""
    if case_type in APPLICATION_CASE_TYPES and Permission.MANAGE_LICENCE_FINAL_ADVICE.value in permissions:
        return True
    elif case_type in CLEARANCE_CASE_TYPES and Permission.MANAGE_CLEARANCE_FINAL_ADVICE.value in permissions:
        return True
    else:
        return False


def can_advice_be_finalised(case):
    """Check that there is no conflicting advice and that the advice can be finalised."""
    for advice in filter_advice_by_level(case["advice"], "final"):
        if advice["type"]["key"] == AdviceType.CONFLICTING:
            return False

    return True


def can_user_create_and_edit_advice(case, permissions):
    """Check that the user can create and edit advice."""
    return Permission.MANAGE_TEAM_CONFIRM_OWN_ADVICE.value in permissions or (
        Permission.MANAGE_TEAM_ADVICE.value in permissions and not case.get("has_advice").get("my_user")
    )


def prepare_data_for_advice(json):
    # Split the json data into multiple
    new_data = []

    for entity_name in SINGULAR_ENTITIES:
        if json.get(entity_name):
            new_data.append(build_case_advice(entity_name, json.get(entity_name), json))

    for entity_name in PLURAL_ENTITIES:
        if json.get(entity_name):
            for entity in json.get(entity_name, []):
                new_data.append(build_case_advice(entity_name, entity, json))

    return new_data


def build_case_advice(key, value, base_data):
    data = base_data.copy()
    data[key] = value

    for entity in ALL_ENTITIES:
        if entity != key and entity in data:
            del data[entity]

    return data


def convert_advice_item_to_base64(advice_item):
    """
    Given an advice item, convert it to base64 suitable for comparisons
    """
    fields = [
        advice_item.get("denial_reasons", ""),
        (advice_item.get("proviso") or "").lower().replace(" ", ""),
        (advice_item.get("text") or "").lower().replace(" ", ""),
        (advice_item.get("note") or "").lower().replace(" ", ""),
        advice_item.get("type"),
        advice_item.get("level"),
    ]

    return b64encode(bytes(json.dumps(fields), "utf-8")).decode("utf-8")


def order_grouped_advice(grouped_advice):
    order = ["conflicting", "approve", "proviso", "no_licence_required", "not_applicable", "refuse", "no_advice"]
    return OrderedDict(sorted(grouped_advice.items(), key=lambda t: order.index(t[1]["type"]["key"])))


def filter_advice_by_target(advice_list, target):
    # filters a list of advice by the type of item it is for eg good, goods_type, country etc
    filtered = []

    for advice in advice_list:
        if advice.get(target) is not None:
            filtered.append(advice)

    return filtered


def case_goods_has_conflicting_advice(goods, advice_list):
    # go through each product. check for conflicting advice
    for good_on_application in goods:
        # find advice belonging to the good
        product_advice = [a for a in advice_list if a["good"] == good_on_application["good"]["id"]]
        advice_types = set([a["type"]["key"] for a in product_advice])

        if "conflicting" in advice_types:
            return True

        # if the good only has one type of advice, skip it
        if len(product_advice) in [0, 1]:
            continue

        if advice_types != {"approve", "proviso"}:
            return True

    return False


def goods_can_finalise(goods, advice_list):
    # go through each product. check for approvals/provisos/NLRs
    for good_on_application in goods:
        # find advice belonging to the good
        product_advice = [a for a in advice_list if a["good"] == good_on_application["good"]["id"]]

        advice_types = set([a["type"]["key"] for a in product_advice])

        if "approve" in advice_types or "proviso" in advice_types or "no_licence_required" in advice_types:
            return True

    return False
