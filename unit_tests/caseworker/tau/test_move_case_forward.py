from bs4 import BeautifulSoup
from django.urls import reverse
import pytest

from core import client


@pytest.fixture(autouse=True)
def setup(mock_queue, mock_case):
    yield


@pytest.fixture
def mock_move_case_forward_api(requests_mock, data_standard_case, data_queue):
    case_id = data_standard_case["case"]["id"]
    url = client._build_absolute_uri(f"/cases/{case_id}/assigned-queues/")
    requests_mock.put(url, json={"queues": [data_queue["id"]]})
    return requests_mock


@pytest.fixture
def url(data_queue, data_standard_case):
    return reverse(
        "cases:tau:move_case_forward",
        kwargs={"queue_pk": data_queue["id"], "pk": data_standard_case["case"]["id"]},
    )


def test_move_case_forward_auth(authorized_client, url, mock_move_case_forward_api):
    """POST /tau should return 200 with an authorised client"""
    response = authorized_client.post(url, dat={})
    assert response.status_code == 302
    assert mock_move_case_forward_api.last_request.json() == {"queues": ["00000000-0000-0000-0000-000000000001"]}


def test_move_case_forward_noauth(client, url, mock_move_case_forward_api):
    """POST /tau should return 302 with an unauthorised client"""
    response = client.post(url)
    assert response.status_code == 302
