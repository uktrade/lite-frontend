import pytest
from unittest.mock import patch

from django.urls import reverse

from core import client
from caseworker.advice import forms, services


@pytest.fixture
def mock_post_team_advice(requests_mock, standard_case_pk):
    url = client._build_absolute_uri(f"/cases/{standard_case_pk}/team-advice/")
    yield requests_mock.post(url=url, json={})


@pytest.fixture
def mock_get_team_advice(requests_mock, standard_case_pk):
    url = client._build_absolute_uri(f"/cases/{standard_case_pk}/team-advice/")
    yield requests_mock.get(url=url, json={})


@pytest.fixture(autouse=True)
def setup(mock_queue, mock_case, mock_denial_reasons, mock_post_team_advice, mock_get_team_advice):
    yield


@pytest.fixture
def consolidated_advice(current_user):
    current_user["team"]["id"] = "2132131d-2432-423424"
    current_user["team"]["alias"] = services.LICENSING_UNIT_TEAM

    return [
        {
            "id": "a9206652-93be-4480-97cf-d7d52ba6e2b5",
            "user": current_user,
            "type": {"key": "approve", "value": "Approve"},
            "text": "meets the requirements",
            "note": "",
            "level": "final",
            "footnote": None,
            "footnote_required": None,
            "good": None,
            "end_user_id": "953f330f-4956-4e9f-9b87-7c07b5dc3abc",
            "ultimate_end_user_id": None,
            "consignee_id": None,
            "third_party_id": None,
            "proviso": "some conditions",
            "pv_grading": None,
            "collated_pv_grading": None,
            "countersign_comments": "",
            "countersigned_by_id": None,
        },
        {
            "id": "78833712-fc78-4a52-8616-37a72bfb1e2a",
            "user": current_user,
            "type": {"key": "approve", "value": "Approve"},
            "text": "meets the requirements",
            "note": "",
            "level": "final",
            "footnote": None,
            "footnote_required": None,
            "good_id": None,
            "goods_type_id": None,
            "country_id": None,
            "end_user_id": None,
            "ultimate_end_user_id": None,
            "consignee_id": "500abd5e-9c9c-4649-bcb4-e5156b39a715",
            "third_party_id": None,
            "proviso": "some conditions",
            "pv_grading": None,
            "collated_pv_grading": None,
            "countersign_comments": "",
            "countersigned_by_id": None,
        },
        {
            "id": "e6c1dbc5-4a39-48ad-84fd-c5d566c3b258",
            "user": current_user,
            "type": {"key": "approve", "value": "Approve"},
            "text": "meets the requirements",
            "note": "",
            "level": "final",
            "footnote": None,
            "footnote_required": None,
            "good_id": None,
            "goods_type_id": None,
            "country_id": None,
            "end_user_id": None,
            "ultimate_end_user_id": "e2ad9d86-c0b3-4560-a8e5-0d7e4cabac4f",
            "consignee_id": None,
            "third_party_id": None,
            "proviso": "some conditions",
            "pv_grading": None,
            "collated_pv_grading": None,
            "countersign_comments": "",
            "countersigned_by_id": None,
        },
        {
            "id": "da4149af-bee6-4d80-b647-f0b4027c9a0b",
            "case_id": "79b2a7f2-3cc1-40ef-a0c7-2517e1aff9a8",
            "user": current_user,
            "type": {"key": "approve", "value": "Approve"},
            "text": "meets the requirements",
            "note": "",
            "level": "final",
            "footnote": None,
            "footnote_required": None,
            "good_id": None,
            "goods_type_id": None,
            "country_id": None,
            "end_user_id": None,
            "ultimate_end_user_id": None,
            "consignee_id": None,
            "third_party_id": "cdb3e406-2760-47a4-ac08-06da333c20c9",
            "proviso": "some conditions",
            "pv_grading": None,
            "collated_pv_grading": None,
            "countersign_comments": "",
            "countersigned_by_id": None,
        },
        {
            "id": "1f8611f2-1e5a-4dbc-bbbe-776db26f8d24",
            "user": current_user,
            "type": {"key": "approve", "value": "Approve"},
            "text": "meets the requirements",
            "note": "",
            "level": "final",
            "footnote": None,
            "footnote_required": None,
            "good_id": "55b1e712-7031-47cb-a613-53ebbdc887ed",
            "goods_type_id": None,
            "country_id": None,
            "end_user_id": None,
            "ultimate_end_user_id": None,
            "consignee_id": None,
            "third_party_id": None,
            "proviso": "some conditions",
            "pv_grading": None,
            "collated_pv_grading": None,
            "countersign_comments": "",
            "countersigned_by_id": None,
        },
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
        },
        {
            "consignee": "cd2263b4-a427-4f14-8552-505e1d192bb8",
            "denial_reasons": ["1", "1a", "2", "2a", "2b", "M"],
            "footnote_required": False,
            "text": "doesn't meet the requirement",
            "type": "refuse",
        },
        {
            "type": "refuse",
            "text": "doesn't meet the requirement",
            "footnote_required": False,
            "ultimate_end_user": "9f077b3c-6116-4111-b9a0-b2491198aa72",
            "denial_reasons": ["1", "1a", "2", "2a", "2b", "M"],
        },
        {
            "denial_reasons": ["1", "1a", "2", "2a", "2b", "M"],
            "footnote_required": False,
            "text": "doesn't meet the requirement",
            "third_party": "95c2d6b7-5cfd-47e8-b3c8-dc76e1ac9747",
            "type": "refuse",
        },
        {
            "denial_reasons": ["1", "1a", "2", "2a", "2b", "M"],
            "footnote_required": False,
            "good": "9fbffa7f-ef50-402e-93ac-2f3f37d09030",
            "text": "doesn't meet the requirement",
            "type": "refuse",
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
    mock_get_gov_user.return_value = ({"user": {"team": {"id": "34344324-34234-432", "alias": team}}}, None)
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
        {"user": {"team": {"id": "34344324-34234-432", "alias": services.LICENSING_UNIT_TEAM}}},
        None,
    )
    requests_mock.put(client._build_absolute_uri(f"/cases/{case_data['case']['id']}/final-advice"), json={})

    data = {"approval_reasons": "meets the requirements updated", "proviso": "updated conditions"}
    response = authorized_client.post(url, data=data)
    assert response.status_code == 302
    history = requests_mock.request_history.pop()
    assert history.method == "PUT"
    assert history.json() == [
        {
            "id": "a9206652-93be-4480-97cf-d7d52ba6e2b5",
            "text": data["approval_reasons"],
            "proviso": data["proviso"],
        },
        {
            "id": "78833712-fc78-4a52-8616-37a72bfb1e2a",
            "text": data["approval_reasons"],
            "proviso": data["proviso"],
        },
        {
            "id": "e6c1dbc5-4a39-48ad-84fd-c5d566c3b258",
            "text": data["approval_reasons"],
            "proviso": data["proviso"],
        },
        {
            "id": "da4149af-bee6-4d80-b647-f0b4027c9a0b",
            "text": data["approval_reasons"],
            "proviso": data["proviso"],
        },
        {
            "id": "1f8611f2-1e5a-4dbc-bbbe-776db26f8d24",
            "text": data["approval_reasons"],
            "proviso": data["proviso"],
        },
    ]


@patch("caseworker.advice.views.get_gov_user")
def test_edit_consolidated_advice_refuse_by_lu_put(
    mock_get_gov_user,
    authorized_client,
    requests_mock,
    data_standard_case,
    url,
    consolidated_advice,
):
    for item in consolidated_advice:
        item["type"] = {"key": "refuse", "value": "Refuse"}

    case_data = data_standard_case
    case_data["case"]["advice"] = consolidated_advice

    mock_get_gov_user.return_value = (
        {"user": {"team": {"id": "34344324-34234-432", "alias": services.LICENSING_UNIT_TEAM}}},
        None,
    )
    requests_mock.put(client._build_absolute_uri(f"/cases/{case_data['case']['id']}/final-advice"), json={})

    data = {"refusal_reasons": "updating the decision to refuse", "denial_reasons": ["1", "2", "5"]}
    response = authorized_client.post(url, data=data)
    assert response.status_code == 302
    history = requests_mock.request_history.pop()
    assert history.method == "PUT"
    assert history.json() == [
        {
            "id": "a9206652-93be-4480-97cf-d7d52ba6e2b5",
            "text": data["refusal_reasons"],
            "denial_reasons": data["denial_reasons"],
        },
        {
            "id": "78833712-fc78-4a52-8616-37a72bfb1e2a",
            "text": data["refusal_reasons"],
            "denial_reasons": data["denial_reasons"],
        },
        {
            "id": "e6c1dbc5-4a39-48ad-84fd-c5d566c3b258",
            "text": data["refusal_reasons"],
            "denial_reasons": data["denial_reasons"],
        },
        {
            "id": "da4149af-bee6-4d80-b647-f0b4027c9a0b",
            "text": data["refusal_reasons"],
            "denial_reasons": data["denial_reasons"],
        },
        {
            "id": "1f8611f2-1e5a-4dbc-bbbe-776db26f8d24",
            "text": data["refusal_reasons"],
            "denial_reasons": data["denial_reasons"],
        },
    ]
