from copy import deepcopy
import pytest
from django.urls import reverse

from core import client


@pytest.fixture(autouse=True)
def setup(
    mock_get_application,
    mock_exporter_user_me,
    mock_get_application_documents,
    mock_get_application_sites,
    mock_get_application_external_locations,
    mock_get_application_case_notes,
    mock_get_application_goods,
):
    yield


def test_application_task_list_200(data_draft_standard_application, authorized_client):
    url = reverse("applications:task_list", kwargs={"pk": data_draft_standard_application["id"]})
    response = authorized_client.get(url)
    assert "applications/task-list.html" in [template.name for template in response.templates]
    assert response.status_code == 200


def test_application_task_list_200_no_new_fields(data_draft_standard_application, authorized_client, requests_mock):
    application_url = client._build_absolute_uri(f"/applications/{data_draft_standard_application['id']}/")
    application = deepcopy(data_draft_standard_application)
    del application["goods_recipients"]
    del application["goods_starting_point"]
    requests_mock.get(url=application_url, json=application)

    url = reverse("applications:task_list", kwargs={"pk": data_draft_standard_application["id"]})
    response = authorized_client.get(url)
    assert "applications/task-list.html" in [template.name for template in response.templates]
    assert response.status_code == 200
