from django import template

from caseworker.advice import constants, services


register = template.Library()


@register.filter()
def get_clc(goods):
    """Return a list of the unique control list entries for all goods in the supplied list.

    A single good may be passed instead of a list of one item.
    """
    if not isinstance(goods, list):
        goods = [goods]

    clcs = {clc["rating"] for good in goods for clc in good.get("good", {}).get("control_list_entries", []) if clc}
    return sorted(clcs - {None})


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
def get_third_party(third_parties, id):
    return [party for party in third_parties if party["id"] == id]


@register.inclusion_tag("advice/group-advice.html", takes_context=True)
def group_advice(context):
    grouped_advice = []
    if context and context.get("case", {}).get("advice"):
        case = context.get("case")
        advice_by_team = services.group_advice_by_team(case["advice"])
        teams = sorted(
            {advice["user"]["team"]["id"]: advice["user"]["team"] for advice in case["advice"]}.values(),
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
            else:
                team_advice["decision"] = constants.TEAM_DECISION_APPROVED_REFUSED
