import copy
from unittest.mock import patch

import pytest

from copy import deepcopy

from bs4 import BeautifulSoup
from django.urls import reverse

from caseworker.advice.services import LICENSING_UNIT_TEAM
from core import client
from caseworker.advice import services


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


@patch("caseworker.advice.views.get_gov_user")
def test_single_lu_countersignature(
    mock_get_gov_user, authorized_client, requests_mock, data_standard_case, final_advice, first_countersignature, url
):
    case_id = data_standard_case["case"]["id"]
    team_id = final_advice["user"]["team"]["id"]
    data_standard_case["case"]["advice"] = [final_advice]
    data_standard_case["case"]["countersign_advice"] = first_countersignature
    requests_mock.get(client._build_absolute_uri(f"/cases/{case_id}"), json=data_standard_case)
    mock_get_gov_user.return_value = (
        {"user": {"team": {"id": team_id, "alias": LICENSING_UNIT_TEAM}}},
        None,
    )
    response = authorized_client.get(url)

    soup = BeautifulSoup(response.content, "html.parser")
    countersignature_block = soup.find(id="countersignatures")
    assert response.status_code == 200

    counter_sigs = countersignature_block.find_all("div", recursive=False)
    assert len(counter_sigs) == 1
    assert counter_sigs[0].find(class_="govuk-heading-m").text == "Countersigned by Testy McTest"
    assert counter_sigs[0].find(class_="govuk-body").text == "I concur"


@patch("caseworker.advice.views.get_gov_user")
def test_double_lu_countersignature(
    mock_get_gov_user,
    authorized_client,
    requests_mock,
    data_standard_case,
    final_advice,
    first_countersignature,
    countersignature_two,
    url,
):
    case_id = data_standard_case["case"]["id"]
    team_id = final_advice["user"]["team"]["id"]
    data_standard_case["case"]["advice"] = [final_advice]
    data_standard_case["case"]["countersign_advice"] = first_countersignature + countersignature_two
    requests_mock.get(client._build_absolute_uri(f"/cases/{case_id}"), json=data_standard_case)
    mock_get_gov_user.return_value = (
        {"user": {"team": {"id": team_id, "alias": LICENSING_UNIT_TEAM}}},
        None,
    )
    response = authorized_client.get(url)

    soup = BeautifulSoup(response.content, "html.parser")
    countersignature_block = soup.find(id="countersignatures")
    assert response.status_code == 200

    counter_sigs = countersignature_block.find_all("div", recursive=False)
    assert len(counter_sigs) == 2
    assert counter_sigs[0].find(class_="govuk-heading-m").text == "Countersigned by Super Visor"
    assert counter_sigs[0].find(class_="govuk-body").text == "LGTM"
    assert counter_sigs[1].find(class_="govuk-heading-m").text == "Countersigned by Testy McTest"
    assert counter_sigs[1].find(class_="govuk-body").text == "I concur"
