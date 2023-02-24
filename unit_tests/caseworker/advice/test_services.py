import pytest

from caseworker.advice.services import (
    BEIS_CHEMICAL_CASES_TO_REVIEW,
    BEIS_NUCLEAR_CASES_TO_REVIEW,
    BEIS_NUCLEAR_COUNTERSIGNING,
    FCDO_CASES_TO_REVIEW_QUEUE,
    FCDO_CPACC_CASES_TO_REVIEW_QUEUE,
    FCDO_COUNTERSIGNING_QUEUE,
    BEIS_CHEMICAL,
    BEIS_NUCLEAR,
    FCDO_TEAM,
    LICENSING_UNIT_TEAM,
    LU_POST_CIRC_FINALISE_QUEUE,
    LU_LICENSING_MANAGER_QUEUE,
    LU_SR_LICENSING_MANAGER_QUEUE,
    MOD_CASES_TO_REVIEW_QUEUES,
    MOD_CONSOLIDATE_QUEUES,
    MOD_CONSOLIDATE_TEAMS,
    MOD_ECJU_TEAM,
    get_advice_tab_context,
    get_advice_to_countersign,
    get_countersigners_decision_advice,
)
from caseworker.cases.objects import Case


@pytest.fixture(autouse=True)
def setup(mock_queue, mock_case):
    yield


@pytest.fixture
def advice(current_user):
    return [
        {
            "consignee": "cd2263b4-a427-4f14-8552-505e1d192bb8",
            "country": None,
            "created_at": "2021-10-16T23:48:39.486679+01:00",
            "denial_reasons": [],
            "end_user": "95d3ea36-6ab9-41ea-a744-7284d17b9cc5",
            "footnote": "footnotes",
            "good": good_id,
            "id": "429c5596-fe8b-4540-988b-c37805cd08de",
            "level": "user",
            "note": "additional notes",
            "proviso": "no conditions",
            "text": "meets the criteria",
            "third_party": "95c2d6b7-5cfd-47e8-b3c8-dc76e1ac9747",
            "type": {"key": "proviso", "value": "Proviso"},
            "ultimate_end_user": None,
            "user": current_user,
            "countersigned_by": {},
        }
        for good_id in ("0bedd1c3-cf97-4aad-b711-d5c9a9f4586e", "6daad1c3-cf97-4aad-b711-d5c9a9f4586e")
    ]


@pytest.fixture
def advice_for_countersign(advice):
    for_countersign = []
    for item in advice:
        item["user"]["team"]["id"] = "2132131d-2432-423424"
        item["user"]["team"]["alias"] = LICENSING_UNIT_TEAM
        item["level"] = "final"
        for_countersign.append(item)

    return for_countersign


def test_get_advice_for_countersign_without_post_circ_countersigning(
    current_user, advice_for_countersign, with_lu_countersigning_disabled
):
    countersign_advice = get_advice_to_countersign(advice_for_countersign, current_user)
    assert len(countersign_advice) == 0


def test_get_advice_for_countersign_with_post_circ_countersigning(
    current_user, advice_for_countersign, with_lu_countersigning_enabled
):
    countersign_advice = get_advice_to_countersign(advice_for_countersign, current_user)
    for user_id, advice in countersign_advice.items():
        assert user_id == current_user["id"]
        assert len(advice) == 2


# fmt: off
advice_tab_test_data = [
    # Fields: Has Advice, Advice Level, Countersigned, User Team, Current Queue, Expected Tab URL, Expected Buttons Enabled (dict)
    # An individual giving advice on a case for the first time
    (False, "user", False, BEIS_CHEMICAL, BEIS_CHEMICAL_CASES_TO_REVIEW, "cases:advice_view", {"make_recommendation": True},),
    (False, "user", False, BEIS_NUCLEAR, BEIS_NUCLEAR_CASES_TO_REVIEW, "cases:advice_view", {"make_recommendation": False, "assess_trigger_list_products": True},),
    (False, "user", False, FCDO_TEAM, FCDO_CASES_TO_REVIEW_QUEUE, "cases:advice_view", {"make_recommendation": True},),
    (False, "user", False, FCDO_TEAM, FCDO_CPACC_CASES_TO_REVIEW_QUEUE, "cases:advice_view", {"make_recommendation": True},),
    (False, "user", False, MOD_CONSOLIDATE_TEAMS[0], MOD_CONSOLIDATE_QUEUES[0], "cases:advice_view", {"make_recommendation": True},),
    (False, "user", False, MOD_CONSOLIDATE_TEAMS[0], MOD_CONSOLIDATE_QUEUES[1], "cases:advice_view", {"make_recommendation": True},),
    (False, "user", False, MOD_CONSOLIDATE_TEAMS[1], MOD_CONSOLIDATE_QUEUES[2], "cases:advice_view", {"make_recommendation": True},),
    (False, "user", False, MOD_CONSOLIDATE_TEAMS[2], MOD_CONSOLIDATE_QUEUES[3], "cases:advice_view", {"make_recommendation": True},),
    (False, "user", False, MOD_CONSOLIDATE_TEAMS[3], MOD_CONSOLIDATE_QUEUES[4], "cases:advice_view", {"make_recommendation": True},),
    # An individual accessing the cases again after having given advice
    (True, "user", False, BEIS_CHEMICAL, BEIS_CHEMICAL_CASES_TO_REVIEW, "cases:view_my_advice", {"edit_recommendation": True, "clear_recommendation": True, "move_case_forward": True},),
    (True, "user", False, BEIS_NUCLEAR, BEIS_NUCLEAR_CASES_TO_REVIEW, "cases:view_my_advice", {"edit_recommendation": True, "clear_recommendation": True, "move_case_forward": True},),
    (True, "user", False, FCDO_TEAM, FCDO_CASES_TO_REVIEW_QUEUE, "cases:view_my_advice", {"edit_recommendation": True, "clear_recommendation": True, "move_case_forward": True},),
    (True, "user", False, FCDO_TEAM, FCDO_CPACC_CASES_TO_REVIEW_QUEUE, "cases:view_my_advice", {"edit_recommendation": True, "clear_recommendation": True, "move_case_forward": True},),
    (True, "user", False, MOD_CONSOLIDATE_TEAMS[0], MOD_CONSOLIDATE_QUEUES[0], "cases:view_my_advice", {"edit_recommendation": True, "clear_recommendation": True, "move_case_forward": True},),
    (True, "user", False, MOD_CONSOLIDATE_TEAMS[0], MOD_CONSOLIDATE_QUEUES[1], "cases:view_my_advice", {"edit_recommendation": True, "clear_recommendation": True, "move_case_forward": True},),
    (True, "user", False, MOD_CONSOLIDATE_TEAMS[1], MOD_CONSOLIDATE_QUEUES[2], "cases:view_my_advice", {"edit_recommendation": True, "clear_recommendation": True, "move_case_forward": True},),
    (True, "user", False, MOD_CONSOLIDATE_TEAMS[2], MOD_CONSOLIDATE_QUEUES[3], "cases:view_my_advice", {"edit_recommendation": True, "clear_recommendation": True, "move_case_forward": True},),
    (True, "user", False, MOD_CONSOLIDATE_TEAMS[3], MOD_CONSOLIDATE_QUEUES[4], "cases:view_my_advice", {"edit_recommendation": True, "clear_recommendation": True, "move_case_forward": True},),
    # An individual countersigning advice on a case for the first time
    (True, "user", False, FCDO_TEAM, FCDO_COUNTERSIGNING_QUEUE, "cases:countersign_advice_view", {"review_and_countersign": True},),
    (True, "user", False, BEIS_NUCLEAR, BEIS_NUCLEAR_COUNTERSIGNING, "cases:countersign_advice_view", {"review_and_countersign": True},),
    # An LU caseworker trying to countersign advice on a case for the first time
    (True, "final", False, LICENSING_UNIT_TEAM, LU_LICENSING_MANAGER_QUEUE, "cases:advice_view", {"review_and_countersign": False},),
    (True, "final", False, LICENSING_UNIT_TEAM, LU_SR_LICENSING_MANAGER_QUEUE, "cases:advice_view", {"review_and_countersign": False},),
    # An individual accessing the case after giving countersigned advice
    (True, "user", True, BEIS_NUCLEAR, BEIS_NUCLEAR_COUNTERSIGNING, "cases:countersign_view", {"edit_recommendation": True, "move_case_forward": True},),
    (True, "user", True, FCDO_TEAM, FCDO_COUNTERSIGNING_QUEUE, "cases:countersign_view", {"edit_recommendation": True, "move_case_forward": True},),
    # An individual consolidating advice on a case for the first time
    (True, "user", True, MOD_ECJU_TEAM, MOD_CASES_TO_REVIEW_QUEUES[0], "cases:consolidate_advice_view", {"review_and_combine": True},),
    (True, "user", True, MOD_ECJU_TEAM, MOD_CASES_TO_REVIEW_QUEUES[1], "cases:consolidate_advice_view", {"review_and_combine": True},),
    (True, "user", True, LICENSING_UNIT_TEAM, LU_POST_CIRC_FINALISE_QUEUE, "cases:consolidate_advice_view", {"review_and_combine": True},),
    # An individual accessing the case after consolidating advice
    (True, "team", True, MOD_ECJU_TEAM, MOD_CASES_TO_REVIEW_QUEUES[0], "cases:consolidate_view", {"edit_recommendation": True, "move_case_forward": True},),
    (True, "team", True, MOD_ECJU_TEAM, MOD_CASES_TO_REVIEW_QUEUES[1], "cases:consolidate_view", {"edit_recommendation": True, "move_case_forward": True},),
    (True, "final", True, LICENSING_UNIT_TEAM, LU_POST_CIRC_FINALISE_QUEUE, "cases:consolidate_view", {"edit_recommendation": True, "move_case_forward": True},),
    # Any individual accessing a case from any other queue (the fallback position)
    (True, "user", False, "any_team", "any_queue", "cases:advice_view", {},),
]
# fmt: on


def _test_get_advice_tab_context(
    advice,
    data_standard_case_with_potential_trigger_list_product,
    current_user,
    test_data,
):
    has_advice, advice_level, countersigned, team_alias, queue_alias, url, buttons = test_data
    queue_detail = data_standard_case_with_potential_trigger_list_product["case"]["queue_details"][0]
    if has_advice:
        advice[0]["level"] = advice_level
        if countersigned:
            advice[0]["countersigned_by"] = current_user
        data_standard_case_with_potential_trigger_list_product["case"]["advice"] = advice
    current_user["team"]["alias"] = team_alias
    queue_detail["alias"] = queue_alias
    context = get_advice_tab_context(
        Case(data_standard_case_with_potential_trigger_list_product["case"]), current_user, queue_detail["id"]
    )

    assert context["url"] == url

    for button_name, enabled in context["buttons"].items():
        assert buttons.get(button_name, False) == enabled


@pytest.mark.parametrize("test_data", advice_tab_test_data)
def test_get_advice_tab_context(
    advice,
    data_standard_case_with_potential_trigger_list_product,
    current_user,
    test_data,
    with_lu_countersigning_disabled,
):
    _test_get_advice_tab_context(
        advice, data_standard_case_with_potential_trigger_list_product, current_user, test_data
    )


# fmt: off
countersign_advice_tab_test_data = [
    # Fields: Has Advice, Advice Level, Countersigned, User Team, Current Queue, Expected Tab URL, Expected Buttons Enabled (dict)
    # An LU caseworker trying to countersign advice on a case for the first time
    (True, "final", False, LICENSING_UNIT_TEAM, LU_LICENSING_MANAGER_QUEUE, "cases:countersign_advice_view", {"review_and_countersign": True},),
    (True, "final", False, LICENSING_UNIT_TEAM, LU_SR_LICENSING_MANAGER_QUEUE, "cases:countersign_advice_view", {"review_and_countersign": True},),
]
# fmt: on


@pytest.mark.parametrize("test_data", countersign_advice_tab_test_data)
def test_get_countersign_advice_tab_context(
    advice,
    data_standard_case_with_potential_trigger_list_product,
    current_user,
    test_data,
    with_lu_countersigning_enabled,
):
    _test_get_advice_tab_context(
        advice, data_standard_case_with_potential_trigger_list_product, current_user, test_data
    )
