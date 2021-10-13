import pytest

from django.urls import reverse

from core import client
from unit_tests.caseworker.conftest import standard_case_pk


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
