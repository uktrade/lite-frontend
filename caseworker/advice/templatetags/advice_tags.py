from collections import defaultdict
from typing import Dict, List
from django import template

from caseworker.advice import constants, services


register = template.Library()


@register.filter()
def get_clc(goods_on_application):
    """Return a list of the unique control list entries for all goods in the supplied list.

    A single good may be passed instead of a list of one item.
    """
    if not isinstance(goods_on_application, list):
        goods_on_application = [goods_on_application]

    clcs = set()
    for good_on_application in goods_on_application:
        good = good_on_application.get("good", {})
        if not good:
            continue

        if good["status"]["key"] == "verified":
            good = good_on_application

        entries = {clc["rating"] for clc in good.get("control_list_entries", []) if clc}
        clcs.update(entries)

    return sorted(clcs - {None})


@register.filter()
def get_values_from_dict_list(items: List[Dict], key: str):
    return [item[key] for item in items]


@register.filter()
def get_adviser_list(case):
    unique_users = set()
    for users in case.assigned_users.values():
        unique_users.update({f"{user.get('first_name')} {user.get('last_name')}" for user in users})
    return list(unique_users)


@register.filter()
def get_flags_list(flags):
    return [flag.get("name") for flag in flags]


@register.filter()
def get_denial_references(denial_matches):
    denial_references = []
    for denial_match in denial_matches:
        denial_references.append(denial_match["denial_entity"]["reference"])
    return denial_references


@register.filter()
def get_sanction_list(sanction_matches):
    sanction_list = set()
    for sanction in sanction_matches:
        sanction_list.add(sanction["list_name"])
    return sanction_list


@register.filter()
def get_case_value(goods):
    return f'{sum([float(good.get("value") or "0") for good in goods]):.2f}'


@register.filter
def is_case_pv_graded(products):
    """Returns True if pv_grading is True for atleast one of the products on the application"""
    gradings = {product.get("good", {}).get("is_pv_graded") for product in products}
    return "yes" in gradings


@register.filter
def index(array, i):
    return array[i]


@register.filter
def get_item(dict, key):
    return dict.get(key, "")


@register.filter
def countersigned_user_team(advice):
    return f"{advice['countersigned_by']['team']['name']}"


@register.filter
def countersignatures_for_advice(case, advice):
    """
    This filters a case returning all LU countersignatures
    on that case (grouped by countersignature reverse order)
    that are attached to the advice passed as the parameter.
    """
    if not isinstance(advice, list):
        advice = [advice]
    advice_ids = {ad["id"] for ad in advice}
    countersignatures_grouped_by_order = defaultdict(list)
    for cs in case.get("countersign_advice", []):
        if cs["valid"] is True and cs.get("advice", {}).get("id") in advice_ids:
            countersignatures_grouped_by_order[cs["order"]].append(cs)
    return [
        countersignatures_grouped_by_order[order]
        for order in sorted(list(countersignatures_grouped_by_order.keys()), reverse=True)
    ]


@register.filter
def get_third_party(third_parties, id):
    return [party for party in third_parties if party["id"] == id]


@register.inclusion_tag("advice/group-advice.html", takes_context=True)
def group_advice(context):
    grouped_advice = []
    if context and context.get("case", {}).get("advice"):
        case = context.get("case")
        advice_by_team = services.group_advice_by_team(case["advice"])
        teams = sorted(
            {advice["team"]["id"]: advice["team"] for advice in case["advice"]}.values(),
            key=lambda a: a["name"],
        )

        for team in teams:
            team_advice = advice_by_team[team["id"]]

            team_users = {advice["user"]["id"]: advice["user"] for advice in team_advice}.values()

            grouped_advice.append(
                {
                    "team": team,
                    "advice": [group_team_advice_by_user(case, team_advice, team_user) for team_user in team_users],
                }
            )

        _add_team_decisions(grouped_advice)
    context["grouped_advice"] = grouped_advice
    return context


@register.filter()
def format_serial_numbers(serial_numbers, quantity):
    quantity = int(quantity)
    response = [f"{index}. {sn}" for index, sn in enumerate(serial_numbers, start=1)]
    if quantity > len(serial_numbers):
        response += [f"{index + 1}." for index in range(len(serial_numbers), quantity)]
    return response


@register.filter
def get_denial_reason_display_values(denial_reasons, denial_reasons_display):
    if denial_reasons and denial_reasons_display:
        return ", ".join([denial_reasons_display[item] for item in denial_reasons])


def group_team_advice_by_user(case, team_advice, team_user, level=None):
    user_advice = services.filter_advice_by_user(team_advice, team_user)

    if level is not None:
        user_advice = services.filter_advice_by_level(user_advice, [level])

    decisions = sorted(set(advice["type"]["value"] for advice in user_advice))
    return {
        "user": team_user,
        "advice": [
            group_user_advice_by_decision(case, user_advice, decision)
            for decision in decisions
            if [a for a in user_advice if a["type"]["value"] == decision]
        ],
    }


def group_user_advice_by_decision(case, user_advice, decision, level=None):
    user_advice_for_decision = [a for a in user_advice if a["type"]["value"] == decision and not a.get("good")]

    if level is not None:
        user_advice_for_decision = services.filter_advice_by_level(user_advice, [level])

    return {
        "decision": decision,
        "decision_verb": constants.DECISION_TYPE_VERB_MAPPING[decision],
        "advice": [
            create_destination_advice_item(user_advice_for_decision, destination)
            for destination in sorted(case.destinations, key=lambda d: d["name"])
            if [a for a in user_advice_for_decision if a.get(destination["type"]) is not None]
        ],
    }


def create_destination_advice_item(user_advice, destination):
    advice_item = [a for a in user_advice if a.get(destination["type"]) is not None][0]
    return {
        "name": destination["name"],
        "address": destination["address"],
        "licence_condition": advice_item.get("proviso"),
        "country": destination["country"]["name"],
        "denial_reasons": advice_item.get("denial_reasons"),
        "advice": advice_item,
    }


def _add_team_decisions(grouped_advice):
    for grouped in grouped_advice:
        for team_advice in grouped["advice"]:
            decisions = set()
            for user_advice in team_advice["advice"]:
                decisions.add(user_advice["decision"])

            if decisions == {"Approve"}:
                team_advice["decision"] = constants.TEAM_DECISION_APPROVED
            elif decisions == {"Proviso"} or decisions == {"Approve", "Proviso"}:
                team_advice["decision"] = constants.TEAM_DECISION_PROVISO
            elif decisions == {"Refuse"}:
                team_advice["decision"] = constants.TEAM_DECISION_REFUSED
            elif decisions == {"F680"}:
                team_advice["decision"] = constants.TEAM_DECISION_APPROVED_F680
            else:
                team_advice["decision"] = constants.TEAM_DECISION_APPROVED_REFUSED
