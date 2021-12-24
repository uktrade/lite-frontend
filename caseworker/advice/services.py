from collections import defaultdict

from requests.exceptions import HTTPError

from core import client
from caseworker.cases.services import put_case_queues

FCDO_COUNTERSIGNING_QUEUE = "5e772575-9ae4-4a16-b55b-7e1476d810c4"

# Teams
FCDO_TEAM = "67b9a4a3-6f3d-4511-8a19-23ccff221a74"
LICENSING_UNIT_TEAM = "58e77e47-42c8-499f-a58d-94f94541f8c6"
FCO_TEAM = "67b9a4a3-6f3d-4511-8a19-23ccff221a74"
MOD_ECJU_TEAM = "b7640925-2577-4c24-8081-b85bd635b62a"
MOD_CONSOLIDATE_TEAMS = [
    "2e5fab3c-4599-432e-9540-74ccfafb18ee",
    "4c62ce4a-18f8-4ada-8d18-4b53a565250f",
    "809eba0f-f197-4f0f-949b-9af309a844fb",
    "a06aec31-47d7-443b-860d-66ab0c6d7cfd",
]
LU_CONSOLIDATE_TEAMS = [FCDO_TEAM, MOD_ECJU_TEAM]
# Flags
LU_COUNTERSIGN_REQUIRED = "bbf29b42-0aae-4ebc-b77a-e502ddea30a8"
LU_SR_MGR_CHECK_REQUIRED = "3e30f39c-ed82-41e9-b180-493a9fd0f169"


def filter_nlr_products(products):
    return [
        product
        for product in products
        if not product["is_good_controlled"] or product["is_good_controlled"]["key"] == "False"
    ]


def filter_current_user_advice(all_advice, user_id):
    return [
        advice
        for advice in all_advice
        if advice["level"] == "user"
        and advice["type"]["key"] in ["approve", "proviso", "refuse"]
        and (advice["user"]["id"] == user_id)
    ]


def filter_advice_by_type(all_advice, advice_types):
    return [advice for advice in all_advice if advice["type"]["key"] in advice_types]


def filter_advice_by_level(all_advice, advice_levels):
    return [advice for advice in all_advice if advice["level"] in advice_levels]


def filter_advice_by_user(all_advice, caseworker):
    return [advice for advice in all_advice if advice["user"]["id"] == caseworker["id"]]


def filter_advice_by_users_team(all_advice, caseworker):
    return [advice for advice in all_advice if advice["user"]["team"]["id"] == caseworker["team"]["id"]]


def filter_advice_by_team(all_advice, team_id):
    return [advice for advice in all_advice if advice["user"]["team"]["id"] == team_id]


def filter_advice_by_teams(all_advice, teams_list):
    advice_from_teams = []
    for team_id in teams_list:
        advice_from_teams.extend(filter_advice_by_team(all_advice, team_id))

    return advice_from_teams


def get_my_advice(advice, caseworker):
    user_level_advice = filter_advice_by_level(advice, ["user"])
    user_advice = filter_current_user_advice(user_level_advice, caseworker)
    grouped_user_advice = group_advice_by_user(user_advice)
    return grouped_user_advice


def group_advice_by_user(advice):
    """E.g. A case with 2 destinations and 2 goods, has 4 distinct
    advice-subjects. As a result, `post_approval_advice` &
    `post_refusal_advice` would create 4 advice records - one for
    each advice-subject and send it to the API.
    The flip side to this is that e.g. the countersigner will need
    to process each advice individually whereas according to the
    designs, he should process the advice from a given advisor
    as a whole.
    This function groups the advice by users so that e.g. for
    countersigning views etc. we can render this in a single block.
    TODO: This is functionally similar to `group_user_advice`
    method in `AdviceView`. We should delete that method and
    move to this one.
    TODO: This will break when we do approve-some-refuse-some.
    In that case, we will need to group approve & refuse advice
    from the same user separately i.e. group-by user & decision.
    """
    result = defaultdict(list)
    for item in advice:
        result[item["user"]["id"]].append(item)
    return result


def group_advice_by_team(advice):
    result = defaultdict(list)
    for item in advice:
        if not item["good"]:
            result[item["user"]["team"]["id"]].append(item)
    return result


def get_advice_to_countersign(advice, caseworker):
    advice_by_team = filter_advice_by_users_team(advice, caseworker)
    user_advice = filter_advice_by_level(advice_by_team, ["user"])
    grouped_user_advice = group_advice_by_user(user_advice)
    return grouped_user_advice


def get_advice_to_consolidate(advice, user_team_id):
    """For MOD consolidate, we need to be able to review advice from other
    teams - which is the only difference between this function and
    `get_advice_to_countersign`.
    """
    user_advice = filter_advice_by_level(advice, ["user"])
    if user_team_id == LICENSING_UNIT_TEAM:
        advice_from_teams = filter_advice_by_teams(user_advice, LU_CONSOLIDATE_TEAMS)
    elif user_team_id == MOD_ECJU_TEAM:
        advice_from_teams = filter_advice_by_teams(user_advice, MOD_CONSOLIDATE_TEAMS)
    else:
        raise Exception(f"Consolidate/combine operation not allowed for team {user_team_id}")

    return group_advice_by_user(advice_from_teams)


def order_by_party_type(all_advice):
    ordered_advice = []
    party_types = ("consignee", "end_user", "ultimate_end_user", "third_party")
    for party_type in party_types:
        for advice in all_advice:
            if advice.get(party_type) and advice not in ordered_advice:
                ordered_advice.append(advice)

    return ordered_advice


def get_consolidated_advice(advice, team_id):
    level = "final" if team_id == LICENSING_UNIT_TEAM else "team"
    team_advice = filter_advice_by_level(advice, [level])
    consolidated_advice = filter_advice_by_team(team_advice, team_id)
    return order_by_party_type(consolidated_advice)


def get_advice_subjects(case, countries=None):
    """The "advice subject" is an item on a case (eg a good, end user, consignee etc)
    that can have advice related to it. See lite-api/api/cases/models.py for foreign
    key fields on the Advice model.
    """
    destinations = []
    for dest in case.destinations:
        if countries is not None:
            if dest["country"]["id"] not in countries:
                continue
        destinations.append((dest["type"], dest["id"]))
    goods = [
        ("good", good["id"])
        for good in case.goods
        if (good.get("is_good_controlled") or {"key": None})["key"] == "True"
    ]
    return destinations + goods


def post_approval_advice(request, case, data, level="user-advice"):
    json = [
        {
            "type": "proviso" if data["proviso"] else "approve",
            "text": data["approval_reasons"],
            "proviso": data["proviso"],
            "note": data["instructions_to_exporter"],
            "footnote_required": True if data["footnote_details"] else False,
            "footnote": data["footnote_details"],
            subject_name: subject_id,
            "denial_reasons": [],
        }
        for subject_name, subject_id in get_advice_subjects(case, data.get("countries"))
    ]
    json_nlr_products = [
        {
            "type": "no_licence_required",
            "text": "",
            "proviso": "",
            "note": "",
            "footnote_required": False,
            "footnote": "",
            "good": good["id"],
            "denial_reasons": [],
        }
        for good in filter_nlr_products(case["data"]["goods"])
    ]
    response = client.post(request, f"/cases/{case['id']}/{level}/", json + json_nlr_products)
    response.raise_for_status()
    return response.json(), response.status_code


def post_refusal_advice(request, case, data, level="user-advice"):
    json = [
        {
            "type": "refuse",
            "text": data["refusal_reasons"],
            "footnote_required": False,
            subject_name: subject_id,
            "denial_reasons": data["denial_reasons"],
        }
        for subject_name, subject_id, in get_advice_subjects(case, data.get("countries"))
    ]
    response = client.post(request, f"/cases/{case['id']}/{level}/", json)
    response.raise_for_status()
    return response.json(), response.status_code


def delete_user_advice(request, case_pk):
    response = client.delete(request, f"/cases/{case_pk}/user-advice/")
    response.raise_for_status()
    return response.json(), response.status_code


def get_users_team_queues(request, user):
    response = client.get(request, f"/users/{user}/team-queues/")
    response.raise_for_status()
    return response.json(), response.status_code


def countersign_advice(request, case, caseworker, formset_data):
    data = []
    queues_to_return = set()
    case_pk = case["id"]
    advice_to_countersign = get_advice_to_countersign(case.advice, caseworker)

    for index, (_, user_advice) in enumerate(advice_to_countersign.items()):
        form_data = formset_data[index]
        comments = ""
        if form_data["agree_with_recommendation"] == "yes":
            comments = form_data["approval_reasons"]
        elif form_data["agree_with_recommendation"] == "no":
            comments = form_data["refusal_reasons"]
            queues_to_return.add(form_data["queue_to_return"])
        for advice in user_advice:
            data.append({"id": advice["id"], "countersigned_by": caseworker["id"], "countersign_comments": comments})

    response = client.put(request, f"/cases/{case_pk}/countersign-advice/", data)
    response.raise_for_status()

    # Remove the case from the FCO countersigning queue
    current_queues = set(case.queues) - {FCDO_COUNTERSIGNING_QUEUE}
    put_case_queues(request, case_pk, json={"queues": list(current_queues | queues_to_return)})

    return response.json(), response.status_code


def move_case_forward(request, case_id, queue_id):
    """This utility function calls the /assigned-queues/ endpoint in the API.
    In turn, /assigned-queues/ runs the routing rules and moves the case forward.
    """
    response = client.put(request, f"/cases/{case_id}/assigned-queues/", {"queues": [queue_id]})
    try:
        response.raise_for_status()
    except HTTPError as e:
        raise HTTPError(response=response) from e
    return response.json()
