import pytest

from bs4 import BeautifulSoup

from django.contrib.messages import constants, get_messages
from django.urls import reverse

from pytest_django.asserts import assertTemplateUsed

from core import client
from core.exceptions import ServiceError


@pytest.fixture(autouse=True)
def setup(data_standard_case, mock_gov_user):
    data_standard_case["case"]["case_officer"] = mock_gov_user["user"]


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
def post_sub_status_api_url(case_id):
    return client._build_absolute_uri(f"/applications/{case_id}/sub-status/")


@pytest.fixture
def mock_put_case_sub_status(post_sub_status_api_url, requests_mock):
    return requests_mock.put(
        url=post_sub_status_api_url,
        json={},
    )


@pytest.fixture
def mock_put_case_sub_status_failure(post_sub_status_api_url, requests_mock):
    return requests_mock.put(
        url=post_sub_status_api_url,
        json={},
        status_code=500,
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
    change_sub_status_url,
):
    response = authorized_client.get(change_sub_status_url)
    assert response.status_code == 200
    assertTemplateUsed("case/form.html")
    soup = BeautifulSoup(response.content, "html.parser")
    select = soup.find(id="id_sub_status")
    options = [(option["value"], option.text) for option in select.find_all("option")]
    assert options == [
        ("", "None"),
        ("status-1", "Status 1"),
        ("status-2", "Status 2"),
    ]


def test_get_change_sub_status_initial_value(
    authorized_client,
    mock_queue,
    mock_case,
    change_sub_status_url,
    data_standard_case,
):
    data_standard_case["case"]["data"]["sub_status"] = {
        "id": "status-2",
        "name": "Status 2",
    }

    response = authorized_client.get(change_sub_status_url)
    soup = BeautifulSoup(response.content, "html.parser")
    select = soup.find(id="id_sub_status")
    option_elements = select.find_all("option")
    assert "selected" not in option_elements[0].attrs
    assert "selected" not in option_elements[1].attrs
    assert "selected" in option_elements[2].attrs


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


def test_change_sub_status_no_available_sub_statuses(
    authorized_client,
    mock_queue,
    mock_case,
    change_sub_status_url,
    data_standard_case,
    get_sub_status_api_url,
    requests_mock,
):
    requests_mock.get(
        url=get_sub_status_api_url,
        json=[],
    )
    response = authorized_client.get(change_sub_status_url)
    assert response.status_code == 404


def test_post_change_sub_status(
    authorized_client,
    change_sub_status_url,
    case_url,
    mock_case,
    mock_queue,
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
    assert [(m.level, m.message) for m in get_messages(response.wsgi_request)] == [
        (constants.SUCCESS, "Case sub-status successfully changed")
    ]


def test_post_change_sub_status_setting_none(
    authorized_client,
    change_sub_status_url,
    case_url,
    mock_case,
    mock_queue,
    mock_put_case_sub_status,
):
    response = authorized_client.post(
        change_sub_status_url,
        data={
            "sub_status": "",
        },
    )
    assert response.status_code == 302
    assert response.url == case_url
    assert mock_put_case_sub_status.called
    assert mock_put_case_sub_status.last_request.json() == {
        "sub_status": "",
    }


def test_post_change_sub_status_setting_failure(
    authorized_client,
    change_sub_status_url,
    case_url,
    mock_case,
    mock_queue,
    mock_put_case_sub_status_failure,
):
    with pytest.raises(ServiceError) as ex:
        authorized_client.post(
            change_sub_status_url,
            data={
                "sub_status": "",
            },
        )

    assert ex.value.status_code == 500
    assert ex.value.user_message == "Unexpected error changing case sub-status"
