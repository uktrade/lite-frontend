import pytest

from copy import deepcopy
from django.urls import reverse

from caseworker.advice import services
from core import client
from caseworker.advice.constants import AdviceSteps


@pytest.fixture(autouse=True)
def setup(mock_queue, mock_case, mock_denial_reasons, mock_approval_reason, mock_proviso, mock_footnote_details):
    yield


@pytest.fixture
def url(data_queue, data_standard_case):
    return reverse(
        f"cases:edit_advice_legacy", kwargs={"queue_pk": data_queue["id"], "pk": data_standard_case["case"]["id"]}
    )


def test_edit_approve_advice_post(authorized_client, requests_mock, data_standard_case, standard_case_with_advice, url):
    user_advice_create_url = f"/cases/{data_standard_case['case']['id']}/user-advice/"
    requests_mock.post(user_advice_create_url, json={})
    case_data = deepcopy(data_standard_case)
    case_data["case"]["data"]["goods"] = standard_case_with_advice["data"]["goods"]
    case_data["case"]["advice"] = standard_case_with_advice["advice"]

    requests_mock.get(client._build_absolute_uri(f"/cases/{data_standard_case['case']['id']}"), json=case_data)
    requests_mock.get(
        client._build_absolute_uri(f"/gov_users/{data_standard_case['case']['id']}"),
        json={"user": {"id": "58e62718-e889-4a01-b603-e676b794b394"}},
    )

    data = {
        "approval_reasons": "meets the requirements updated",
        "instructions_to_exporter": "no specific instructions",
    }
    response = authorized_client.post(url, data=data)
    assert response.status_code == 302
    history = [item for item in requests_mock.request_history if user_advice_create_url in item.url]
    assert len(history) == 1
    history = history[0]
    assert history.method == "POST"
    assert history.json() == [
        {
            "denial_reasons": [],
            "end_user": "95d3ea36-6ab9-41ea-a744-7284d17b9cc5",
            "footnote": "",
            "footnote_required": False,
            "note": "no specific instructions",
            "proviso": "",
            "text": "meets the requirements updated",
            "type": "approve",
        },
        {
            "consignee": "cd2263b4-a427-4f14-8552-505e1d192bb8",
            "denial_reasons": [],
            "footnote": "",
            "footnote_required": False,
            "note": "no specific instructions",
            "proviso": "",
            "text": "meets the requirements updated",
            "type": "approve",
        },
        {
            "ultimate_end_user": "9f077b3c-6116-4111-b9a0-b2491198aa72",
            "denial_reasons": [],
            "footnote": "",
            "footnote_required": False,
            "note": "no specific instructions",
            "proviso": "",
            "text": "meets the requirements updated",
            "type": "approve",
        },
        {
            "denial_reasons": [],
            "footnote": "",
            "footnote_required": False,
            "note": "no specific instructions",
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
            "note": "no specific instructions",
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
    authorized_client,
    requests_mock,
    data_standard_case,
    standard_case_with_advice,
    refusal_advice,
    url,
    mock_denial_reasons,
):
    user_advice_create_url = f"/cases/{data_standard_case['case']['id']}/user-advice/"
    requests_mock.post(user_advice_create_url, json={})
    case_data = deepcopy(data_standard_case)
    case_data["case"]["data"]["goods"] = standard_case_with_advice["data"]["goods"]
    case_data["case"]["advice"] = refusal_advice

    requests_mock.get(client._build_absolute_uri(f"/cases/{data_standard_case['case']['id']}"), json=case_data)
    requests_mock.get(
        client._build_absolute_uri(f"/gov_users/{data_standard_case['case']['id']}"),
        json={"user": {"id": "58e62718-e889-4a01-b603-e676b794b394"}},
    )

    data = {
        "refusal_reasons": "doesn't meet the requirement",
        "denial_reasons": ["3", "4", "5", "5a", "5b"],
    }
    response = authorized_client.post(url, data=data)
    assert response.status_code == 302
    history = requests_mock.request_history.pop()
    assert user_advice_create_url in history.url
    assert history.method == "POST"
    assert history.json() == [
        {
            "denial_reasons": ["3", "4", "5", "5a", "5b"],
            "end_user": "95d3ea36-6ab9-41ea-a744-7284d17b9cc5",
            "footnote_required": False,
            "text": "doesn't meet the requirement",
            "type": "refuse",
            "is_refusal_note": False,
        },
        {
            "consignee": "cd2263b4-a427-4f14-8552-505e1d192bb8",
            "denial_reasons": ["3", "4", "5", "5a", "5b"],
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
            "denial_reasons": ["3", "4", "5", "5a", "5b"],
            "is_refusal_note": False,
        },
        {
            "denial_reasons": ["3", "4", "5", "5a", "5b"],
            "footnote_required": False,
            "text": "doesn't meet the requirement",
            "third_party": "95c2d6b7-5cfd-47e8-b3c8-dc76e1ac9747",
            "type": "refuse",
            "is_refusal_note": False,
        },
        {
            "denial_reasons": ["3", "4", "5", "5a", "5b"],
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


def test_edit_refuse_advice_get(
    authorized_client, requests_mock, data_standard_case, standard_case_with_advice, refusal_advice, url, mock_gov_user
):
    case_data = deepcopy(data_standard_case)
    case_data["case"]["data"]["goods"] = standard_case_with_advice["data"]["goods"]
    case_data["case"]["advice"] = refusal_advice

    requests_mock.get(client._build_absolute_uri(f"/cases/{data_standard_case['case']['id']}"), json=case_data)
    requests_mock.get(
        client._build_absolute_uri(f"/gov_users/{data_standard_case['case']['id']}"),
        json={"user": {"id": "58e62718-e889-4a01-b603-e676b794b394"}},
    )
    response = authorized_client.get(url)
    assert response.context["security_approvals_classified_display"] == "F680"
    assert response.context["edit"] is True
    assert response.context["current_user"] == mock_gov_user["user"]


@pytest.fixture
def url_desnz(data_queue, data_standard_case):
    return reverse(f"cases:edit_advice", kwargs={"queue_pk": data_queue["id"], "pk": data_standard_case["case"]["id"]})


@pytest.fixture
def post_to_step(post_to_step_factory, url_desnz):
    return post_to_step_factory(url_desnz)


def test_DESNZ_give_approval_advice_post_valid(
    authorized_client,
    requests_mock,
    data_standard_case,
    url,
    mock_approval_reason,
    mock_proviso,
    mock_footnote_details,
    mock_post_advice,
    standard_case_with_advice,
    post_to_step,
    beautiful_soup,
    mocker,
):
    get_gov_user_value = (
        {
            "user": {
                "team": {
                    "id": "58e62718-e889-4a01-b603-e676b794b394",
                    "name": "DESNZ Chemical",
                    "alias": services.DESNZ_CHEMICAL,
                }
            }
        },
        None,
    )
    mocker.patch("caseworker.advice.views.mixins.get_gov_user", return_value=get_gov_user_value)
    case_data = deepcopy(data_standard_case)
    case_data["case"]["data"]["goods"] = standard_case_with_advice["data"]["goods"]
    case_data["case"]["advice"] = standard_case_with_advice["advice"]

    requests_mock.get(client._build_absolute_uri(f"/cases/{data_standard_case['case']['id']}"), json=case_data)
    requests_mock.get(
        client._build_absolute_uri(f"/gov_users/{data_standard_case['case']['id']}"),
        json={"user": {"id": "58e62718-e889-4a01-b603-e676b794b394"}},
    )

    response = post_to_step(
        AdviceSteps.RECOMMEND_APPROVAL,
        {"approval_reasons": "reason updated", "add_licence_conditions": False},
    )
    assert response.status_code == 302
    history = mock_post_advice.request_history
    assert len(history) == 1
    history = history[0]
    assert history.method == "POST"
    assert history.json() == [
        {
            "type": "approve",
            "text": "reason updated",
            "proviso": "",
            "note": "",
            "footnote_required": False,
            "footnote": "",
            "end_user": "95d3ea36-6ab9-41ea-a744-7284d17b9cc5",
            "denial_reasons": [],
        },
        {
            "type": "approve",
            "text": "reason updated",
            "proviso": "",
            "note": "",
            "footnote_required": False,
            "footnote": "",
            "consignee": "cd2263b4-a427-4f14-8552-505e1d192bb8",
            "denial_reasons": [],
        },
        {
            "type": "approve",
            "text": "reason updated",
            "proviso": "",
            "note": "",
            "footnote_required": False,
            "footnote": "",
            "ultimate_end_user": "9f077b3c-6116-4111-b9a0-b2491198aa72",
            "denial_reasons": [],
        },
        {
            "type": "approve",
            "text": "reason updated",
            "proviso": "",
            "note": "",
            "footnote_required": False,
            "footnote": "",
            "third_party": "95c2d6b7-5cfd-47e8-b3c8-dc76e1ac9747",
            "denial_reasons": [],
        },
        {
            "type": "approve",
            "text": "reason updated",
            "proviso": "",
            "note": "",
            "footnote_required": False,
            "footnote": "",
            "good": "9fbffa7f-ef50-402e-93ac-2f3f37d09030",
            "denial_reasons": [],
        },
        {
            "type": "no_licence_required",
            "text": "",
            "proviso": "",
            "note": "",
            "footnote_required": False,
            "footnote": "",
            "good": "d4feac1e-851d-41a5-b833-eb28addb8547",
            "denial_reasons": [],
        },
    ]


def test_DESNZ_give_approval_advice_post_valid_add_conditional(
    authorized_client,
    requests_mock,
    data_standard_case,
    url,
    mock_approval_reason,
    mock_proviso,
    mock_footnote_details,
    mock_post_advice,
    standard_case_with_advice,
    post_to_step,
    beautiful_soup,
    mocker,
):
    get_gov_user_value = (
        {
            "user": {
                "team": {
                    "id": "58e62718-e889-4a01-b603-e676b794b394",
                    "name": "DESNZ Chemical",
                    "alias": services.DESNZ_CHEMICAL,
                }
            }
        },
        None,
    )
    mocker.patch("caseworker.advice.views.mixins.get_gov_user", return_value=get_gov_user_value)
    case_data = deepcopy(data_standard_case)
    case_data["case"]["data"]["goods"] = standard_case_with_advice["data"]["goods"]
    case_data["case"]["advice"] = standard_case_with_advice["advice"]

    requests_mock.get(client._build_absolute_uri(f"/cases/{data_standard_case['case']['id']}"), json=case_data)
    requests_mock.get(
        client._build_absolute_uri(f"/gov_users/{data_standard_case['case']['id']}"),
        json={"user": {"id": "58e62718-e889-4a01-b603-e676b794b394"}},
    )

    response = post_to_step(
        AdviceSteps.RECOMMEND_APPROVAL,
        {"approval_reasons": "reason updated", "add_licence_conditions": True},
    )
    assert response.status_code == 200
    soup = beautiful_soup(response.content)
    # redirected to next form
    header = soup.find("h1")
    assert header.text == "Add licence conditions, instructions to exporter or footnotes (optional)"

    add_licence_condition_response = post_to_step(
        AdviceSteps.LICENCE_CONDITIONS,
        {"proviso": "proviso updated"},
    )
    assert add_licence_condition_response.status_code == 200
    soup = beautiful_soup(add_licence_condition_response.content)
    # redirected to next form
    header = soup.find("h1")
    assert header.text == "Instructions for the exporter (optional)"

    add_instructions_response = post_to_step(
        AdviceSteps.LICENCE_FOOTNOTES,
        {"instructions_to_exporter": "instructions updated", "footnote_details": "footnotes updated"},
    )
    assert add_instructions_response.status_code == 302
    history = mock_post_advice.request_history
    assert len(history) == 1
    history = history[0]
    assert history.method == "POST"
    assert history.json() == [
        {
            "type": "proviso",
            "text": "reason updated",
            "proviso": "proviso updated",
            "note": "instructions updated",
            "footnote_required": True,
            "footnote": "footnotes updated",
            "end_user": "95d3ea36-6ab9-41ea-a744-7284d17b9cc5",
            "denial_reasons": [],
        },
        {
            "type": "proviso",
            "text": "reason updated",
            "proviso": "proviso updated",
            "note": "instructions updated",
            "footnote_required": True,
            "footnote": "footnotes updated",
            "consignee": "cd2263b4-a427-4f14-8552-505e1d192bb8",
            "denial_reasons": [],
        },
        {
            "type": "proviso",
            "text": "reason updated",
            "proviso": "proviso updated",
            "note": "instructions updated",
            "footnote_required": True,
            "footnote": "footnotes updated",
            "ultimate_end_user": "9f077b3c-6116-4111-b9a0-b2491198aa72",
            "denial_reasons": [],
        },
        {
            "type": "proviso",
            "text": "reason updated",
            "proviso": "proviso updated",
            "note": "instructions updated",
            "footnote_required": True,
            "footnote": "footnotes updated",
            "third_party": "95c2d6b7-5cfd-47e8-b3c8-dc76e1ac9747",
            "denial_reasons": [],
        },
        {
            "type": "proviso",
            "text": "reason updated",
            "proviso": "proviso updated",
            "note": "instructions updated",
            "footnote_required": True,
            "footnote": "footnotes updated",
            "good": "9fbffa7f-ef50-402e-93ac-2f3f37d09030",
            "denial_reasons": [],
        },
        {
            "type": "no_licence_required",
            "text": "",
            "proviso": "",
            "note": "",
            "footnote_required": False,
            "footnote": "",
            "good": "d4feac1e-851d-41a5-b833-eb28addb8547",
            "denial_reasons": [],
        },
    ]
