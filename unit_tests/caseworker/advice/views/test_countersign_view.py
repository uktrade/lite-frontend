import pytest

from copy import deepcopy
from django.urls import reverse

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
