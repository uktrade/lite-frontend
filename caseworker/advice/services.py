from collections import defaultdict

from requests.exceptions import HTTPError

from core import client

# Queues
FCDO_CASES_TO_REVIEW_QUEUE = "f458094c-1fed-4222-ac70-ff5fa20ff649"
FCDO_COUNTERSIGNING_QUEUE = "5e772575-9ae4-4a16-b55b-7e1476d810c4"
MOD_CASES_TO_REVIEW_QUEUE = "a4c5bd9d-0d06-4856-abe1-c71d73abe636"
MOD_CONSOLIDATE_QUEUES = [
    "0dd6c6f0-8f8b-4c03-b68f-0d8b04225369",
    "a84d6556-782e-4002-abe2-8bc1e5c2b162",
    "1a5f47ee-ef5e-456b-914c-4fa629b4559c",
    "93d1bc19-979d-4ba3-a57c-b0ce253c6237",
]
LU_POST_CIRC_FINALISE_QUEUE = "f0e7c2fa-100f-42ad-b740-bb072393e664"

# Teams
FCDO_TEAM = "67b9a4a3-6f3d-4511-8a19-23ccff221a74"
LICENSING_UNIT_TEAM = "58e77e47-42c8-499f-a58d-94f94541f8c6"
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
        if not item.get("good"):
            result[item["user"]["team"]["id"]].append(item)
    return result


def get_advice_to_countersign(advice, caseworker):
    advice_by_team = filter_advice_by_users_team(advice, caseworker)
    user_advice = filter_advice_by_level(advice_by_team, ["user"])
    grouped_user_advice = group_advice_by_user(user_advice)
    return grouped_user_advice


def get_countersigners(advice_to_countersign):
    """Get a set of user ids representing the users that have already
    countersigned the advice supplied by `advice_to_countersign`.
    """
    countersigned_by = set()
    for user_advice in advice_to_countersign.values():
        for advice in user_advice:
            if advice["countersigned_by"]:
                countersigned_by.add(advice["countersigned_by"]["id"])
    return countersigned_by


def get_advice_to_consolidate(advice, user_team_id):
    """For MOD consolidate, we need to be able to review advice from other
    teams - which is the only difference between this function and
    `get_advice_to_countersign`.
    """
    if user_team_id == LICENSING_UNIT_TEAM:
        # LU needs to review the consolidated advice given by MOD which is at team level
        user_team_advice = filter_advice_by_level(advice, ["user", "team"])
        advice_from_teams = filter_advice_by_teams(user_team_advice, LU_CONSOLIDATE_TEAMS)
    elif user_team_id == MOD_ECJU_TEAM:
        user_advice = filter_advice_by_level(advice, ["user"])
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
    case_pk = case["id"]
    advice_to_countersign = get_advice_to_countersign(case.advice, caseworker)

    for index, (_, user_advice) in enumerate(advice_to_countersign.items()):
        form_data = formset_data[index]
        comments = form_data["approval_reasons"]
        for advice in user_advice:
            data.append({"id": advice["id"], "countersigned_by": caseworker["id"], "countersign_comments": comments})

    response = client.put(request, f"/cases/{case_pk}/countersign-advice/", data)
    response.raise_for_status()


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


def get_advice_tab_context(case, caseworker, queue_id):
    """Get contextual information for the advice tab such as the tab's URL and
    button visibility, based off the case, the current user and current user's queue.
    """
    team_id = caseworker["team"]["id"]

    # The default context
    context = {
        # The URL that the advice tab should go to when clicked
        "url": "cases:advice_view",
        # Booleans that determine button visibility
        "buttons": {
            "make_recommendation": False,
            "edit_recommendation": False,
            "clear_recommendation": False,
            "review_and_countersign": False,
            "review_and_combine": False,
            "move_case_forward": False,
        },
    }

    if team_id in (FCDO_TEAM, *MOD_CONSOLIDATE_TEAMS):
        if queue_id in (FCDO_CASES_TO_REVIEW_QUEUE, *MOD_CONSOLIDATE_QUEUES):
            existing_advice = get_my_advice(case.advice, caseworker["id"])

            if not existing_advice:
                # An individual giving advice on a case for the first time
                context["buttons"]["make_recommendation"] = True
            else:
                # An individual accessing a case again after having given advice
                context["url"] = "cases:view_my_advice"
                context["buttons"]["edit_recommendation"] = True
                context["buttons"]["clear_recommendation"] = True
                context["buttons"]["move_case_forward"] = True

        elif queue_id == FCDO_COUNTERSIGNING_QUEUE:
            advice_to_countersign = get_advice_to_countersign(case.advice, caseworker)
            countersigned_by = get_countersigners(advice_to_countersign)

            if caseworker["id"] not in countersigned_by:
                # An individual countersigning advice on a case for the first time
                context["url"] = "cases:countersign_advice_view"
                context["buttons"]["review_and_countersign"] = True
            else:
                # An individual accessing the case after giving countersigned advice
                context["url"] = "cases:countersign_view"
                context["buttons"]["edit_recommendation"] = True
                context["buttons"]["move_case_forward"] = True

    elif team_id in (MOD_ECJU_TEAM, LICENSING_UNIT_TEAM):
        consolidated_advice = get_consolidated_advice(case.advice, team_id)

        if queue_id in (MOD_CASES_TO_REVIEW_QUEUE, LU_POST_CIRC_FINALISE_QUEUE):
            if not consolidated_advice:
                # An individual consolidating advice on a case for the first time
                context["url"] = "cases:consolidate_advice_view"
                context["buttons"]["review_and_combine"] = True
            else:
                # An individual accessing the case after consolidating advice
                context["url"] = "cases:consolidate_view"
                context["buttons"]["edit_recommendation"] = True
                context["buttons"]["move_case_forward"] = True

    return context
