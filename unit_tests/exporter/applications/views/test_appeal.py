import pytest

from django.urls import reverse


@pytest.fixture
def appeal_url(data_standard_case):
    case_pk = data_standard_case["case"]["id"]

    return reverse("applications:appeal", kwargs={"case_pk": case_pk})


def test_appeal_view(authorized_client, appeal_url):
    response = authorized_client.get(appeal_url)
    assert response.status_code == 200
