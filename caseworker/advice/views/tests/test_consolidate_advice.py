import pytest

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
    mock_finalise_advice_documents,
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
        "cases:consolidate",
        kwargs={"queue_pk": data_queue["id"], "pk": data_standard_case["case"]["id"], "advice_type": "approve"},
    )


@pytest.fixture
def consolidate_refuse_url(data_queue, data_standard_case):
    return reverse(
        "cases:consolidate",
        kwargs={"queue_pk": data_queue["id"], "pk": data_standard_case["case"]["id"], "advice_type": "refuse"},
    )


@pytest.fixture
def advice_data(current_user, admin_team):
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
        "team": admin_team,
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
    assert response.context["title"] == "Review and combine case recommendation - GBSIEL/2020/0002687/T - jim"


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
    assert response.context["title"] == "Review and combine case recommendation - GBSIEL/2020/0002687/T - jim"


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
    lu_gov_user,
    consolidate_refuse_url,
):
    data_standard_case["case"]["advice"] = mixed_advice
    response = authorized_client.post(consolidate_select_decision_url, data={"recommendation": "refuse"}, follow=False)
    assert response.status_code == 302
    assert response.url == consolidate_refuse_url
