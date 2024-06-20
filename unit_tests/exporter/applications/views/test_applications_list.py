import pytest

from django.urls import reverse
from pytest_django.asserts import assertTemplateUsed


@pytest.fixture
def mock_get_applications(requests_mock):
    return requests_mock.get(
        f"/applications/?page=1&submitted=True&finalised=False&sort=submitted_at",
        json={
            "count": 2,
            "total_pages": 1,
            "results": [
                {
                    "id": "7d391e14-4923-4896-933d-76c2af9ae95d",
                    "name": "Test1",
                    "case_type": {"sub_type": {"key": "standard", "value": "Standard Licence"}},
                    "status": {
                        "id": "00000000-0000-0000-0000-000000000004",
                        "key": "initial_checks",
                        "value": "Initial checks",
                    },
                    "submitted_at": "2020-04-09T09:54:28.247458+01:00",
                    "updated_at": "2023-06-07T12:05:42.003433+01:00",
                    "reference_code": "GBSIEL/2000/0000001/P",
                    "export_type": {"key": "permanent", "value": "Permanent"},
                    "exporter_user_notification_count": 0,
                },
                {
                    "id": "819ff014-1cfe-434a-8c56-a5b403174a4f",
                    "name": "Test2",
                    "case_type": {"sub_type": {"key": "standard", "value": "Standard Licence"}},
                    "status": {"id": "00000000-0000-0000-0000-000000000007", "key": "finalised", "value": "Finalised"},
                    "submitted_at": "2021-04-05T12:30:23.553351+01:00",
                    "updated_at": "2024-04-05T12:39:29.540878+01:00",
                    "reference_code": "GBSIEL/2000/0000002/P",
                    "export_type": {"key": "permanent", "value": "Permanent"},
                    "exporter_user_notification_count": 0,
                },
            ],
        },
    )


def test_get_applications(authorized_client, mock_get_applications):
    url = reverse("applications:applications")
    response = authorized_client.get(url)
    assert response.status_code == 200
    assertTemplateUsed(response, "applications/applications.html")
