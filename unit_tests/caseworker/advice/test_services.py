import pytest
import requests

from unittest.mock import patch

from caseworker.advice.services import (
    DESNZ_CHEMICAL_CASES_TO_REVIEW,
    DESNZ_NUCLEAR_CASES_TO_REVIEW,
    DESNZ_NUCLEAR_COUNTERSIGNING,
    FCDO_CASES_TO_REVIEW_QUEUE,
    FCDO_CPACC_CASES_TO_REVIEW_QUEUE,
    NCSC_CASES_TO_REVIEW,
    FCDO_COUNTERSIGNING_QUEUE,
    DESNZ_CHEMICAL,
    DESNZ_NUCLEAR,
    FCDO_TEAM,
    NCSC_TEAM,
    LICENSING_UNIT_TEAM,
    LU_POST_CIRC_FINALISE_QUEUE,
    LU_LICENSING_MANAGER_QUEUE,
    LU_SR_LICENSING_MANAGER_QUEUE,
    MOD_CASES_TO_REVIEW_QUEUES,
    MOD_CONSOLIDATE_QUEUES,
    MOD_CONSOLIDATE_TEAMS,
    MOD_ECJU_TEAM,
    filter_advice_by_users_team,
    filter_advice_by_team,
    filter_advice_by_teams,
    get_advice_tab_context,
    get_advice_to_countersign,
    get_decision_advices_by_countersigner,
    update_countersign_decision_advice,
    group_advice_by_team,
    update_advice,
)
from caseworker.cases.objects import Case
from uuid import uuid4


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
        for good_id in (
            "0bedd1c3-cf97-4aad-b711-d5c9a9f4586e",
            "6daad1c3-cf97-4aad-b711-d5c9a9f4586e",
            "56273dd4-4634-4ad7-a782-e480f85a85a9",
        )
    ]


@pytest.fixture
def advice_for_countersign(advice):
    for_countersign = []
    for item in advice:
        item["user"]["team"]["id"] = "2132131d-2432-423424"
        item["user"]["team"]["alias"] = LICENSING_UNIT_TEAM
        item["team"] = {
            "id": "2132131d-2432-423424",
            "alias": LICENSING_UNIT_TEAM,
        }
        item["level"] = "final"
        for_countersign.append(item)

    return for_countersign


@pytest.fixture
def countersign_advice(data_standard_case, advice_for_countersign, current_user):
    return [
        {
            "id": str(uuid4()),
            "valid": True,
            "order": 1,
            "outcome_accepted": True,
            "reasons": "reasons",
            "countersigned_user": current_user,
            "case": data_standard_case["case"]["id"],
            "advice": item["id"],
        }
        for item in advice_for_countersign
    ]


def test_get_advice_for_countersign_with_post_circ_countersigning(current_user, advice_for_countersign):
    countersign_advice = get_advice_to_countersign(advice_for_countersign, current_user)
    for user_id, advice in countersign_advice.items():
        assert user_id == current_user["id"]
        assert len(advice) == 3


# fmt: off
advice_tab_test_data = [
    # Fields: Has Advice, Advice Level, Countersigned, User Team, Current Queue, Expected Tab URL, Expected Buttons Enabled (dict)
    # An individual giving advice on a case for the first time
    (False, "user", False, DESNZ_CHEMICAL, DESNZ_CHEMICAL_CASES_TO_REVIEW, "cases:advice_view", {"make_recommendation": True},),
    (False, "user", False, DESNZ_NUCLEAR, DESNZ_NUCLEAR_CASES_TO_REVIEW, "cases:advice_view", {"make_recommendation": False, "assess_trigger_list_products": True},),
    (False, "user", False, FCDO_TEAM, FCDO_CASES_TO_REVIEW_QUEUE, "cases:advice_view", {"make_recommendation": True},),
    (False, "user", False, FCDO_TEAM, FCDO_CPACC_CASES_TO_REVIEW_QUEUE, "cases:advice_view", {"make_recommendation": True},),
    (False, "user", False, MOD_CONSOLIDATE_TEAMS[0], MOD_CONSOLIDATE_QUEUES[0], "cases:advice_view", {"make_recommendation": True},),
    (False, "user", False, MOD_CONSOLIDATE_TEAMS[0], MOD_CONSOLIDATE_QUEUES[1], "cases:advice_view", {"make_recommendation": True},),
    (False, "user", False, MOD_CONSOLIDATE_TEAMS[1], MOD_CONSOLIDATE_QUEUES[2], "cases:advice_view", {"make_recommendation": True},),
    (False, "user", False, MOD_CONSOLIDATE_TEAMS[2], MOD_CONSOLIDATE_QUEUES[3], "cases:advice_view", {"make_recommendation": True},),
    (False, "user", False, MOD_CONSOLIDATE_TEAMS[3], MOD_CONSOLIDATE_QUEUES[4], "cases:advice_view", {"make_recommendation": True},),
    (False, "user", False, NCSC_TEAM, NCSC_CASES_TO_REVIEW, "cases:advice_view", {"make_recommendation": True},),
    # An individual accessing the cases again after having given advice
    (True, "user", False, DESNZ_CHEMICAL, DESNZ_CHEMICAL_CASES_TO_REVIEW, "cases:view_my_advice", {"edit_recommendation": True, "clear_recommendation": True, "move_case_forward": True},),
    (True, "user", False, DESNZ_NUCLEAR, DESNZ_NUCLEAR_CASES_TO_REVIEW, "cases:view_my_advice", {"edit_recommendation": True, "clear_recommendation": True, "move_case_forward": True},),
    (True, "user", False, FCDO_TEAM, FCDO_CASES_TO_REVIEW_QUEUE, "cases:view_my_advice", {"edit_recommendation": True, "clear_recommendation": True, "move_case_forward": True},),
    (True, "user", False, FCDO_TEAM, FCDO_CPACC_CASES_TO_REVIEW_QUEUE, "cases:view_my_advice", {"edit_recommendation": True, "clear_recommendation": True, "move_case_forward": True},),
    (True, "user", False, MOD_CONSOLIDATE_TEAMS[0], MOD_CONSOLIDATE_QUEUES[0], "cases:view_my_advice", {"edit_recommendation": True, "clear_recommendation": True, "move_case_forward": True},),
    (True, "user", False, MOD_CONSOLIDATE_TEAMS[0], MOD_CONSOLIDATE_QUEUES[1], "cases:view_my_advice", {"edit_recommendation": True, "clear_recommendation": True, "move_case_forward": True},),
    (True, "user", False, MOD_CONSOLIDATE_TEAMS[1], MOD_CONSOLIDATE_QUEUES[2], "cases:view_my_advice", {"edit_recommendation": True, "clear_recommendation": True, "move_case_forward": True},),
    (True, "user", False, MOD_CONSOLIDATE_TEAMS[2], MOD_CONSOLIDATE_QUEUES[3], "cases:view_my_advice", {"edit_recommendation": True, "clear_recommendation": True, "move_case_forward": True},),
    (True, "user", False, MOD_CONSOLIDATE_TEAMS[3], MOD_CONSOLIDATE_QUEUES[4], "cases:view_my_advice", {"edit_recommendation": True, "clear_recommendation": True, "move_case_forward": True},),
    (True, "user", False, NCSC_TEAM, NCSC_CASES_TO_REVIEW, "cases:view_my_advice", {"edit_recommendation": True, "clear_recommendation": True, "move_case_forward": True},),
    # An individual countersigning advice on a case for the first time
    (True, "user", False, FCDO_TEAM, FCDO_COUNTERSIGNING_QUEUE, "cases:countersign_advice_view", {"review_and_countersign": True},),
    (True, "user", False, DESNZ_NUCLEAR, DESNZ_NUCLEAR_COUNTERSIGNING, "cases:countersign_advice_view", {"review_and_countersign": True},),
    # An LU caseworker trying to countersign advice on a case for the first time
    (True, "final", False, LICENSING_UNIT_TEAM, LU_LICENSING_MANAGER_QUEUE, "cases:advice_view", {"review_and_countersign": False},),
    (True, "final", False, LICENSING_UNIT_TEAM, LU_SR_LICENSING_MANAGER_QUEUE, "cases:advice_view", {"review_and_countersign": False},),
    # An individual accessing the case after giving countersigned advice
    (True, "user", True, DESNZ_NUCLEAR, DESNZ_NUCLEAR_COUNTERSIGNING, "cases:countersign_view", {"edit_recommendation": True, "move_case_forward": True},),
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


# fmt: off
countersign_advice_tab_test_data = [
    # Fields: Has Advice, Advice Level, Countersigned, User Team, Current Queue, Expected Tab URL, Expected Buttons Enabled (dict)
    # An LU caseworker trying to countersign advice on a case for the first time
    (True, "final", False, LICENSING_UNIT_TEAM, LU_LICENSING_MANAGER_QUEUE, "cases:countersign_advice_view", {"review_and_countersign": True},),
    (True, "final", False, LICENSING_UNIT_TEAM, LU_SR_LICENSING_MANAGER_QUEUE, "cases:countersign_advice_view", {"review_and_countersign": True},),
    (True, "final", True, LICENSING_UNIT_TEAM, LU_LICENSING_MANAGER_QUEUE, "cases:countersign_view", {"move_case_forward": True, "edit_recommendation": True},),
    (True, "final", True, LICENSING_UNIT_TEAM, LU_SR_LICENSING_MANAGER_QUEUE, "cases:countersign_view", {"move_case_forward": True, "edit_recommendation": True},),
]
# fmt: on


@pytest.mark.parametrize("test_data", countersign_advice_tab_test_data)
def test_get_countersign_advice_tab_context(
    advice,
    data_standard_case,
    current_user,
    countersign_advice,
    test_data,
):
    has_advice, advice_level, countersigned, team_alias, queue_alias, url, buttons = test_data
    queue_detail = data_standard_case["case"]["queue_details"][0]
    if has_advice:
        advice[0]["level"] = advice_level
        if countersigned:
            data_standard_case["case"]["countersign_advice"] = countersign_advice
        data_standard_case["case"]["advice"] = advice
    current_user["team"]["alias"] = team_alias
    queue_detail["alias"] = queue_alias
    context = get_advice_tab_context(Case(data_standard_case["case"]), current_user, queue_detail["id"])

    assert context["url"] == url

    for button_name, enabled in context["buttons"].items():
        assert buttons.get(button_name, False) == enabled


def test_get_decision_advices_by_countersigner(
    advice,
    data_standard_case,
    current_user,
    countersign_advice,
    LU_team_user,
    team1_user,
):
    # test incorrect team and also incorrect user are not included in results
    countersign_advice[0]["countersigned_user"] = LU_team_user
    countersign_advice[1]["countersigned_user"] = team1_user
    data_standard_case["case"]["countersign_advice"] = countersign_advice
    data_standard_case["case"]["advice"] = advice
    advices = get_decision_advices_by_countersigner(Case(data_standard_case["case"]), current_user)
    assert len(advices) == 1


def setup_requests_mock(requests_mock, client):
    requests_mock.requests_session = requests.Session()
    requests_mock.session = client.session
    requests_mock.headers = {}


def test_update_countersign_decision_advice(
    advice,
    data_standard_case,
    current_user,
    team1_user,
    LU_team_user,
    countersign_advice,
    client,
    requests_mock,
):
    case = Case(data_standard_case["case"])
    # incorrect team, advice not updated
    countersign_advice[0]["countersigned_user"] = team1_user
    # incorrect countersigner, advice not updated
    countersign_advice[1]["countersigned_user"] = LU_team_user
    case.countersign_advice = countersign_advice
    case.advice = advice
    data = {
        "outcome_accepted": False,
        "rejected_reasons": "this part can be used in H bombs",
    }
    countersign_advice_url = f"/cases/{case.id}/countersign-decision-advice/"
    setup_requests_mock(requests_mock, client)
    requests_mock.put(countersign_advice_url, json={})

    update_countersign_decision_advice(requests_mock, case, current_user, [data])

    assert requests_mock.called
    history = [item for item in requests_mock.request_history if countersign_advice_url in item.url]
    assert len(history) == 1
    history = history[0]
    assert history.method == "PUT"
    # only 1 of the 3 advices should be updated/
    assert history.json() == [
        {
            "id": countersign_advice[2]["id"],
            "outcome_accepted": data["outcome_accepted"],
            "reasons": data["rejected_reasons"],
        }
    ]


@patch("caseworker.advice.views.get_gov_user")
def test_update_advice_by_team_other_than_LU_raises_error(
    mock_get_gov_user,
    advice,
    data_standard_case,
    current_user,
    requests_mock,
):
    case = Case(data_standard_case["case"])
    case.advice = advice
    mock_get_gov_user.return_value = (
        {"user": {"team": {"id": "34344324-34234-432", "alias": FCDO_TEAM}}},
        None,
    )

    with pytest.raises(NotImplementedError):
        update_advice(requests_mock, case, current_user, "approve", {}, "final-advice")

    with pytest.raises(NotImplementedError):
        update_advice(requests_mock, case, current_user, "refuse", {}, "final-advice")


@patch("caseworker.advice.views.get_gov_user")
def test_update_advice_not_supported_advice_type_raises_error(
    mock_get_gov_user,
    advice,
    data_standard_case,
    current_user,
    requests_mock,
):
    case = Case(data_standard_case["case"])
    case.advice = advice
    mock_get_gov_user.return_value = (
        {"user": {"team": {"id": "34344324-34234-432", "alias": LICENSING_UNIT_TEAM}}},
        None,
    )

    with pytest.raises(NotImplementedError):
        update_advice(requests_mock, case, current_user, "no_licence_required", {}, "final-advice")


@pytest.mark.parametrize(
    "all_advice, caseworker, expected",
    (
        ([], {}, []),
        (
            [{"id": "advice_1", "team": {"id": "team_1"}}, {"id": "advice_2", "team": {"id": "team_2"}}],
            {"team": {"id": "team_1"}},
            [{"id": "advice_1", "team": {"id": "team_1"}}],
        ),
        (
            [
                {"id": "advice_1", "team": {"id": "team_1"}},
                {"id": "advice_2", "team": {"id": "team_2"}},
                {"id": "advice_3", "team": {"id": "team_2"}},
            ],
            {"team": {"id": "team_2"}},
            [{"id": "advice_2", "team": {"id": "team_2"}}, {"id": "advice_3", "team": {"id": "team_2"}}],
        ),
    ),
)
def test_filter_advice_by_users_team(all_advice, caseworker, expected):
    assert filter_advice_by_users_team(all_advice, caseworker) == expected


@pytest.mark.parametrize(
    "all_advice, team_alias, expected",
    (
        ([], "", []),
        (
            [{"id": "advice_1", "team": {"alias": "team_1"}}, {"id": "advice_2", "team": {"alias": "team_2"}}],
            "team_1",
            [{"id": "advice_1", "team": {"alias": "team_1"}}],
        ),
        (
            [
                {"id": "advice_1", "team": {"alias": "team_1"}},
                {"id": "advice_2", "team": {"alias": "team_2"}},
                {"id": "advice_3", "team": {"alias": "team_2"}},
            ],
            "team_2",
            [{"id": "advice_2", "team": {"alias": "team_2"}}, {"id": "advice_3", "team": {"alias": "team_2"}}],
        ),
    ),
)
def test_filter_advice_by_team(all_advice, team_alias, expected):
    assert filter_advice_by_team(all_advice, team_alias) == expected


@pytest.mark.parametrize(
    "all_advice, teams_list, expected",
    (
        ([], [""], []),
        (
            [{"id": "advice_1", "team": {"alias": "team_1"}}, {"id": "advice_2", "team": {"alias": "team_2"}}],
            ["team_1"],
            [{"id": "advice_1", "team": {"alias": "team_1"}}],
        ),
        (
            [
                {"id": "advice_1", "team": {"alias": "team_1"}},
                {"id": "advice_2", "team": {"alias": "team_2"}},
                {"id": "advice_3", "team": {"alias": "team_2"}},
            ],
            ["team_2"],
            [{"id": "advice_2", "team": {"alias": "team_2"}}, {"id": "advice_3", "team": {"alias": "team_2"}}],
        ),
        (
            [
                {"id": "advice_1", "team": {"alias": "team_1"}},
                {"id": "advice_2", "team": {"alias": "team_2"}},
                {"id": "advice_3", "team": {"alias": "team_2"}},
            ],
            ["team_1", "team_2"],
            [
                {"id": "advice_1", "team": {"alias": "team_1"}},
                {"id": "advice_2", "team": {"alias": "team_2"}},
                {"id": "advice_3", "team": {"alias": "team_2"}},
            ],
        ),
    ),
)
def test_filter_advice_by_teams(all_advice, teams_list, expected):
    assert filter_advice_by_teams(all_advice, teams_list) == expected


@pytest.mark.parametrize(
    "advice, expected",
    (
        ([], {}),
        ([{"id": "advice_1", "team": {"id": "team_1"}}], {"team_1": [{"id": "advice_1", "team": {"id": "team_1"}}]}),
        (
            [{"id": "advice_1", "team": {"id": "team_1"}}, {"id": "advice_2", "team": {"id": "team_2"}}],
            {
                "team_1": [{"id": "advice_1", "team": {"id": "team_1"}}],
                "team_2": [{"id": "advice_2", "team": {"id": "team_2"}}],
            },
        ),
        (
            [
                {"id": "advice_1", "team": {"id": "team_1"}},
                {"id": "advice_2", "team": {"id": "team_2"}},
                {"id": "advice_3", "team": {"id": "team_1"}},
            ],
            {
                "team_1": [{"id": "advice_1", "team": {"id": "team_1"}}, {"id": "advice_3", "team": {"id": "team_1"}}],
                "team_2": [{"id": "advice_2", "team": {"id": "team_2"}}],
            },
        ),
    ),
)
def test_group_advice_by_team(advice, expected):
    assert group_advice_by_team(advice) == expected
