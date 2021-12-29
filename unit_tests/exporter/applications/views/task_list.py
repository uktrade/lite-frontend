import pytest
from django.urls import reverse


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
