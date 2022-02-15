import pytest
from unittest.mock import patch

from copy import deepcopy
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
