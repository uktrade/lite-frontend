from collections import defaultdict

from requests.exceptions import HTTPError

from core import client
from caseworker.advice import constants
from caseworker.advice.constants import AdviceType

# Queues
DESNZ_CHEMICAL_CASES_TO_REVIEW = "DESNZ_CHEMICAL_CASES_TO_REVIEW"
DESNZ_NUCLEAR_CASES_TO_REVIEW = "DESNZ_NUCLEAR_CASES_TO_REVIEW"
DESNZ_NUCLEAR_COUNTERSIGNING = "DESNZ_NUCLEAR_COUNTERSIGNING"
FCDO_CASES_TO_REVIEW_QUEUE = "FCDO_CASES_TO_REVIEW"
FCDO_CPACC_CASES_TO_REVIEW_QUEUE = "FCDO_CPACC_CASES_TO_REVIEW"
FCDO_COUNTERSIGNING_QUEUE = "FCDO_COUNTER_SIGNING"
NCSC_CASES_TO_REVIEW = "NCSC_CASES_TO_REVIEW"
MOD_CASES_TO_REVIEW_QUEUES = [
    "MOD_CASES_TO_REVIEW",
    "MOD_ECJU_REVIEW_AND_COMBINE",
]
MOD_CONSOLIDATE_QUEUES = [
    "MOD_DI_CASES_TO_REVIEW",
    "MOD_DI_DIRECT_CASES_TO_REVIEW",
    "MOD_DSR_CASES_TO_REVIEW",
    "MOD_DSTL_CASES_TO_REVIEW",
    "MOD_CAPPROT_CASES_TO_REVIEW",
    "MOD_ECJU_REVIEW_AND_COMBINE",
]
LU_POST_CIRC_FINALISE_QUEUE = "LU_POST_CIRC_FINALISE"
LU_LICENSING_MANAGER_QUEUE = "LU_LICENSING_MANAGER_QUEUE"
LU_SR_LICENSING_MANAGER_QUEUE = "LU_SR_LICENSING_MANAGER_QUEUE"

# Teams
DESNZ_CHEMICAL = "DESNZ_CHEMICAL"
DESNZ_NUCLEAR = "DESNZ_NUCLEAR"
DESNZ_TEAMS = [
    DESNZ_CHEMICAL,
    DESNZ_NUCLEAR,
]
FCDO_TEAM = "FCO"
LICENSING_UNIT_TEAM = "LICENSING_UNIT"
MOD_ECJU_TEAM = "MOD_ECJU"
MOD_CONSOLIDATE_TEAMS = [
    "MOD_DI",
    "MOD_DSR",
    "MOD_DSTL",
    "MOD_CAPPROT",
]
MOD_TEAMS = [MOD_ECJU_TEAM, *MOD_CONSOLIDATE_TEAMS]
LU_CONSOLIDATE_TEAMS = [FCDO_TEAM, MOD_ECJU_TEAM]
NCSC_TEAM = "NCSC"
OGD_TEAMS = [
    *BEIS_TEAMS,
    FCDO_TEAM,
    *MOD_TEAMS,
    NCSC_TEAM,
]

# Flags
LU_COUNTERSIGN_REQUIRED_ID = "bbf29b42-0aae-4ebc-b77a-e502ddea30a8"  # /PS-IGNORE
LU_SR_MGR_CHECK_REQUIRED_ID = "3e30f39c-ed82-41e9-b180-493a9fd0f169"  # /PS-IGNORE
MANPADS_ID = "a6bf56e8-dda7-491c-aa43-0edf249beca4"  # /PS-IGNORE
AP_LANDMINE_ID = "b8000761-14fa-4a6c-8532-6d21db337c2d"  # /PS-IGNORE

LU_COUNTERSIGN_FLAGS = {LU_COUNTERSIGN_REQUIRED_ID, LU_SR_MGR_CHECK_REQUIRED_ID}

NSG_POTENTIAL_TRIGGER_LIST_REGIME = "NSG Potential Trigger List"

# Countersigning
FIRST_COUNTERSIGN = 1
SECOND_COUNTERSIGN = 2


def filter_nlr_products(products):
    return [
        product
        for product in products
        if not product["is_good_controlled"] or product["is_good_controlled"]["key"] == "False"
    ]


def is_trigger_list_regime(product):
    return [
        regime_entry
        for regime_entry in product.get("regime_entries", [])
        if regime_entry["subsection"]["name"] == NSG_POTENTIAL_TRIGGER_LIST_REGIME
    ]


def is_trigger_list_assessed(product):
    """Returns True if a product has been assessed for trigger list criteria"""
    return product.get("is_trigger_list_guidelines_applicable") in [True, False]


def filter_trigger_list_products(products):
    """
    Returns list of products which are controlled and their regime entries
    match with potential trigger list regime
    """
    return [
        product
        for product in products
        if (product["is_good_controlled"] and product["is_good_controlled"]["key"] == "True")
        and is_trigger_list_regime(product)
    ]


def filter_current_user_advice(all_advice, user_id):
    return [
        advice
        for advice in all_advice
        if advice["level"] == constants.AdviceLevel.USER
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
    return [advice for advice in all_advice if advice["team"]["id"] == caseworker["team"]["id"]]


def filter_advice_by_team(all_advice, team_alias):
    return [advice for advice in all_advice if advice["team"]["alias"] == team_alias]


def filter_advice_by_teams(all_advice, teams_list):
    advice_from_teams = []
    for team_alias in teams_list:
        advice_from_teams.extend(filter_advice_by_team(all_advice, team_alias))

    return advice_from_teams


def filter_countersign_advice_by_order(countersign_advice, order):
    return [advice for advice in countersign_advice if advice["valid"] is True and advice["order"] == order]


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
            result[item["team"]["id"]].append(item)
    return result


def get_advice_to_countersign(advice, caseworker):
    advice_levels_to_countersign = [constants.AdviceLevel.USER]

    if caseworker["team"]["alias"] == LICENSING_UNIT_TEAM:
        advice_levels_to_countersign = [constants.AdviceLevel.FINAL]
    advice_by_team = filter_advice_by_users_team(advice, caseworker)
    user_advice = filter_advice_by_level(advice_by_team, advice_levels_to_countersign)
    grouped_user_advice = group_advice_by_user(user_advice)
    return grouped_user_advice


def get_countersign_decision_advice_by_user(case, caseworker):
    result = defaultdict(list)

    if caseworker["team"]["alias"] != LICENSING_UNIT_TEAM:
        return result

    for item in get_decision_advices_by_countersigner(case, caseworker):
        result[item["countersigned_user"]["id"]].append(item)

    return result


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


def get_countersigners_decision_advice(case, caseworker):
    """Get a set of user ids representing the users that have already
    countersigned the advice on this case with accept/reject decision.
    """
    countersigned_by = set()
    for advice in case.countersign_advice:
        if advice["valid"] is True and advice["countersigned_user"]["team"]["id"] == caseworker["team"]["id"]:
            countersigned_by.add(advice["countersigned_user"]["id"])
    return countersigned_by


def get_decision_advices_by_countersigner(case, caseworker):
    """Get users countersign advice on this case with accept/reject decision."""
    advices = []
    for advice in case.countersign_advice:
        if (
            advice["countersigned_user"]["team"]["id"] == caseworker["team"]["id"]
            and advice["countersigned_user"]["id"] == caseworker["id"]
        ):
            advices.append(advice)
    return advices


def get_advice_to_consolidate(advice, user_team_alias):
    """For MOD consolidate, we need to be able to review advice from other
    teams - which is the only difference between this function and
    `get_advice_to_countersign`.
    """

    if user_team_alias == LICENSING_UNIT_TEAM:
        # LU needs to review the consolidated advice given by MOD which is at team level
        user_team_advice = filter_advice_by_level(advice, [constants.AdviceLevel.USER, constants.AdviceLevel.TEAM])
        advice_from_teams = filter_advice_by_teams(user_team_advice, LU_CONSOLIDATE_TEAMS)
    elif user_team_alias == MOD_ECJU_TEAM:
        user_advice = filter_advice_by_level(advice, [constants.AdviceLevel.USER])
        advice_from_teams = filter_advice_by_teams(user_advice, MOD_CONSOLIDATE_TEAMS)
    else:
        raise Exception(f"Consolidate/combine operation not allowed for team {user_team_alias}")

    return group_advice_by_user(advice_from_teams)


def order_by_party_type(all_advice):
    ordered_advice = []
    party_types = ("consignee", "end_user", "ultimate_end_user", "third_party")
    for party_type in party_types:
        for advice in all_advice:
            if advice.get(party_type) and advice not in ordered_advice:
                ordered_advice.append(advice)

    return ordered_advice


def get_consolidated_advice(advice, team_alias):
    level = "final" if team_alias == LICENSING_UNIT_TEAM else "team"
    team_advice = filter_advice_by_level(advice, [level])
    consolidated_advice = filter_advice_by_team(team_advice, team_alias)
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
            "text": data["text"],
            "footnote_required": False,
            subject_name: subject_id,
            "denial_reasons": data["denial_reasons"],
            "is_refusal_note": data.get("is_refusal_note", False),
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


def update_advice(request, case, caseworker, advice_type, data, level):
    user_team_alias = caseworker["team"]["alias"]
    if user_team_alias != LICENSING_UNIT_TEAM:
        raise NotImplementedError(f"Implement approval advice update for {user_team_alias}")

    team_advice = filter_advice_by_level(case.advice, ["final"])
    consolidated_advice = filter_advice_by_team(team_advice, user_team_alias)
    licenceable_products_advice = [
        item for item in consolidated_advice if item["type"]["key"] != AdviceType.NO_LICENCE_REQUIRED
    ]
    nlr_products_advice = [
        item for item in consolidated_advice if item["type"]["key"] == AdviceType.NO_LICENCE_REQUIRED
    ]

    json = []
    if advice_type in (AdviceType.APPROVE, AdviceType.PROVISO):
        json = [
            {
                "id": advice["id"],
                "text": data["approval_reasons"],
                "proviso": data["proviso"],
                "type": AdviceType.PROVISO if data["proviso"] else AdviceType.APPROVE,
            }
            for advice in licenceable_products_advice
        ]
    elif advice_type == AdviceType.REFUSE:
        json = [
            {
                "id": advice["id"],
                "text": data["text"],
                "denial_reasons": data["denial_reasons"],
                "is_refusal_note": data.get("is_refusal_note", False),
            }
            for advice in licenceable_products_advice
        ]
    else:
        raise NotImplementedError(f"Implement advice update for advice type {advice_type}")

    json_nlr = [
        {
            "id": advice["id"],
            "text": "",
            "proviso": "",
            "note": "",
            "denial_reasons": [],
        }
        for advice in nlr_products_advice
    ]

    response = client.put(request, f"/cases/{case['id']}/{level}/", json + json_nlr)
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


def countersign_decision_advice(request, case, queue_id, caseworker, formset_data):
    data = []
    case_pk = case["id"]
    order = FIRST_COUNTERSIGN  # common case

    queue_alias = next((item["alias"] for item in case["queue_details"] if item["id"] == queue_id), None)
    # in some case second countersign required
    if queue_alias == LU_SR_LICENSING_MANAGER_QUEUE:
        order = SECOND_COUNTERSIGN

    advice_to_countersign = get_advice_to_countersign(case.advice, caseworker)
    for index, (_, user_advice) in enumerate(advice_to_countersign.items()):
        form_data = formset_data[index]
        for advice in user_advice:
            outcome_accepted = form_data["outcome_accepted"]
            if outcome_accepted:
                reasons = form_data["approval_reasons"]
            else:
                reasons = form_data["rejected_reasons"]

            data.append(
                {
                    "order": order,
                    "outcome_accepted": outcome_accepted,
                    "reasons": reasons,
                    "countersigned_user": caseworker["id"],
                    "case": case_pk,
                    "advice": advice["id"],
                }
            )

    response = client.post(request, f"/cases/{case_pk}/countersign-decision-advice/", data)
    response.raise_for_status()


def update_countersign_decision_advice(request, case, caseworker, formset_data):
    data = []
    case_pk = case["id"]
    countersign_advice = get_countersign_decision_advice_by_user(case, caseworker)
    for index, (_, countersign_advice_data) in enumerate(countersign_advice.items()):
        form_data = formset_data[index]
        data = [
            {
                "id": countersign_advice["id"],
                "outcome_accepted": form_data["outcome_accepted"],
                "reasons": (
                    form_data["approval_reasons"] if form_data["outcome_accepted"] else form_data["rejected_reasons"]
                ),
            }
            for countersign_advice in countersign_advice_data
        ]

    response = client.put(request, f"/cases/{case_pk}/countersign-decision-advice/", data)
    response.raise_for_status()
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


def post_trigger_list_assessment(request, case_id, data):
    response = client.put(request, f"/applications/{case_id}/goods-on-application", data)
    return response.json(), response.status_code


def unassessed_trigger_list_goods(case):
    return [
        product
        for product in filter_trigger_list_products(case["data"]["goods"])
        if not is_trigger_list_assessed(product)
    ]


def get_advice_tab_context(case, caseworker, queue_id):
    """Get contextual information for the advice tab such as the tab's URL and
    button visibility, based off the case, the current user and current user's queue.
    """
    team_alias = caseworker["team"]["alias"]
    queue_alias = next((item["alias"] for item in case["queue_details"] if item["id"] == queue_id), None)
    # The default context
    context = {
        # The URL that the advice tab should go to when clicked
        "url": "cases:advice_view",
        # Booleans that determine button visibility
        "buttons": {
            "edit_recommendation": False,
            "clear_recommendation": False,
            "review_and_countersign": False,
            "review_and_combine": False,
            "move_case_forward": False,
            "assess_trigger_list_products": False,
        },
    }
    if team_alias in (FCDO_TEAM, *MOD_CONSOLIDATE_TEAMS, *DESNZ_TEAMS, NCSC_TEAM):
        if queue_alias in (
            FCDO_CASES_TO_REVIEW_QUEUE,
            FCDO_CPACC_CASES_TO_REVIEW_QUEUE,
            *MOD_CONSOLIDATE_QUEUES,
            DESNZ_CHEMICAL_CASES_TO_REVIEW,
            DESNZ_NUCLEAR_CASES_TO_REVIEW,
            NCSC_CASES_TO_REVIEW,
        ):
            existing_advice = get_my_advice(case.advice, caseworker["id"])

            if existing_advice:
                # An individual accessing a case again after having given advice
                context["url"] = "cases:view_my_advice"
                context["buttons"]["edit_recommendation"] = True
                context["buttons"]["clear_recommendation"] = True
                context["buttons"]["move_case_forward"] = True

            # DESNZ Nuclear need to assess products first before giving recommendation
            if (team_alias == DESNZ_NUCLEAR) and (queue_alias == DESNZ_NUCLEAR_CASES_TO_REVIEW) and not existing_advice:
                context["buttons"]["assess_trigger_list_products"] = len(unassessed_trigger_list_goods(case)) > 0
        elif queue_alias == FCDO_COUNTERSIGNING_QUEUE or (queue_alias == DESNZ_NUCLEAR_COUNTERSIGNING):
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

    elif team_alias in (MOD_ECJU_TEAM, LICENSING_UNIT_TEAM):
        consolidated_advice = get_consolidated_advice(case.advice, team_alias)

        if queue_alias in (LU_LICENSING_MANAGER_QUEUE, LU_SR_LICENSING_MANAGER_QUEUE):
            advice_to_countersign = get_advice_to_countersign(case.advice, caseworker)
            countersigned_by = get_countersigners_decision_advice(case, caseworker)

            if advice_to_countersign:
                if caseworker["id"] not in countersigned_by:
                    # An individual countersigning advice on a case for the first time
                    context["url"] = "cases:countersign_advice_view"
                    context["countersign"] = True
                    context["buttons"]["review_and_countersign"] = True
                else:
                    # An individual accessing the case after giving countersigned advice
                    context["url"] = "cases:countersign_view"
                    context["buttons"]["edit_recommendation"] = True
                    context["buttons"]["move_case_forward"] = True

        elif queue_alias in (LU_POST_CIRC_FINALISE_QUEUE, *MOD_CASES_TO_REVIEW_QUEUES):
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


def unadvised_countries(caseworker, case):
    """Returns a dict of countries for which advice has not been given by the current user's team."""
    dest_types = constants.DESTINATION_TYPES
    advised_on = {
        # Map of destinations advised on -> team that gave the advice
        advice.get(dest_type): advice["user"]["team"]["id"]
        for dest_type in dest_types
        for advice in case.advice
        if advice.get(dest_type) is not None
    }
    return {
        dest["country"]["id"]: dest["country"]["name"]
        for dest in case.destinations
        # Don't include destinations already advised on by the current user's team
        if (dest["id"], caseworker["team"]["id"]) not in advised_on.items()
    }
