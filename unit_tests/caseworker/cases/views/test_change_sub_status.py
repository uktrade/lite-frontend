import pytest

from bs4 import BeautifulSoup

from django.urls import reverse

from pytest_django.asserts import assertTemplateUsed

from core import client


@pytest.fixture
def queue_id(data_queue):
    return data_queue["id"]


@pytest.fixture
def case_id(data_standard_case):
    return data_standard_case["case"]["id"]


@pytest.fixture
def get_sub_status_api_url(case_id):
    return client._build_absolute_uri(f"/applications/{case_id}/sub-statuses/")


@pytest.fixture
def mock_get_case_sub_statuses(get_sub_status_api_url, requests_mock):
    requests_mock.get(
        url=get_sub_status_api_url,
        json=[
            {"id": "status-1", "name": "Status 1"},
            {"id": "status-2", "name": "Status 2"},
        ],
    )


@pytest.fixture
def post_sub_status_api_url(case_id):
    return client._build_absolute_uri(f"/applications/{case_id}/sub-status/")


@pytest.fixture
def mock_put_case_sub_status(post_sub_status_api_url, requests_mock):
    return requests_mock.put(
        url=post_sub_status_api_url,
        json={},
    )


@pytest.fixture
def change_sub_status_url(queue_id, case_id):
    return reverse(
        "cases:change_sub_status",
        kwargs={
            "queue_pk": queue_id,
            "pk": case_id,
        },
    )


@pytest.fixture
def case_url(queue_id, case_id):
    return reverse(
        "cases:case",
        kwargs={
            "queue_pk": queue_id,
            "pk": case_id,
            "tab": "details",
        },
    )


def test_get_change_sub_status(
    authorized_client,
    mock_queue,
    mock_case,
    mock_get_case_sub_statuses,
    change_sub_status_url,
):
    response = authorized_client.get(change_sub_status_url)
    assert response.status_code == 200
    assertTemplateUsed("case/form.html")
    soup = BeautifulSoup(response.content, "html.parser")
    select = soup.find(id="id_sub_status")
    options = [(option["value"], option.text) for option in select.find_all("option")]
    assert options == [
        ("status-1", "Status 1"),
        ("status-2", "Status 2"),
    ]


def test_change_sub_status_invalid_case_pk(
    authorized_client,
    queue_id,
    case_id,
    mock_queue,
    requests_mock,
):
    url = client._build_absolute_uri(f"/cases/fbaa077a-01d1-47e6-b09b-697f7acd78a5/")
    requests_mock.get(url=url, json={}, status_code=404)

    url = reverse(
        "cases:change_sub_status",
        kwargs={
            "queue_pk": queue_id,
            "pk": "fbaa077a-01d1-47e6-b09b-697f7acd78a5",
        },
    )
    response = authorized_client.get(url)
    assert response.status_code == 404


def test_post_change_sub_status(
    authorized_client,
    change_sub_status_url,
    case_url,
    mock_case,
    mock_queue,
    mock_get_case_sub_statuses,
    mock_put_case_sub_status,
):
    response = authorized_client.post(
        change_sub_status_url,
        data={
            "sub_status": "status-1",
        },
    )
    assert response.status_code == 302
    assert response.url == case_url
    assert mock_put_case_sub_status.called
    assert mock_put_case_sub_status.last_request.json() == {
        "sub_status": "status-1",
    }
