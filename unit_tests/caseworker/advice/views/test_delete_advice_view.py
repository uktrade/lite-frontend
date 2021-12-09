import pytest

from django.urls import reverse

from core import client


@pytest.fixture(autouse=True)
def setup(mock_queue, mock_case):
    yield


@pytest.fixture
def url(data_queue, data_standard_case):
    return reverse("cases:delete_advice", kwargs={"queue_pk": data_queue["id"], "pk": data_standard_case["case"]["id"]})


def test_delete_advice_get(authorized_client, url):
    response = authorized_client.get(url)

    assert response.status_code == 200
    assert "Are you sure you want to delete your recommendation on this case?" in str(response.content)


def test_delete_advice_post(authorized_client, url, data_queue, data_standard_case, requests_mock):
    requests_mock.delete(client._build_absolute_uri(f"/cases/{data_standard_case['case']['id']}/user-advice/"), json={})

    response = authorized_client.post(url)

    assert response.status_code == 302
    assert response.url == reverse(
        "cases:select_advice", kwargs={"queue_pk": data_queue["id"], "pk": data_standard_case["case"]["id"]}
    )
