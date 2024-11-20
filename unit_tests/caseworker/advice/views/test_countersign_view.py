import pytest

from unittest.mock import patch

from bs4 import BeautifulSoup
from django.urls import reverse

from caseworker.advice.services import LICENSING_UNIT_TEAM, FIRST_COUNTERSIGN, SECOND_COUNTERSIGN
from core import client
from unit_tests.caseworker.conftest import countersignatures_for_advice


@pytest.fixture(autouse=True)
def setup(mock_queue, mock_denial_reasons, mock_case):
    yield


@pytest.fixture
def url(request, data_queue, data_standard_case):
    return reverse(
        f"cases:countersign_view", kwargs={"queue_pk": data_queue["id"], "pk": data_standard_case["case"]["id"]}
    )


def test_countersign_view_security_approvals(authorized_client, requests_mock, data_standard_case, url):
    case_id = data_standard_case["case"]["id"]
    requests_mock.get(client._build_absolute_uri(f"/cases/{case_id}"), json=data_standard_case)
    requests_mock.get(
        client._build_absolute_uri(f"/gov_users/{case_id}"),
        json={"user": {"id": "58e62718-e889-4a01-b603-e676b794b394"}},
    )
    response = authorized_client.get(url)
    assert response.status_code == 200
    assert response.context["security_approvals_classified_display"] == "F680"


def test_countersign_view_trigger_list_products(
    authorized_client, requests_mock, data_standard_case_with_all_trigger_list_products_assessed, url
):
    case_id = data_standard_case_with_all_trigger_list_products_assessed["case"]["id"]
    requests_mock.get(
        client._build_absolute_uri(f"/cases/{case_id}"), json=data_standard_case_with_all_trigger_list_products_assessed
    )
    response = authorized_client.get(url)
    assert response.status_code == 200
    expected_context = [
        {"line_number": num, **good}
        for num, good in enumerate(
            data_standard_case_with_all_trigger_list_products_assessed["case"]["data"]["goods"], start=1
        )
    ]
    assert response.context["assessed_trigger_list_goods"] == expected_context


@patch("caseworker.advice.views.get_gov_user")
def test_single_lu_countersignature(
    mock_get_gov_user,
    authorized_client,
    requests_mock,
    data_standard_case,
    final_advice,
    url,
):
    case_id = data_standard_case["case"]["id"]
    team_id = final_advice["user"]["team"]["id"]
    data_standard_case["case"]["advice"] = [final_advice]
    data_standard_case["case"]["countersign_advice"] = countersignatures_for_advice(
        [final_advice],
        [
            {"order": FIRST_COUNTERSIGN, "outcome_accepted": True},
        ],
    )
    requests_mock.get(client._build_absolute_uri(f"/cases/{case_id}"), json=data_standard_case)
    mock_get_gov_user.return_value = (
        {"user": {"team": {"id": team_id, "alias": LICENSING_UNIT_TEAM}}},
        None,
    )
    response = authorized_client.get(url)

    soup = BeautifulSoup(response.content, "html.parser")
    countersignature_block = soup.find(class_="countersignatures")
    assert response.status_code == 200

    counter_sigs = countersignature_block.find_all("div", recursive=False)
    assert len(counter_sigs) == 1
    assert counter_sigs[0].find(class_="govuk-heading-m").text == "Countersigned by Testy McTest"
    assert counter_sigs[0].find(class_="govuk-body").text == "I concur"
    rejected_warning = soup.find(id="rejected-countersignature")
    assert not rejected_warning


@patch("caseworker.advice.views.get_gov_user")
def test_double_lu_countersignature(
    mock_get_gov_user,
    authorized_client,
    requests_mock,
    data_standard_case,
    final_advice,
    url,
):
    case_id = data_standard_case["case"]["id"]
    team_id = final_advice["user"]["team"]["id"]
    data_standard_case["case"]["advice"] = [final_advice]
    data_standard_case["case"]["countersign_advice"] = countersignatures_for_advice(
        [final_advice],
        [
            {"order": FIRST_COUNTERSIGN, "outcome_accepted": True},
            {"order": SECOND_COUNTERSIGN, "outcome_accepted": True},
        ],
    )
    requests_mock.get(client._build_absolute_uri(f"/cases/{case_id}"), json=data_standard_case)
    mock_get_gov_user.return_value = (
        {"user": {"team": {"id": team_id, "alias": LICENSING_UNIT_TEAM}}},
        None,
    )
    response = authorized_client.get(url)

    soup = BeautifulSoup(response.content, "html.parser")
    countersignature_block = soup.find(class_="countersignatures")
    assert response.status_code == 200

    counter_sigs = countersignature_block.find_all("div", recursive=False)
    assert len(counter_sigs) == 2
    assert counter_sigs[0].find(class_="govuk-heading-m").text == "Senior countersigned by Super Visor"
    assert counter_sigs[0].find(class_="govuk-body").text == "LGTM"
    assert counter_sigs[1].find(class_="govuk-heading-m").text == "Countersigned by Testy McTest"
    assert counter_sigs[1].find(class_="govuk-body").text == "I concur"
    rejected_warning = soup.find(id="rejected-countersignature")
    assert not rejected_warning


@pytest.mark.parametrize(
    "countersigning_data",
    (
        [
            {"order": FIRST_COUNTERSIGN, "valid": True, "outcome_accepted": False},
        ],
        [
            {"order": FIRST_COUNTERSIGN, "valid": False, "outcome_accepted": False},
        ],
    ),
)
@patch("caseworker.advice.views.get_gov_user")
def test_single_lu_rejected_countersignature(
    mock_get_gov_user,
    countersigning_data,
    authorized_client,
    requests_mock,
    data_standard_case,
    final_advice,
    url,
):
    case_id = data_standard_case["case"]["id"]
    team_id = final_advice["user"]["team"]["id"]
    data_standard_case["case"]["advice"] = [final_advice]
    data_standard_case["case"]["countersign_advice"] = countersignatures_for_advice(
        [final_advice],
        countersigning_data,
    )
    requests_mock.get(client._build_absolute_uri(f"/cases/{case_id}"), json=data_standard_case)
    mock_get_gov_user.return_value = (
        {"user": {"team": {"id": team_id, "alias": LICENSING_UNIT_TEAM}}},
        None,
    )
    response = authorized_client.get(url)
    assert response.status_code == 200

    soup = BeautifulSoup(response.content, "html.parser")

    countersignature_valid = any(item["valid"] for item in countersigning_data)

    if countersignature_valid:
        counter_sigs = soup.find_all(class_="countersigned-by")
        assert len(counter_sigs) == 0
        rejected_counter_sigs = soup.find_all(class_="rejected-countersignature")
        assert len(rejected_counter_sigs) == 1
        assert (
            rejected_counter_sigs[0].find("h2").text == "Countersigner Testy McTest disagrees with this recommendation"
        )
        assert rejected_counter_sigs[0].find("p").text == "I disagree"
        rejected_warning = soup.find(id="rejected-countersignature")
        assert rejected_warning
        assert "This case will be returned to the case officer's queue." in rejected_warning.text
        assert (
            "It will come back for countersigning once they have reviewed and moved it forward."
            in rejected_warning.text
        )
    else:
        counter_sigs = soup.find_all(class_="countersigned-by")
        assert len(counter_sigs) == 0
        rejected_warning = soup.find(id="rejected-countersignature")
        assert rejected_warning is None


@pytest.mark.parametrize(
    "countersigning_data",
    (
        [
            {"order": FIRST_COUNTERSIGN, "valid": True, "outcome_accepted": True},
            {"order": SECOND_COUNTERSIGN, "valid": True, "outcome_accepted": False},
        ],
        [
            {"order": FIRST_COUNTERSIGN, "valid": False, "outcome_accepted": True},
            {"order": SECOND_COUNTERSIGN, "valid": False, "outcome_accepted": False},
        ],
    ),
)
@patch("caseworker.advice.views.get_gov_user")
def test_lu_rejected_senior_countersignature(
    mock_get_gov_user,
    countersigning_data,
    authorized_client,
    requests_mock,
    data_standard_case,
    final_advice,
    url,
):
    case_id = data_standard_case["case"]["id"]
    team_id = final_advice["user"]["team"]["id"]
    data_standard_case["case"]["advice"] = [final_advice]
    data_standard_case["case"]["countersign_advice"] = countersignatures_for_advice([final_advice], countersigning_data)
    requests_mock.get(client._build_absolute_uri(f"/cases/{case_id}"), json=data_standard_case)
    mock_get_gov_user.return_value = (
        {"user": {"team": {"id": team_id, "alias": LICENSING_UNIT_TEAM}}},
        None,
    )
    response = authorized_client.get(url)
    assert response.status_code == 200

    soup = BeautifulSoup(response.content, "html.parser")

    countersignature_valid = any(item["valid"] for item in countersigning_data)
    if countersignature_valid:
        counter_sigs = soup.find_all(class_=["countersigned-by", "rejected-countersignature"])
        assert len(counter_sigs) == 2
        # We expect the senior countersignature at the top.
        assert counter_sigs[0].find("h2").text == "Senior countersigner Super Visor disagrees with this recommendation"
        assert counter_sigs[0].find("p").text == "Nope"
        assert counter_sigs[1].find("h2").text == "Countersigned by Testy McTest"
        assert counter_sigs[1].find("p").text == "I concur"
        rejected_warning = soup.find(id="rejected-countersignature")
        assert rejected_warning
        assert "This case will be returned to the case officer's queue." in rejected_warning.text
        assert (
            "It will come back for countersigning once they have reviewed and moved it forward."
            in rejected_warning.text
        )
    else:
        counter_sigs = soup.find_all(class_="countersigned-by")
        assert len(counter_sigs) == 0
        rejected_warning = soup.find(id="rejected-countersignature")
        assert rejected_warning is None
