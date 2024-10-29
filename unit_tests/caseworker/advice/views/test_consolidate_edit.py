import copy

import pytest
from unittest.mock import patch
from uuid import uuid4

from bs4 import BeautifulSoup
from django.urls import reverse

from core import client
from caseworker.advice import forms, services
from caseworker.advice.constants import AdviceType
from unit_tests.caseworker.conftest import countersignatures_for_advice
from caseworker.advice.services import LICENSING_UNIT_TEAM, MOD_ECJU_TEAM

TEAM_ID = "34344324-34234-432"


@pytest.fixture
def mock_post_team_advice(requests_mock, standard_case_pk):
    url = client._build_absolute_uri(f"/cases/{standard_case_pk}/team-advice/")
    yield requests_mock.post(url=url, json={})


@pytest.fixture
def mock_get_team_advice(requests_mock, standard_case_pk):
    url = client._build_absolute_uri(f"/cases/{standard_case_pk}/team-advice/")
    yield requests_mock.get(url=url, json={})


@pytest.fixture(autouse=True)
def setup(
    mock_queue,
    mock_case,
    mock_denial_reasons,
    mock_approval_reason,
    mock_proviso,
    mock_footnote_details,
    mock_post_team_advice,
    mock_get_team_advice,
):
    yield


def get_advice_subjects(case):
    case_data = case["case"]["data"]
    parties = [
        ("consignee", case_data["consignee"]["id"]),
        ("end_user", case_data["end_user"]["id"]),
        ("ultimate_end_user", case_data["ultimate_end_users"][0]["id"]),
    ]
    goods = [("good", good["id"]) for good in case["case"]["data"]["goods"]]

    return parties + goods


@pytest.fixture
def consolidated_advice(data_standard_case, current_user, lu_team):
    current_user["team"] = lu_team
    subjects = get_advice_subjects(data_standard_case)

    return [
        {
            "id": str(uuid4()),
            "user": current_user,
            "team": lu_team,
            "type": {"key": "approve", "value": "Approve"},
            "text": "meets the requirements",
            "note": "",
            "level": "final",
            "footnote": None,
            "footnote_required": None,
            subject_type: subject_id,
            "proviso": "some conditions",
            "countersign_comments": "",
            "countersigned_by_id": None,
        }
        for subject_type, subject_id in subjects
    ]


@pytest.fixture
def url(data_queue, data_standard_case):
    return reverse(
        f"cases:consolidate_edit", kwargs={"queue_pk": data_queue["id"], "pk": data_standard_case["case"]["id"]}
    )


def test_edit_approve_advice_post(authorized_client, requests_mock, data_standard_case, standard_case_with_advice, url):
    case_data = data_standard_case
    case_data["case"]["data"]["goods"] = standard_case_with_advice["data"]["goods"]
    case_data["case"]["advice"] = standard_case_with_advice["advice"]
    for advice in case_data["case"]["advice"]:
        advice["level"] = "team"

    data = {"approval_reasons": "meets the requirements updated"}
    response = authorized_client.post(url, data=data)
    assert response.status_code == 302
    history = [item for item in requests_mock.request_history if "team-advice" in item.url]
    assert len(history) == 1
    history = history[0]
    assert history.method == "POST"
    assert history.json() == [
        {
            "denial_reasons": [],
            "end_user": "95d3ea36-6ab9-41ea-a744-7284d17b9cc5",
            "footnote": "",
            "footnote_required": False,
            "note": "",
            "proviso": "",
            "text": "meets the requirements updated",
            "type": "approve",
        },
        {
            "consignee": "cd2263b4-a427-4f14-8552-505e1d192bb8",
            "denial_reasons": [],
            "footnote": "",
            "footnote_required": False,
            "note": "",
            "proviso": "",
            "text": "meets the requirements updated",
            "type": "approve",
        },
        {
            "denial_reasons": [],
            "footnote": "",
            "footnote_required": False,
            "note": "",
            "proviso": "",
            "text": "meets the requirements updated",
            "ultimate_end_user": "9f077b3c-6116-4111-b9a0-b2491198aa72",
            "type": "approve",
        },
        {
            "denial_reasons": [],
            "footnote": "",
            "footnote_required": False,
            "note": "",
            "proviso": "",
            "text": "meets the requirements updated",
            "third_party": "95c2d6b7-5cfd-47e8-b3c8-dc76e1ac9747",
            "type": "approve",
        },
        {
            "denial_reasons": [],
            "footnote": "",
            "footnote_required": False,
            "good": "9fbffa7f-ef50-402e-93ac-2f3f37d09030",
            "note": "",
            "proviso": "",
            "text": "meets the requirements updated",
            "type": "approve",
        },
        {
            "denial_reasons": [],
            "footnote": "",
            "footnote_required": False,
            "good": "d4feac1e-851d-41a5-b833-eb28addb8547",
            "note": "",
            "proviso": "",
            "text": "",
            "type": "no_licence_required",
        },
    ]


def test_edit_refuse_advice_post(
    authorized_client, requests_mock, data_standard_case, standard_case_with_advice, refusal_advice, url
):
    case_data = data_standard_case
    case_data["case"]["data"]["goods"] = standard_case_with_advice["data"]["goods"]
    case_data["case"]["advice"] = refusal_advice
    for advice in case_data["case"]["advice"]:
        advice["level"] = "team"

    data = {
        "refusal_reasons": "doesn't meet the requirement",
        "denial_reasons": ["1", "1a", "2", "2a", "2b", "M"],
    }
    response = authorized_client.post(url, data=data)
    assert response.status_code == 302
    history = requests_mock.request_history.pop()
    assert "team-advice" in history.url
    assert history.method == "POST"
    assert history.json() == [
        {
            "denial_reasons": ["1", "1a", "2", "2a", "2b", "M"],
            "end_user": "95d3ea36-6ab9-41ea-a744-7284d17b9cc5",
            "footnote_required": False,
            "text": "doesn't meet the requirement",
            "type": "refuse",
            "is_refusal_note": False,
        },
        {
            "consignee": "cd2263b4-a427-4f14-8552-505e1d192bb8",
            "denial_reasons": ["1", "1a", "2", "2a", "2b", "M"],
            "footnote_required": False,
            "text": "doesn't meet the requirement",
            "type": "refuse",
            "is_refusal_note": False,
        },
        {
            "type": "refuse",
            "text": "doesn't meet the requirement",
            "footnote_required": False,
            "ultimate_end_user": "9f077b3c-6116-4111-b9a0-b2491198aa72",
            "denial_reasons": ["1", "1a", "2", "2a", "2b", "M"],
            "is_refusal_note": False,
        },
        {
            "denial_reasons": ["1", "1a", "2", "2a", "2b", "M"],
            "footnote_required": False,
            "text": "doesn't meet the requirement",
            "third_party": "95c2d6b7-5cfd-47e8-b3c8-dc76e1ac9747",
            "type": "refuse",
            "is_refusal_note": False,
        },
        {
            "denial_reasons": ["1", "1a", "2", "2a", "2b", "M"],
            "footnote_required": False,
            "good": "9fbffa7f-ef50-402e-93ac-2f3f37d09030",
            "text": "doesn't meet the requirement",
            "type": "refuse",
            "is_refusal_note": False,
        },
        {
            "denial_reasons": [],
            "footnote": "",
            "footnote_required": False,
            "good": "d4feac1e-851d-41a5-b833-eb28addb8547",
            "note": "",
            "proviso": "",
            "text": "",
            "type": "no_licence_required",
        },
    ]


@pytest.mark.parametrize(
    "team, advice_level",
    ((services.LICENSING_UNIT_TEAM, "final"), (services.MOD_ECJU_TEAM, "team")),
)
@patch("caseworker.advice.views.get_gov_user")
def test_edit_advice_get(
    mock_get_gov_user,
    team,
    advice_level,
    authorized_client,
    requests_mock,
    data_standard_case,
    standard_case_with_advice,
    refusal_advice,
    url,
):
    mock_get_gov_user.return_value = ({"user": {"team": {"id": TEAM_ID, "alias": team}}}, None)
    case_data = data_standard_case
    case_data["case"]["data"]["goods"] = standard_case_with_advice["data"]["goods"]
    # Add conflicting user advice
    case_data["case"]["advice"] = standard_case_with_advice["advice"] + refusal_advice
    # Add final advice
    for advice in standard_case_with_advice["advice"]:
        advice["level"] = advice_level
        advice["user"]["team"]["alias"] = team
    case_data["case"]["advice"] += standard_case_with_advice["advice"]

    response = authorized_client.get(url)
    form = response.context["form"]
    # The final advice was approval advice so we should see an approval form
    assert isinstance(form, forms.ConsolidateApprovalForm)


@patch("caseworker.advice.views.get_gov_user")
def test_edit_consolidated_advice_approve_by_lu_put(
    mock_get_gov_user,
    authorized_client,
    requests_mock,
    data_standard_case,
    url,
    consolidated_advice,
):
    case_data = data_standard_case
    case_data["case"]["advice"] = consolidated_advice

    mock_get_gov_user.return_value = (
        {"user": {"team": {"id": TEAM_ID, "alias": services.LICENSING_UNIT_TEAM}}},
        None,
    )
    requests_mock.put(client._build_absolute_uri(f"/cases/{case_data['case']['id']}/final-advice"), json={})

    data = {"approval_reasons": "meets the requirements updated", "proviso": "updated conditions"}
    response = authorized_client.post(url, data=data)
    assert response.status_code == 302
    history = requests_mock.request_history.pop()
    assert history.method == "PUT"
    assert history.json() == [
        {"id": advice["id"], "text": data["approval_reasons"], "proviso": data["proviso"], "type": "proviso"}
        for advice in consolidated_advice
    ]


@patch("caseworker.advice.views.get_gov_user")
def test_edit_consolidated_advice_approve__with_nlr_products_by_lu_put(
    mock_get_gov_user,
    authorized_client,
    requests_mock,
    data_standard_case,
    url,
    consolidated_advice,
):
    # Mark last item as NLR
    case_data = data_standard_case
    consolidated_advice[-1]["type"] = {"key": AdviceType.NO_LICENCE_REQUIRED, "value": "No licence required"}
    case_data["case"]["advice"] = consolidated_advice

    mock_get_gov_user.return_value = (
        {"user": {"team": {"id": TEAM_ID, "alias": services.LICENSING_UNIT_TEAM}}},
        None,
    )
    requests_mock.put(client._build_absolute_uri(f"/cases/{case_data['case']['id']}/final-advice"), json={})

    data = {"approval_reasons": "meets the requirements updated", "proviso": "updated conditions"}
    response = authorized_client.post(url, data=data)
    assert response.status_code == 302
    history = requests_mock.request_history.pop()
    assert history.method == "PUT"

    liceceable_products_advice = consolidated_advice[:-1]
    nlr_advice = consolidated_advice[-1]
    nlr_advice_data = [{"id": nlr_advice["id"], "text": "", "proviso": "", "note": "", "denial_reasons": []}]
    assert (
        history.json()
        == [
            {"id": advice["id"], "text": data["approval_reasons"], "proviso": data["proviso"], "type": "proviso"}
            for advice in liceceable_products_advice
        ]
        + nlr_advice_data
    )


@patch("caseworker.advice.views.get_gov_user")
def test_edit_consolidated_advice_refuse_note_by_lu_put(
    mock_get_gov_user,
    authorized_client,
    requests_mock,
    data_standard_case,
    url,
    consolidated_advice,
):
    for item in consolidated_advice:
        item["type"] = {"key": "refuse", "value": "Refuse"}
        item["is_refusal_note"] = True

    case_data = data_standard_case
    case_data["case"]["advice"] = consolidated_advice

    mock_get_gov_user.return_value = (
        {"user": {"team": {"id": TEAM_ID, "alias": services.LICENSING_UNIT_TEAM}}},
        None,
    )
    requests_mock.put(client._build_absolute_uri(f"/cases/{case_data['case']['id']}/final-advice"), json={})

    data = {"refusal_note": "updating the decision to refuse", "denial_reasons": ["1", "2", "5"]}
    response = authorized_client.post(url, data=data)
    assert response.status_code == 302
    history = requests_mock.request_history.pop()
    assert history.method == "PUT"
    assert history.json() == [
        {
            "id": advice["id"],
            "text": data["refusal_note"],
            "denial_reasons": data["denial_reasons"],
            "is_refusal_note": True,
        }
        for advice in consolidated_advice
    ]


@patch("caseworker.advice.views.get_gov_user")
def test_edit_consolidated_advice_by_LU_error_from_API(
    mock_get_gov_user,
    authorized_client,
    requests_mock,
    data_standard_case,
    url,
    consolidated_advice,
):
    case_data = data_standard_case
    case_data["case"]["advice"] = consolidated_advice

    mock_get_gov_user.return_value = (
        {"user": {"team": {"id": TEAM_ID, "alias": services.LICENSING_UNIT_TEAM}}},
        None,
    )
    requests_mock.put(
        client._build_absolute_uri(f"/cases/{case_data['case']['id']}/final-advice"),
        json={"errors": ["Failed to put"]},
        status_code=400,
    )

    data = {"approval_reasons": "meets the requirements updated", "proviso": "updated conditions"}
    response = authorized_client.post(url, data=data)
    assert response.status_code == 200
    assert "Failed to put" in response.content.decode("utf-8")


@pytest.mark.parametrize(
    "advice_type, expected_title",
    (
        ("FCDO", "Countersigned by FCDO User"),
        ("MOD", "Countersigned by MOD User"),
    ),
)
@patch("caseworker.advice.views.get_gov_user")
def test_edit_advice_get_displays_correct_counteradvice(
    mock_get_gov_user,
    authorized_client,
    data_standard_case,
    standard_case_with_advice,
    refusal_advice,
    url,
    fcdo_countersigned_advice,
    mod_countersigned_advice,
    advice_type,
    expected_title,
    lu_team,
):
    mock_get_gov_user.return_value = ({"user": {"team": lu_team}}, None)
    case_data = data_standard_case
    case_data["case"]["data"]["goods"] = standard_case_with_advice["data"]["goods"]
    # Add final advice
    for advice in standard_case_with_advice["advice"]:
        advice["level"] = "final"
        advice["user"]["team"] = lu_team
        advice["team"] = lu_team
    more_advice = copy.deepcopy(standard_case_with_advice["advice"])
    more_advice[0]["id"] = "d8cbfd81-290d-4c98-958b-621c0876dffc"
    case_data["case"]["advice"] += more_advice

    # Add some new-style countersignatures to the case.
    case_data["case"]["countersign_advice"] = countersignatures_for_advice(
        case_data["case"]["advice"],
        [
            {"order": services.FIRST_COUNTERSIGN, "outcome_accepted": True},
        ],
    )

    # Add FCDO/MOD advice with old-style countersignature
    fcdo_or_mod_advice = {"FCDO": fcdo_countersigned_advice, "MOD": mod_countersigned_advice}[advice_type]
    case_data["case"]["advice"] += fcdo_or_mod_advice

    response = authorized_client.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    countersignatures = soup.find_all(class_="countersignature-block")

    # Assert the correct countersignature is displayed.
    assert len(countersignatures) == 1
    assert countersignatures[0].find("h2").text == expected_title
    assert countersignatures[0].find("p").text == fcdo_or_mod_advice[0]["countersign_comments"]


@patch("caseworker.advice.views.get_gov_user")  # Pass to the mock version; mock_get_gov_user
def test_edit_refusal_note_exists(
    mock_get_gov_user,
    authorized_client,
    data_queue,
    data_standard_case,
    refusal_notes,
):
    data_standard_case["case"]["advice"] = refusal_notes
    mock_get_gov_user.return_value = (
        {"user": {"team": {"id": "21313212-23123-3123-323wq2", "alias": LICENSING_UNIT_TEAM}}},
        None,
    )
    url = reverse(
        f"cases:consolidate_edit", kwargs={"queue_pk": data_queue["id"], "pk": data_standard_case["case"]["id"]}
    )
    response = authorized_client.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    denial_element = soup.find("option", {"value": "2a", "selected": True})
    note_element = soup.find("textarea", {"id": "id_refusal_note"})

    assert denial_element["value"] == "2a"
    assert note_element.get_text(strip=True) == "The refusal note assess_1_2"


@patch("caseworker.advice.views.get_gov_user")  # Pass to the mock version; mock_get_gov_user
def test_mod_ecju_edit_exists(
    mock_get_gov_user,
    authorized_client,
    data_queue,
    data_standard_case,
    mod_ecju_refusal_reasons,
):
    data_standard_case["case"]["advice"] = mod_ecju_refusal_reasons
    mock_get_gov_user.return_value = (
        {"user": {"team": {"id": "21313212-23123-3123-323wq2", "alias": MOD_ECJU_TEAM}}},
        None,
    )
    url = reverse(
        f"cases:consolidate_edit", kwargs={"queue_pk": data_queue["id"], "pk": data_standard_case["case"]["id"]}
    )
    response = authorized_client.get(url)
    soup = BeautifulSoup(response.content, "html.parser")

    denial_element = soup.find("option", {"value": "5b", "selected": True})
    refusal_element = soup.find("textarea", {"id": "id_refusal_reasons"})

    assert denial_element["value"] == "5b"
    assert refusal_element.get_text(strip=True) == "something_test_1"
