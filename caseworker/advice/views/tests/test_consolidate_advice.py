import pytest

from bs4 import BeautifulSoup
from django.urls import reverse

from core import client
from caseworker.advice.services import (
    LICENSING_UNIT_TEAM,
    MOD_ECJU_TEAM,
)


@pytest.fixture(autouse=True)
def setup(
    mock_queue,
    mock_case,
    mock_approval_reason,
    mock_denial_reasons,
    mock_proviso,
    mock_footnote_details,
):
    return


@pytest.fixture
def consolidate_select_decision_url(data_queue, data_standard_case):
    return reverse(
        "cases:consolidate_review", kwargs={"queue_pk": data_queue["id"], "pk": data_standard_case["case"]["id"]}
    )


@pytest.fixture
def consolidate_approve_url(data_queue, data_standard_case):
    return reverse(
        "cases:consolidate_approve",
        kwargs={"queue_pk": data_queue["id"], "pk": data_standard_case["case"]["id"]},
    )


@pytest.fixture
def consolidate_refuse_url(data_queue, data_standard_case):
    return reverse(
        "cases:consolidate_refuse",
        kwargs={"queue_pk": data_queue["id"], "pk": data_standard_case["case"]["id"]},
    )


@pytest.fixture
def lu_consolidate_refuse_url(data_queue, data_standard_case):
    return reverse(
        "cases:consolidate_refuse_lu",
        kwargs={"queue_pk": data_queue["id"], "pk": data_standard_case["case"]["id"]},
    )


@pytest.fixture
def consolidate_view_url(data_queue, data_standard_case):
    return reverse(
        "cases:consolidate_view",
        kwargs={"queue_pk": data_queue["id"], "pk": data_standard_case["case"]["id"]},
    )


@pytest.fixture
def advice_data(current_user):
    return {
        "consignee": "cd2263b4-a427-4f14-8552-505e1d192bb8",  # /PS-IGNORE
        "country": None,
        "created_at": "2021-10-16T23:48:39.486679+01:00",
        "denial_reasons": [],
        "end_user": "95d3ea36-6ab9-41ea-a744-7284d17b9cc5",
        "footnote": "footnotes",
        "good": None,
        "id": "429c5596-fe8b-4540-988b-c37805cd08de",  # /PS-IGNORE
        "level": "user",
        "note": "additional notes",
        "proviso": "no conditions",
        "text": "meets the criteria",
        "third_party": "95c2d6b7-5cfd-47e8-b3c8-dc76e1ac9747",
        "type": {"key": "approve", "value": "Approve"},
        "ultimate_end_user": None,
        "user": current_user,
        "team": {"id": "some-team", "alias": "FCO"},
    }


@pytest.fixture
def approval_advice(advice_data):
    return [
        {**advice_data.copy(), "good": good_id}
        for good_id in ("0bedd1c3-cf97-4aad-b711-d5c9a9f4586e", "6daad1c3-cf97-4aad-b711-d5c9a9f4586e")
    ]


@pytest.fixture
def mixed_advice(advice_data):
    return [
        {
            **advice_data.copy(),
            "good": "0bedd1c3-cf97-4aad-b711-d5c9a9f4586e",
            "type": {"key": "refuse", "value": "Refuse"},
        },
        {
            **advice_data.copy(),
            "good": "6daad1c3-cf97-4aad-b711-d5c9a9f4586e",
            "type": {"key": "approve", "value": "Approve"},
        },
    ]


@pytest.fixture
def gov_user():
    return {
        "user": {
            "id": "2a43805b-c082-47e7-9188-c8b3e1a83cb0",  # /PS-IGNORE
            "team": {
                "id": "211111b-c111-11e1-1111-1111111111a",
                "name": "Test",
                "alias": "TEST_1",
            },
        }
    }


@pytest.fixture
def lu_gov_user(requests_mock, gov_user):
    gov_user["user"]["team"]["name"] = "Licensing Unit"
    gov_user["user"]["team"]["alias"] = LICENSING_UNIT_TEAM

    requests_mock.get(
        client._build_absolute_uri("/gov-users/2a43805b-c082-47e7-9188-c8b3e1a83cb0"),  # /PS-IGNORE
        json=gov_user,
    )


@pytest.fixture
def mod_ecju_gov_user(requests_mock, gov_user):
    gov_user["user"]["team"]["name"] = "MOD-ECJU"
    gov_user["user"]["team"]["alias"] = MOD_ECJU_TEAM

    requests_mock.get(
        client._build_absolute_uri("/gov-users/2a43805b-c082-47e7-9188-c8b3e1a83cb0"),  # /PS-IGNORE
        json=gov_user,
    )


#################################
# ConsolidateSelectDecisionView
#################################


def test_ConsolidateSelectDecisionView_GET_team_not_allowed_raises_exception(
    authorized_client,
    consolidate_select_decision_url,
    mixed_advice,
    data_standard_case,
):
    data_standard_case["case"]["advice"] = mixed_advice

    with pytest.raises(Exception) as err:
        authorized_client.get(consolidate_select_decision_url)

    assert str(err.value) == "Consolidate/combine operation not allowed for team 00000000-0000-0000-0000-000000000001"


def test_ConsolidateSelectDecisionView_POST_team_not_allowed_raises_exception(
    authorized_client,
    consolidate_select_decision_url,
    mixed_advice,
    data_standard_case,
):
    data_standard_case["case"]["advice"] = mixed_advice

    with pytest.raises(Exception) as err:
        authorized_client.post(consolidate_select_decision_url)

    assert str(err.value) == "Consolidate/combine operation not allowed for team 00000000-0000-0000-0000-000000000001"


def test_ConsolidateSelectDecisionView_all_advice_approve_redirects(
    authorized_client,
    consolidate_select_decision_url,
    approval_advice,
    data_standard_case,
    consolidate_approve_url,
    lu_gov_user,
):
    data_standard_case["case"]["advice"] = approval_advice
    response = authorized_client.get(consolidate_select_decision_url, follow=False)
    assert response.status_code == 302
    assert response.url == consolidate_approve_url


def test_ConsolidateSelectDecisionView_lu_gov_user_GET(
    authorized_client,
    consolidate_select_decision_url,
    mixed_advice,
    data_standard_case,
    lu_gov_user,
):
    data_standard_case["case"]["advice"] = mixed_advice
    response = authorized_client.get(consolidate_select_decision_url, follow=False)
    assert response.status_code == 200
    assert (
        response.context["title"]
        == f"Review and combine case recommendation - {data_standard_case['case']['reference_code']} - {data_standard_case['case']['data']['organisation']['name']}"
    )


def test_ConsolidateSelectDecisionView_mod_ecju_gov_user_GET(
    authorized_client,
    consolidate_select_decision_url,
    mixed_advice,
    data_standard_case,
    mod_ecju_gov_user,
):
    data_standard_case["case"]["advice"] = mixed_advice
    response = authorized_client.get(consolidate_select_decision_url, follow=False)
    assert response.status_code == 200
    assert (
        response.context["title"]
        == f"Review and combine case recommendation - {data_standard_case['case']['reference_code']} - {data_standard_case['case']['data']['organisation']['name']}"
    )


def test_ConsolidateSelectDecisionView_POST_bad_data(
    authorized_client,
    consolidate_select_decision_url,
    mixed_advice,
    data_standard_case,
    lu_gov_user,
):
    data_standard_case["case"]["advice"] = mixed_advice
    response = authorized_client.post(consolidate_select_decision_url, data={})
    assert response.status_code == 200
    form = response.context["form"]
    assert form.errors == {"recommendation": ["Select if you approve or refuse"]}


def test_ConsolidateSelectDecisionView_POST_approve_success(
    authorized_client,
    consolidate_select_decision_url,
    mixed_advice,
    data_standard_case,
    lu_gov_user,
    consolidate_approve_url,
):
    data_standard_case["case"]["advice"] = mixed_advice
    response = authorized_client.post(consolidate_select_decision_url, data={"recommendation": "approve"}, follow=False)
    assert response.status_code == 302
    assert response.url == consolidate_approve_url


def test_ConsolidateSelectDecisionView_POST_refuse_success(
    authorized_client,
    consolidate_select_decision_url,
    mixed_advice,
    data_standard_case,
    mod_ecju_gov_user,
    consolidate_refuse_url,
):
    data_standard_case["case"]["advice"] = mixed_advice
    response = authorized_client.post(consolidate_select_decision_url, data={"recommendation": "refuse"}, follow=False)
    assert response.status_code == 302
    assert response.url == consolidate_refuse_url


def test_ConsolidateSelectDecisionView_POST_lu_refuse_success(
    authorized_client,
    consolidate_select_decision_url,
    mixed_advice,
    data_standard_case,
    lu_gov_user,
    lu_consolidate_refuse_url,
):
    data_standard_case["case"]["advice"] = mixed_advice
    response = authorized_client.post(consolidate_select_decision_url, data={"recommendation": "refuse"}, follow=False)
    assert response.status_code == 302
    assert response.url == lu_consolidate_refuse_url


########################
# ConsolidateApproveView
########################


def test_ConsolidateApproveView_GET_team_not_allowed_raises_exception(
    authorized_client,
    consolidate_approve_url,
    mixed_advice,
    data_standard_case,
):
    data_standard_case["case"]["advice"] = mixed_advice

    with pytest.raises(Exception) as err:
        authorized_client.get(consolidate_approve_url)

    assert str(err.value) == "Consolidate/combine operation not allowed for team 00000000-0000-0000-0000-000000000001"


def test_ConsolidateApproveView_POST_team_not_allowed_raises_exception(
    authorized_client,
    consolidate_approve_url,
    mixed_advice,
    data_standard_case,
):
    data_standard_case["case"]["advice"] = mixed_advice
    pass

    with pytest.raises(Exception) as err:
        authorized_client.post(consolidate_approve_url)

    assert str(err.value) == "Consolidate/combine operation not allowed for team 00000000-0000-0000-0000-000000000001"


def test_ConsolidateApproveView_lu_gov_user_GET(
    authorized_client,
    consolidate_approve_url,
    mixed_advice,
    data_standard_case,
    lu_gov_user,
):
    data_standard_case["case"]["advice"] = mixed_advice
    response = authorized_client.get(consolidate_approve_url, follow=False)
    assert response.status_code == 200
    assert (
        response.context["title"]
        == f"Review and combine case recommendation - {data_standard_case['case']['reference_code']} - {data_standard_case['case']['data']['organisation']['name']}"
    )


def test_ConsolidateApproveView_mod_ecju_gov_user_GET(
    authorized_client,
    consolidate_approve_url,
    mixed_advice,
    data_standard_case,
    mod_ecju_gov_user,
):
    data_standard_case["case"]["advice"] = mixed_advice
    response = authorized_client.get(consolidate_approve_url, follow=False)
    assert response.status_code == 200
    assert (
        response.context["title"]
        == f"Review and combine case recommendation - {data_standard_case['case']['reference_code']} - {data_standard_case['case']['data']['organisation']['name']}"
    )


def test_ConsolidateApproveView_GET_collated_provisos(
    authorized_client,
    consolidate_approve_url,
    mixed_advice,
    advice_data,
    data_standard_case,
    lu_gov_user,
):
    """
    Ensure that proviso is pre-filled from collecting provisos across all valid advice.
    """
    mixed_advice[0]["proviso"] = "condition 1"
    mixed_advice[1]["proviso"] = "condition 2"
    extra_advice = {
        **advice_data,
        "team": {"id": "mod-ecju-team", "alias": "MOD_ECJU"},
        "good": "6daad1c3-cf97-4aad-b711-d5c9a9f4586e",
        "type": {"key": "approve", "value": "Approve"},
        "proviso": "",
    }
    mixed_advice.append(extra_advice)
    data_standard_case["case"]["advice"] = mixed_advice

    response = authorized_client.get(consolidate_approve_url, follow=False)
    assert response.status_code == 200
    assert response.context["form"].initial == {"proviso": "condition 1\n\n--------\ncondition 2"}


def test_ConsolidateApproveView_GET_canned_snippets(
    authorized_client,
    consolidate_approve_url,
    mixed_advice,
    advice_data,
    data_standard_case,
    lu_gov_user,
):
    """
    Ensure that the canned snippets proviso component renders as expected.
    """
    mixed_advice[0]["proviso"] = "condition 1"
    mixed_advice[1]["proviso"] = "condition 2"
    extra_advice = {
        **advice_data,
        "team": {"id": "mod-ecju-team", "alias": "MOD_ECJU"},
        "good": "6daad1c3-cf97-4aad-b711-d5c9a9f4586e",
        "type": {"key": "approve", "value": "Approve"},
        "proviso": "",
    }
    mixed_advice.append(extra_advice)
    data_standard_case["case"]["advice"] = mixed_advice

    response = authorized_client.get(consolidate_approve_url, follow=False)
    assert response.status_code == 200
    soup = BeautifulSoup(response.content, "html.parser")
    assert "firearm serial numbers" in soup.find("div", {"id": "div_id_proviso_snippets"}).text
    assert soup.find("button", attrs={"data-snippet-key": "firearm_serial_numbers"}).text == "Add licence condition"
    assert (
        soup.find("script", {"id": "proviso"}).text
        == '{"firearm_serial_numbers": "Firearm serial numbers text", "no_release": "No release of capability details", "no_specifications": "No release of specifications"}'
    )


def test_ConsolidateApproveView_POST_bad_input(
    authorized_client,
    consolidate_approve_url,
    mixed_advice,
    data_standard_case,
    lu_gov_user,
):
    data_standard_case["case"]["advice"] = mixed_advice
    response = authorized_client.post(consolidate_approve_url, data={})
    assert response.status_code == 200
    form = response.context["form"]
    assert form.errors == {"approval_reasons": ["Enter a reason for approving"]}


@pytest.fixture
def mock_post_approval_final_advice(requests_mock, data_standard_case):
    return requests_mock.post(
        client._build_absolute_uri(f"/cases/{data_standard_case['case']['id']}/final-advice/"),
        json={},
    )


@pytest.fixture
def mock_post_approval_team_advice(requests_mock, data_standard_case):
    return requests_mock.post(
        client._build_absolute_uri(f"/cases/{data_standard_case['case']['id']}/team-advice/"),
        json={},
    )


@pytest.mark.parametrize(
    "approval_data, expected_post_data",
    (
        (
            {"approval_reasons": "yep, go for it"},
            [
                {
                    "denial_reasons": [],
                    "end_user": "95d3ea36-6ab9-41ea-a744-7284d17b9cc5",
                    "footnote": "",
                    "footnote_required": False,
                    "note": "",
                    "proviso": "",
                    "text": "yep, go for it",
                    "type": "approve",
                },
                {
                    "consignee": "cd2263b4-a427-4f14-8552-505e1d192bb8",  # /PS-IGNORE
                    "denial_reasons": [],
                    "footnote": "",
                    "footnote_required": False,
                    "note": "",
                    "proviso": "",
                    "text": "yep, go for it",
                    "type": "approve",
                },
                {
                    "denial_reasons": [],
                    "footnote": "",
                    "footnote_required": False,
                    "note": "",
                    "proviso": "",
                    "text": "yep, go for it",
                    "type": "approve",
                    "ultimate_end_user": "9f077b3c-6116-4111-b9a0-b2491198aa72",
                },
                {
                    "denial_reasons": [],
                    "footnote": "",
                    "footnote_required": False,
                    "note": "",
                    "proviso": "",
                    "text": "yep, go for it",
                    "third_party": "95c2d6b7-5cfd-47e8-b3c8-dc76e1ac9747",
                    "type": "approve",
                },
                {
                    "denial_reasons": [],
                    "footnote": "",
                    "footnote_required": False,
                    "good": "0bedd1c3-cf97-4aad-b711-d5c9a9f4586e",
                    "note": "",
                    "proviso": "",
                    "text": "yep, go for it",
                    "type": "approve",
                },
                {
                    "denial_reasons": [],
                    "footnote": "",
                    "footnote_required": False,
                    "good": "6daad1c3-cf97-4aad-b711-d5c9a9f4586e",
                    "note": "",
                    "proviso": "",
                    "text": "",
                    "type": "no_licence_required",
                },
            ],
        ),
        (
            {
                "approval_reasons": "yep, go for it",
                "proviso": "just consider this",
            },
            [
                {
                    "denial_reasons": [],
                    "end_user": "95d3ea36-6ab9-41ea-a744-7284d17b9cc5",
                    "footnote": "",
                    "footnote_required": False,
                    "note": "",
                    "proviso": "just consider this",
                    "text": "yep, go for it",
                    "type": "proviso",
                },
                {
                    "consignee": "cd2263b4-a427-4f14-8552-505e1d192bb8",  # /PS-IGNORE
                    "denial_reasons": [],
                    "footnote": "",
                    "footnote_required": False,
                    "note": "",
                    "proviso": "just consider this",
                    "text": "yep, go for it",
                    "type": "proviso",
                },
                {
                    "denial_reasons": [],
                    "footnote": "",
                    "footnote_required": False,
                    "note": "",
                    "proviso": "just consider this",
                    "text": "yep, go for it",
                    "type": "proviso",
                    "ultimate_end_user": "9f077b3c-6116-4111-b9a0-b2491198aa72",
                },
                {
                    "denial_reasons": [],
                    "footnote": "",
                    "footnote_required": False,
                    "note": "",
                    "proviso": "just consider this",
                    "text": "yep, go for it",
                    "third_party": "95c2d6b7-5cfd-47e8-b3c8-dc76e1ac9747",
                    "type": "proviso",
                },
                {
                    "denial_reasons": [],
                    "footnote": "",
                    "footnote_required": False,
                    "good": "0bedd1c3-cf97-4aad-b711-d5c9a9f4586e",
                    "note": "",
                    "proviso": "just consider this",
                    "text": "yep, go for it",
                    "type": "proviso",
                },
                {
                    "denial_reasons": [],
                    "footnote": "",
                    "footnote_required": False,
                    "good": "6daad1c3-cf97-4aad-b711-d5c9a9f4586e",
                    "note": "",
                    "proviso": "",
                    "text": "",
                    "type": "no_licence_required",
                },
            ],
        ),
    ),
)
def test_ConsolidateApproveView_lu_gov_user_POST_success(
    approval_data,
    expected_post_data,
    authorized_client,
    consolidate_approve_url,
    mixed_advice,
    data_standard_case,
    lu_gov_user,
    mock_post_approval_final_advice,
    consolidate_view_url,
):
    data_standard_case["case"]["advice"] = mixed_advice
    data_standard_case["case"]["data"]["goods"][0]["is_good_controlled"] = {"key": "True", "value": "Yes"}

    response = authorized_client.post(consolidate_approve_url, data=approval_data)
    assert response.status_code == 302
    assert response.url == consolidate_view_url
    assert len(mock_post_approval_final_advice.request_history) == 1
    assert mock_post_approval_final_advice.request_history[0].json() == expected_post_data


@pytest.mark.parametrize(
    "approval_data, expected_post_data",
    (
        (
            {"approval_reasons": "yep, go for it"},
            [
                {
                    "denial_reasons": [],
                    "end_user": "95d3ea36-6ab9-41ea-a744-7284d17b9cc5",
                    "footnote": "",
                    "footnote_required": False,
                    "note": "",
                    "proviso": "",
                    "text": "yep, go for it",
                    "type": "approve",
                },
                {
                    "consignee": "cd2263b4-a427-4f14-8552-505e1d192bb8",  # /PS-IGNORE
                    "denial_reasons": [],
                    "footnote": "",
                    "footnote_required": False,
                    "note": "",
                    "proviso": "",
                    "text": "yep, go for it",
                    "type": "approve",
                },
                {
                    "denial_reasons": [],
                    "footnote": "",
                    "footnote_required": False,
                    "note": "",
                    "proviso": "",
                    "text": "yep, go for it",
                    "type": "approve",
                    "ultimate_end_user": "9f077b3c-6116-4111-b9a0-b2491198aa72",
                },
                {
                    "denial_reasons": [],
                    "footnote": "",
                    "footnote_required": False,
                    "note": "",
                    "proviso": "",
                    "text": "yep, go for it",
                    "third_party": "95c2d6b7-5cfd-47e8-b3c8-dc76e1ac9747",
                    "type": "approve",
                },
                {
                    "denial_reasons": [],
                    "footnote": "",
                    "footnote_required": False,
                    "good": "0bedd1c3-cf97-4aad-b711-d5c9a9f4586e",
                    "note": "",
                    "proviso": "",
                    "text": "yep, go for it",
                    "type": "approve",
                },
                {
                    "denial_reasons": [],
                    "footnote": "",
                    "footnote_required": False,
                    "good": "6daad1c3-cf97-4aad-b711-d5c9a9f4586e",
                    "note": "",
                    "proviso": "",
                    "text": "",
                    "type": "no_licence_required",
                },
            ],
        ),
        (
            {
                "approval_reasons": "yep, go for it",
                "proviso": "just consider this",
            },
            [
                {
                    "denial_reasons": [],
                    "end_user": "95d3ea36-6ab9-41ea-a744-7284d17b9cc5",
                    "footnote": "",
                    "footnote_required": False,
                    "note": "",
                    "proviso": "just consider this",
                    "text": "yep, go for it",
                    "type": "proviso",
                },
                {
                    "consignee": "cd2263b4-a427-4f14-8552-505e1d192bb8",  # /PS-IGNORE
                    "denial_reasons": [],
                    "footnote": "",
                    "footnote_required": False,
                    "note": "",
                    "proviso": "just consider this",
                    "text": "yep, go for it",
                    "type": "proviso",
                },
                {
                    "denial_reasons": [],
                    "footnote": "",
                    "footnote_required": False,
                    "note": "",
                    "proviso": "just consider this",
                    "text": "yep, go for it",
                    "type": "proviso",
                    "ultimate_end_user": "9f077b3c-6116-4111-b9a0-b2491198aa72",
                },
                {
                    "denial_reasons": [],
                    "footnote": "",
                    "footnote_required": False,
                    "note": "",
                    "proviso": "just consider this",
                    "text": "yep, go for it",
                    "third_party": "95c2d6b7-5cfd-47e8-b3c8-dc76e1ac9747",
                    "type": "proviso",
                },
                {
                    "denial_reasons": [],
                    "footnote": "",
                    "footnote_required": False,
                    "good": "0bedd1c3-cf97-4aad-b711-d5c9a9f4586e",
                    "note": "",
                    "proviso": "just consider this",
                    "text": "yep, go for it",
                    "type": "proviso",
                },
                {
                    "denial_reasons": [],
                    "footnote": "",
                    "footnote_required": False,
                    "good": "6daad1c3-cf97-4aad-b711-d5c9a9f4586e",
                    "note": "",
                    "proviso": "",
                    "text": "",
                    "type": "no_licence_required",
                },
            ],
        ),
    ),
)
def test_ConsolidateApproveView_mod_ecju_gov_user_POST_success(
    approval_data,
    expected_post_data,
    authorized_client,
    consolidate_approve_url,
    mixed_advice,
    data_standard_case,
    mod_ecju_gov_user,
    mock_post_approval_team_advice,
    consolidate_view_url,
):
    data_standard_case["case"]["advice"] = mixed_advice
    data_standard_case["case"]["data"]["goods"][0]["is_good_controlled"] = {"key": "True", "value": "Yes"}

    response = authorized_client.post(consolidate_approve_url, data=approval_data)
    assert response.status_code == 302
    assert response.url == consolidate_view_url
    assert len(mock_post_approval_team_advice.request_history) == 1
    assert mock_post_approval_team_advice.request_history[0].json() == expected_post_data


@pytest.fixture
def mock_post_approval_team_advice_server_error(requests_mock, data_standard_case):
    return requests_mock.post(
        client._build_absolute_uri(f"/cases/{data_standard_case['case']['id']}/team-advice/"),
        json={},
        status_code=500,
    )


def test_ConsolidateApproveView_POST_server_error(
    authorized_client,
    consolidate_approve_url,
    mixed_advice,
    data_standard_case,
    mod_ecju_gov_user,
    mock_post_approval_team_advice_server_error,
):
    data_standard_case["case"]["advice"] = mixed_advice
    response = authorized_client.post(consolidate_approve_url, data={"approval_reasons": "yep, go for it"})
    assert response.status_code == 200
    form = response.context["form"]
    assert form.errors == {"__all__": ["An error occurred when saving consolidated advice"]}


########################
# ConsolidateRefuseView
########################


def test_ConsolidateRefuseView_GET_team_not_allowed_raises_exception(
    authorized_client,
    consolidate_refuse_url,
    mixed_advice,
    data_standard_case,
):
    data_standard_case["case"]["advice"] = mixed_advice

    with pytest.raises(Exception) as err:
        authorized_client.get(consolidate_refuse_url)

    assert str(err.value) == "Consolidate/combine operation not allowed for team 00000000-0000-0000-0000-000000000001"


def test_ConsolidateRefuseView_POST_team_not_allowed_raises_exception(
    authorized_client,
    consolidate_refuse_url,
    mixed_advice,
    data_standard_case,
):
    data_standard_case["case"]["advice"] = mixed_advice
    pass

    with pytest.raises(Exception) as err:
        authorized_client.post(consolidate_refuse_url)

    assert str(err.value) == "Consolidate/combine operation not allowed for team 00000000-0000-0000-0000-000000000001"


def test_ConsolidateRefuseView_GET(
    authorized_client,
    consolidate_refuse_url,
    mixed_advice,
    data_standard_case,
    mod_ecju_gov_user,
):
    data_standard_case["case"]["advice"] = mixed_advice
    response = authorized_client.get(consolidate_refuse_url, follow=False)
    assert response.status_code == 200
    assert (
        response.context["title"]
        == f"Licence refused for case - {data_standard_case['case']['reference_code']} - {data_standard_case['case']['data']['organisation']['name']}"
    )


def test_ConsolidateRefuseView_POST_bad_input(
    authorized_client,
    consolidate_refuse_url,
    mixed_advice,
    data_standard_case,
    mod_ecju_gov_user,
):
    data_standard_case["case"]["advice"] = mixed_advice
    response = authorized_client.post(consolidate_refuse_url, data={})
    assert response.status_code == 200
    form = response.context["form"]
    assert form.errors == {
        "denial_reasons": ["Select at least one refusal criteria"],
        "refusal_reasons": ["Enter a reason for refusing"],
    }


@pytest.fixture
def mock_post_refusal_team_advice(requests_mock, data_standard_case):
    return requests_mock.post(
        client._build_absolute_uri(f"/cases/{data_standard_case['case']['id']}/team-advice/"),
        json={},
    )


@pytest.mark.parametrize(
    "refusal_data, expected_post_data",
    (
        (
            {"denial_reasons": ["1"], "refusal_reasons": "you can't do that"},
            [
                {
                    "denial_reasons": ["1"],
                    "end_user": "95d3ea36-6ab9-41ea-a744-7284d17b9cc5",
                    "footnote_required": False,
                    "is_refusal_note": False,
                    "text": "you can't do that",
                    "type": "refuse",
                },
                {
                    "consignee": "cd2263b4-a427-4f14-8552-505e1d192bb8",  # /PS-IGNORE
                    "denial_reasons": ["1"],
                    "footnote_required": False,
                    "is_refusal_note": False,
                    "text": "you can't do that",
                    "type": "refuse",
                },
                {
                    "denial_reasons": ["1"],
                    "footnote_required": False,
                    "is_refusal_note": False,
                    "text": "you can't do that",
                    "type": "refuse",
                    "ultimate_end_user": "9f077b3c-6116-4111-b9a0-b2491198aa72",
                },
                {
                    "denial_reasons": ["1"],
                    "footnote_required": False,
                    "is_refusal_note": False,
                    "text": "you can't do that",
                    "third_party": "95c2d6b7-5cfd-47e8-b3c8-dc76e1ac9747",
                    "type": "refuse",
                },
                {
                    "denial_reasons": ["1"],
                    "footnote_required": False,
                    "good": "0bedd1c3-cf97-4aad-b711-d5c9a9f4586e",
                    "is_refusal_note": False,
                    "text": "you can't do that",
                    "type": "refuse",
                },
                {
                    "denial_reasons": [],
                    "footnote": "",
                    "footnote_required": False,
                    "good": "6daad1c3-cf97-4aad-b711-d5c9a9f4586e",
                    "note": "",
                    "proviso": "",
                    "text": "",
                    "type": "no_licence_required",
                },
            ],
        ),
        (
            {"denial_reasons": ["1", "2a"], "refusal_reasons": "you can't do that"},
            [
                {
                    "denial_reasons": ["1", "2a"],
                    "end_user": "95d3ea36-6ab9-41ea-a744-7284d17b9cc5",
                    "footnote_required": False,
                    "is_refusal_note": False,
                    "text": "you can't do that",
                    "type": "refuse",
                },
                {
                    "consignee": "cd2263b4-a427-4f14-8552-505e1d192bb8",  # /PS-IGNORE
                    "denial_reasons": ["1", "2a"],
                    "footnote_required": False,
                    "is_refusal_note": False,
                    "text": "you can't do that",
                    "type": "refuse",
                },
                {
                    "denial_reasons": ["1", "2a"],
                    "footnote_required": False,
                    "is_refusal_note": False,
                    "text": "you can't do that",
                    "type": "refuse",
                    "ultimate_end_user": "9f077b3c-6116-4111-b9a0-b2491198aa72",
                },
                {
                    "denial_reasons": ["1", "2a"],
                    "footnote_required": False,
                    "is_refusal_note": False,
                    "text": "you can't do that",
                    "third_party": "95c2d6b7-5cfd-47e8-b3c8-dc76e1ac9747",
                    "type": "refuse",
                },
                {
                    "denial_reasons": ["1", "2a"],
                    "footnote_required": False,
                    "good": "0bedd1c3-cf97-4aad-b711-d5c9a9f4586e",
                    "is_refusal_note": False,
                    "text": "you can't do that",
                    "type": "refuse",
                },
                {
                    "denial_reasons": [],
                    "footnote": "",
                    "footnote_required": False,
                    "good": "6daad1c3-cf97-4aad-b711-d5c9a9f4586e",
                    "note": "",
                    "proviso": "",
                    "text": "",
                    "type": "no_licence_required",
                },
            ],
        ),
    ),
)
def test_ConsolidateRefuseView_POST_success(
    refusal_data,
    expected_post_data,
    authorized_client,
    consolidate_refuse_url,
    mixed_advice,
    data_standard_case,
    mod_ecju_gov_user,
    mock_post_refusal_team_advice,
    consolidate_view_url,
):
    data_standard_case["case"]["advice"] = mixed_advice
    data_standard_case["case"]["data"]["goods"][0]["is_good_controlled"] = {"key": "True", "value": "Yes"}

    response = authorized_client.post(consolidate_refuse_url, data=refusal_data)
    assert response.status_code == 302
    assert response.url == consolidate_view_url
    assert len(mock_post_refusal_team_advice.request_history) == 1
    assert mock_post_refusal_team_advice.request_history[0].json() == expected_post_data


@pytest.fixture
def mock_post_refusal_team_advice_server_error(requests_mock, data_standard_case):
    return requests_mock.post(
        client._build_absolute_uri(f"/cases/{data_standard_case['case']['id']}/team-advice/"),
        json={},
        status_code=500,
    )


def test_ConsolidateRefuseView_POST_server_error(
    authorized_client,
    consolidate_refuse_url,
    mixed_advice,
    data_standard_case,
    mod_ecju_gov_user,
    mock_post_refusal_team_advice_server_error,
):
    data_standard_case["case"]["advice"] = mixed_advice
    response = authorized_client.post(
        consolidate_refuse_url, data={"denial_reasons": ["1", "2a"], "refusal_reasons": "you can't do that"}
    )
    assert response.status_code == 200
    form = response.context["form"]
    assert form.errors == {"__all__": ["An error occurred when saving consolidated advice"]}


# LUConsolidatRefuseView


def test_LUConsolidateRefuseView_GET_team_not_allowed_raises_exception(
    authorized_client,
    lu_consolidate_refuse_url,
    mixed_advice,
    data_standard_case,
):
    data_standard_case["case"]["advice"] = mixed_advice

    with pytest.raises(Exception) as err:
        authorized_client.get(lu_consolidate_refuse_url)

    assert str(err.value) == "Consolidate/combine operation not allowed for team 00000000-0000-0000-0000-000000000001"


def test_LUConsolidateRefuseView_POST_team_not_allowed_raises_exception(
    authorized_client,
    lu_consolidate_refuse_url,
    mixed_advice,
    data_standard_case,
):
    data_standard_case["case"]["advice"] = mixed_advice
    pass

    with pytest.raises(Exception) as err:
        authorized_client.post(lu_consolidate_refuse_url)

    assert str(err.value) == "Consolidate/combine operation not allowed for team 00000000-0000-0000-0000-000000000001"


def test_LUConsolidateRefuseView_GET(
    authorized_client,
    lu_consolidate_refuse_url,
    mixed_advice,
    data_standard_case,
    lu_gov_user,
):
    data_standard_case["case"]["advice"] = mixed_advice
    response = authorized_client.get(lu_consolidate_refuse_url, follow=False)
    assert response.status_code == 200
    assert (
        response.context["title"]
        == f"Licence refused for case - {data_standard_case['case']['reference_code']} - {data_standard_case['case']['data']['organisation']['name']}"
    )


def test_LUConsolidateRefuseView_POST_bad_input(
    authorized_client,
    lu_consolidate_refuse_url,
    mixed_advice,
    data_standard_case,
    lu_gov_user,
):
    data_standard_case["case"]["advice"] = mixed_advice
    response = authorized_client.post(lu_consolidate_refuse_url, data={})
    assert response.status_code == 200
    form = response.context["form"]
    assert form.errors == {
        "denial_reasons": ["Select at least one refusal criteria"],
        "refusal_note": ["Enter the refusal meeting note"],
    }


@pytest.fixture
def mock_post_refusal_final_advice(requests_mock, data_standard_case):
    return requests_mock.post(
        client._build_absolute_uri(f"/cases/{data_standard_case['case']['id']}/final-advice/"),
        json={},
    )


@pytest.mark.parametrize(
    "refusal_data, expected_post_data",
    (
        (
            {"denial_reasons": ["1"], "refusal_note": "LU says no"},
            [
                {
                    "denial_reasons": ["1"],
                    "end_user": "95d3ea36-6ab9-41ea-a744-7284d17b9cc5",
                    "footnote_required": False,
                    "is_refusal_note": True,
                    "text": "LU says no",
                    "type": "refuse",
                },
                {
                    "consignee": "cd2263b4-a427-4f14-8552-505e1d192bb8",  # /PS-IGNORE
                    "denial_reasons": ["1"],
                    "footnote_required": False,
                    "is_refusal_note": True,
                    "text": "LU says no",
                    "type": "refuse",
                },
                {
                    "denial_reasons": ["1"],
                    "footnote_required": False,
                    "is_refusal_note": True,
                    "text": "LU says no",
                    "type": "refuse",
                    "ultimate_end_user": "9f077b3c-6116-4111-b9a0-b2491198aa72",
                },
                {
                    "denial_reasons": ["1"],
                    "footnote_required": False,
                    "is_refusal_note": True,
                    "text": "LU says no",
                    "third_party": "95c2d6b7-5cfd-47e8-b3c8-dc76e1ac9747",
                    "type": "refuse",
                },
                {
                    "denial_reasons": ["1"],
                    "footnote_required": False,
                    "good": "0bedd1c3-cf97-4aad-b711-d5c9a9f4586e",
                    "is_refusal_note": True,
                    "text": "LU says no",
                    "type": "refuse",
                },
                {
                    "denial_reasons": [],
                    "footnote": "",
                    "footnote_required": False,
                    "good": "6daad1c3-cf97-4aad-b711-d5c9a9f4586e",
                    "note": "",
                    "proviso": "",
                    "text": "",
                    "type": "no_licence_required",
                },
            ],
        ),
        (
            {"denial_reasons": ["1", "2a"], "refusal_note": "LU says no"},
            [
                {
                    "denial_reasons": ["1", "2a"],
                    "end_user": "95d3ea36-6ab9-41ea-a744-7284d17b9cc5",
                    "footnote_required": False,
                    "is_refusal_note": True,
                    "text": "LU says no",
                    "type": "refuse",
                },
                {
                    "consignee": "cd2263b4-a427-4f14-8552-505e1d192bb8",  # /PS-IGNORE
                    "denial_reasons": ["1", "2a"],
                    "footnote_required": False,
                    "is_refusal_note": True,
                    "text": "LU says no",
                    "type": "refuse",
                },
                {
                    "denial_reasons": ["1", "2a"],
                    "footnote_required": False,
                    "is_refusal_note": True,
                    "text": "LU says no",
                    "type": "refuse",
                    "ultimate_end_user": "9f077b3c-6116-4111-b9a0-b2491198aa72",
                },
                {
                    "denial_reasons": ["1", "2a"],
                    "footnote_required": False,
                    "is_refusal_note": True,
                    "text": "LU says no",
                    "third_party": "95c2d6b7-5cfd-47e8-b3c8-dc76e1ac9747",
                    "type": "refuse",
                },
                {
                    "denial_reasons": ["1", "2a"],
                    "footnote_required": False,
                    "good": "0bedd1c3-cf97-4aad-b711-d5c9a9f4586e",
                    "is_refusal_note": True,
                    "text": "LU says no",
                    "type": "refuse",
                },
                {
                    "denial_reasons": [],
                    "footnote": "",
                    "footnote_required": False,
                    "good": "6daad1c3-cf97-4aad-b711-d5c9a9f4586e",
                    "note": "",
                    "proviso": "",
                    "text": "",
                    "type": "no_licence_required",
                },
            ],
        ),
    ),
)
def test_LUConsolidateRefuseView_POST_success(
    refusal_data,
    expected_post_data,
    authorized_client,
    lu_consolidate_refuse_url,
    mixed_advice,
    data_standard_case,
    lu_gov_user,
    mock_post_refusal_final_advice,
    consolidate_view_url,
):
    data_standard_case["case"]["advice"] = mixed_advice
    data_standard_case["case"]["data"]["goods"][0]["is_good_controlled"] = {"key": "True", "value": "Yes"}

    response = authorized_client.post(lu_consolidate_refuse_url, data=refusal_data)
    assert response.status_code == 302
    assert response.url == consolidate_view_url
    assert len(mock_post_refusal_final_advice.request_history) == 1
    assert mock_post_refusal_final_advice.request_history[0].json() == expected_post_data


@pytest.fixture
def mock_post_refusal_final_advice_server_error(requests_mock, data_standard_case):
    return requests_mock.post(
        client._build_absolute_uri(f"/cases/{data_standard_case['case']['id']}/final-advice/"),
        json={},
        status_code=500,
    )


def test_LUConsolidateRefuseView_POST_server_error(
    authorized_client,
    lu_consolidate_refuse_url,
    mixed_advice,
    data_standard_case,
    lu_gov_user,
    mock_post_refusal_final_advice_server_error,
):
    data_standard_case["case"]["advice"] = mixed_advice
    response = authorized_client.post(
        lu_consolidate_refuse_url, data={"denial_reasons": ["1", "2a"], "refusal_note": "you can't do that"}
    )
    assert response.status_code == 200
    form = response.context["form"]
    assert form.errors == {"__all__": ["An error occurred when saving consolidated advice"]}
