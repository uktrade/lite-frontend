from unittest import mock

import pytest

from django.urls import reverse

from core import client
from unit_tests.caseworker.conftest import mock_gov_user, standard_case_pk


@pytest.fixture(autouse=True)
def setup(mock_queue, mock_case):
    yield


@pytest.fixture
def url(data_queue, data_standard_case):
    return reverse("cases:approve_all", kwargs={"queue_pk": data_queue["id"], "pk": data_standard_case["case"]["id"]})


def test_give_approval_advice_get(authorized_client, url):
    response = authorized_client.get(url)
    assert response.status_code == 200


def test_select_advice_post(authorized_client, requests_mock, data_standard_case, url):
    requests_mock.post(f"/cases/{data_standard_case['case']['id']}/user-advice/", json={})

    data = {"approval_reasons": "meets the requirements", "instructions_to_exporter": "no specific instructions"}
    response = authorized_client.post(url, data=data)
    assert response.status_code == 302


@mock.patch("caseworker.advice.views.get_gov_user")
def test_fco_give_approval_advice_get(mock_get_gov_user, authorized_client, url):
    mock_get_gov_user.return_value = ({"user": {"team": {"name": "FCO"}}}, None)
    response = authorized_client.get(url)
    assert response.status_code == 200
    assert "countries" in response.context_data["form"].fields
    assert response.context_data["form"].fields["countries"].choices == [
        ("GB", "United Kingdom"),
        ("AE-AZ", "Abu Dhabi"),
    ]


@pytest.mark.parametrize(
    "countries, approval_reasons, expected_status_code",
    [
        # Valid form
        (["GB"], "test", 302),
        # Valid form with 2 countries
        (["GB", "AE-AZ"], "test", 302),
        # Invalid form - missing countries
        ([], "test", 200),
        # Invalid form - missing approval_reasons
        (["GB"], "", 200),
        # Invalid form - missing countries & approval_reasons
        ([], "", 200),
    ],
)
@mock.patch("caseworker.advice.views.get_gov_user")
def test_fco_give_approval_advice_post(
    mock_get_gov_user,
    authorized_client,
    requests_mock,
    data_standard_case,
    url,
    countries,
    approval_reasons,
    expected_status_code,
):
    mock_get_gov_user.return_value = ({"user": {"team": {"name": "FCO"}}}, None)
    requests_mock.post(f"/cases/{data_standard_case['case']['id']}/user-advice/", json={})
    data = {"approval_reasons": approval_reasons, "countries": countries}
    response = authorized_client.post(url, data=data)
    assert response.status_code == expected_status_code
