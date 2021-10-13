import pytest

from django.urls import reverse

from unit_tests.caseworker.conftest import standard_case_pk


@pytest.fixture(autouse=True)
def setup(mock_queue, mock_case):
    yield


@pytest.fixture
def url(data_queue, data_standard_case):
    return reverse("cases:select_advice", kwargs={"queue_pk": data_queue["id"], "pk": data_standard_case["case"]["id"]})


def test_select_advice_get(authorized_client, url):
    response = authorized_client.get(url)
    assert response.status_code == 200


@pytest.mark.parametrize("recommendation, redirect", [("approve_all", "approve"), ("refuse_all", "refuse")])
def test_select_advice_post(authorized_client, url, recommendation, redirect):
    response = authorized_client.post(url, data={"recommendation": recommendation})
    assert response.status_code == 302
    assert redirect in response.url
