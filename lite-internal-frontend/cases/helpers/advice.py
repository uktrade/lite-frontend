import json
from base64 import b64encode
from collections import OrderedDict
from typing import List, Dict

from cases.objects import Case
from cases.services import get_blocking_flags
from conf.constants import APPLICATION_CASE_TYPES, Permission, CLEARANCE_CASE_TYPES, AdviceType
from core.builtins.custom_tags import filter_advice_by_level, filter_advice_by_id, filter_advice_by_user
from core.services import get_status_properties
from teams.services import get_teams

SINGULAR_ENTITIES = ["end_user", "consignee"]
PLURAL_ENTITIES = ["ultimate_end_user", "third_party", "country", "good", "goods_type"]
ALL_ENTITIES = SINGULAR_ENTITIES + PLURAL_ENTITIES


def get_param_destinations(request, case: Case):
    selected_destinations_ids = [
        *request.GET.getlist("ultimate_end_user"),
        *request.GET.getlist("countries"),
        *request.GET.getlist("third_party"),
        request.GET.get("end_user"),
        request.GET.get("consignee"),
    ]
    destinations = case.destinations
    return_values = []

    for destination in destinations:
        if destination.get("country"):
            if destination["country"]["id"] in selected_destinations_ids:
                return_values.append(destination["country"])
        else:
            if destination["id"] in selected_destinations_ids:
                return_values.append(destination)

    return return_values


def get_param_goods(request, case: Case):
    selected_goods_ids = request.GET.getlist("goods", request.GET.getlist("goods_types"))
    goods = case.data.get("goods", case.data.get("goods_types"))
    return_values = []

    for good in goods:
        if "good" in good:
            if good["good"]["id"] in selected_goods_ids:
                return_values.append(good)
        else:
            if good["id"] in selected_goods_ids:
                return_values.append(good)

    return return_values


def get_advice_additional_context(request, case, permissions):
    status_props, _ = get_status_properties(request, case.data["status"]["key"])
    current_advice_level = "user"
    blocking_flags = get_blocking_flags(request, case["id"])

    if filter_advice_by_level(case["advice"], "team"):
        current_advice_level = "team"

        if Permission.MANAGE_TEAM_ADVICE.value not in permissions:
            current_advice_level = None

    if filter_advice_by_level(case["advice"], "final") and _check_user_permitted_to_give_final_advice(
        case["application"]["case_type"]["sub_type"]["key"], permissions
    ):
        current_advice_level = "final"

    if not _can_user_create_and_edit_advice(case, permissions) or status_props["is_terminal"]:
        current_advice_level = None

    return {
        "is_user_team": True,
        "teams": get_teams(request),
        "current_advice_level": current_advice_level,
        "can_finalise": current_advice_level == "final" and can_advice_be_finalised(case) and not blocking_flags,
        "blocking_flags": blocking_flags,
    }


def same_value(dicts, key):
    original_value = dicts[0][key]

    for dict in dicts:
        if dict[key] != original_value:
            return

    return original_value


def flatten_goods_data(items: List[Dict]):
    if not items:
        return

    if "good" in items[0]:
        items = [x["good"] for x in items]

    is_good_controlled = same_value(items, "is_good_controlled")
    control_list_entries = [
        {"key": clc["rating"], "value": clc["rating"]} for clc in same_value(items, "control_list_entries")
    ]

    return {"is_good_controlled": is_good_controlled, "control_list_entries": control_list_entries}


def flatten_advice_data(request, case: Case, items: List[Dict], level):
    keys = ["proviso", "denial_reasons", "note", "text", "type"]

    if level == "user-advice":
        level = "user"
    elif level == "team-advice":
        level = "team"
    elif level == "final-advice":
        level = "final"

    pre_filtered_advice = filter_advice_by_user(
        filter_advice_by_level(case["advice"], level), request.user.lite_api_user_id
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


def _check_user_permitted_to_give_final_advice(case_type, permissions):
    """ Check if the user is permitted to give final advice on the case based on their
    permissions and the case type. """
    if case_type in APPLICATION_CASE_TYPES and Permission.MANAGE_LICENCE_FINAL_ADVICE.value in permissions:
        return True
    elif case_type in CLEARANCE_CASE_TYPES and Permission.MANAGE_CLEARANCE_FINAL_ADVICE.value in permissions:
        return True
    else:
        return False


def can_advice_be_finalised(case):
    """Check that there is no conflicting advice and that the advice can be finalised. """
    for advice in filter_advice_by_level(case["advice"], "final"):
        if advice["type"]["key"] == AdviceType.CONFLICTING:
            return False

    return True


def _can_user_create_and_edit_advice(case, permissions):
    """Check that the user can create and edit advice. """
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
        advice_item.get("proviso", "").lower().replace(" ", ""),
        advice_item["text"].lower().replace(" ", ""),
        advice_item["note"].lower().replace(" ", ""),
        advice_item["type"],
        advice_item["level"],
    ]

    return b64encode(bytes(json.dumps(fields), "utf-8")).decode("utf-8")


def order_grouped_advice(grouped_advice):
    order = ["conflicting", "approve", "proviso", "no_licence_required", "not_applicable", "refuse", "no_advice"]
    return OrderedDict(sorted(grouped_advice.items(), key=lambda t: order.index(t[1]["type"]["key"])))
