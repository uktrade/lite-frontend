import pytest

from django.urls import reverse


@pytest.fixture(autouse=True)
def setup(mock_cases_search, authorized_client, queue_pk, mock_queue, mock_countries):
    yield


@pytest.mark.parametrize(
    "url",
    [
        reverse("core:index"),
        reverse("queues:cases"),
        reverse("queues:cases", kwargs={"queue_pk": "00000000-0000-0000-0000-000000000001"}),
    ],
)
def test_cases_view(url, authorized_client):
    response = authorized_client.get(url)
    assert response.status_code == 200
