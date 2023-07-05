import pytest
from bs4 import BeautifulSoup
from django.urls import reverse
from pytest_django.asserts import assertTemplateUsed

from core import client


@pytest.fixture
def mock_put_application_status(requests_mock, data_standard_case, mock_gov_user):
    case_id = data_standard_case["case"]["id"]
    url = client._build_absolute_uri(f"/applications/{case_id}/status/")
    return requests_mock.put(url=url, json={})


def test_change_status_GET(
    authorized_client, data_queue, data_standard_case, data_assignment, mock_standard_case, mock_queue
):
    case = data_standard_case
    url = (
        # Who knows why this url name is what it is
        reverse("cases:manage", kwargs={"queue_pk": data_queue["id"], "pk": case["case"]["id"]})
    )
    response = authorized_client.get(url)
    assert response.status_code == 200
    assertTemplateUsed(response, "layouts/case.html")
    context = response.context
    assert context["case"].id == case["case"]["id"]

    html = BeautifulSoup(response.content, "html.parser")
    all_h1s = [elem.get_text().strip() for elem in html.find_all("h1")]
    assert "Change case status" in all_h1s


def test_change_status_POST(
    authorized_client,
    data_queue,
    data_standard_case,
    data_assignment,
    mock_standard_case,
    mock_queue,
    mock_put_application_status,
):
    case = data_standard_case
    url = reverse("cases:manage", kwargs={"queue_pk": data_queue["id"], "pk": case["case"]["id"]})
    response = authorized_client.post(url, status="submitted", follow=False)
    assert response.status_code == 302
    assert response.url == f"/queues/{data_queue['id']}/cases/{case['case']['id']}/details/"
