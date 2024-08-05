import pytest

from bs4 import BeautifulSoup
from faker import Faker
from urllib.parse import urlencode
from uuid import uuid4

from django.urls import reverse
from pytest_django.asserts import assertTemplateUsed

faker = Faker()


def base_application_data():
    return {
        "id": str(uuid4()),
        "name": faker.name(),
        "export_type": {"key": "permanent", "value": "Permanent"},
        "exporter_user_notification_count": 0,
        "case_type": {"sub_type": {"key": "standard", "value": "Standard Licence"}},
    }


def draft_applications():
    return [
        {
            "status": {"id": "00000000-0000-0000-0000-000000000000", "key": "draft", "value": "Draft"},
            "reference_code": "",
            **base_application_data(),
        }
        for _ in range(5)
    ]


def submitted_applications():
    return [
        {
            "status": {"id": "00000000-0000-0000-0000-000000000004", "key": "submitted", "value": "Submitted"},
            "reference_code": "GBSIEL/2024/0000004/P",
            **base_application_data(),
        },
        {
            "status": {
                "id": "00000000-0000-0000-0000-000000000003",
                "key": "initial_checks",
                "value": "Initial checks",
            },
            "reference_code": "GBSIEL/2024/0000003/P",
            **base_application_data(),
        },
        {
            "status": {"id": "00000000-0000-0000-0000-000000000002", "key": "under_review", "value": "Under review"},
            "reference_code": "GBSIEL/2024/0000002/P",
            **base_application_data(),
        },
        {
            "status": {"id": "00000000-0000-0000-0000-000000000001", "key": "ogd_advice", "value": "OGD Advice"},
            "reference_code": "GBSIEL/2024/0000001/P",
            **base_application_data(),
        },
    ]


def finalised_applications():
    return [
        {
            "status": {"id": "00000000-0000-0000-0000-000000000009", "key": "finalised", "value": "Finalised"},
            "reference_code": f"GBSIEL/2024/000000{index}/P",
            **base_application_data(),
        }
        for index in range(8)
    ]


def archived_applications():
    return [
        {
            "status": {
                "id": "00000000-0000-0000-0000-000000000009",
                "key": "superseded_by_exporter_edit",
                "value": "Superseded by Exporter edit",
            },
            "reference_code": f"GBSIEL/2024/000000{index}/P",
            **base_application_data(),
        }
        for index in range(4)
    ]


@pytest.fixture
def mock_get_draft_applications(requests_mock):
    drafts = draft_applications()

    return requests_mock.get(
        f"/applications/?selected_filter=draft_applications",
        json={
            "count": len(drafts),
            "total_pages": 1,
            "results": drafts,
        },
    )


@pytest.fixture
def mock_get_submitted_applications(requests_mock):
    submitted = submitted_applications()

    return requests_mock.get(
        f"/applications/?selected_filter=submitted_applications",
        json={
            "count": len(submitted),
            "total_pages": 1,
            "results": submitted,
        },
    )


@pytest.fixture
def mock_get_finalised_applications(requests_mock):
    finalised = finalised_applications()

    return requests_mock.get(
        f"/applications/?selected_filter=finalised_applications",
        json={
            "count": len(finalised),
            "total_pages": 1,
            "results": finalised,
        },
    )


@pytest.fixture
def mock_get_archived_applications(requests_mock):
    archived = archived_applications()

    return requests_mock.get(
        f"/applications/?selected_filter=archived_applications",
        json={
            "count": len(archived),
            "total_pages": 1,
            "results": archived,
        },
    )


def get_applications(response):
    soup = BeautifulSoup(response.content, "html.parser")
    return soup.find("tbody", {"class": "govuk-table__body"}).find_all("tr", recursive=False)


def test_get_applications(authorized_client, mock_get_submitted_applications):
    url = reverse("applications:applications")
    response = authorized_client.get(url)
    assert response.status_code == 200

    assertTemplateUsed(response, "applications/applications.html")
    assert len(get_applications(response)) == len(submitted_applications())


def test_get_draft_applications(authorized_client, mock_get_draft_applications):
    query_params = {"selected_filter": "draft_applications"}
    url = reverse("applications:applications") + f"?{urlencode(query_params, doseq=True)}"

    response = authorized_client.get(url)
    assert response.status_code == 200

    assertTemplateUsed(response, "applications/applications.html")
    assert len(get_applications(response)) == len(draft_applications())


def test_get_submitted_applications(authorized_client, mock_get_submitted_applications):
    query_params = {"selected_filter": "submitted_applications"}
    url = reverse("applications:applications") + f"?{urlencode(query_params, doseq=True)}"

    response = authorized_client.get(url)
    assert response.status_code == 200

    assertTemplateUsed(response, "applications/applications.html")
    assert len(get_applications(response)) == len(submitted_applications())


def test_get_finalised_applications(authorized_client, mock_get_finalised_applications):
    query_params = {"selected_filter": "finalised_applications"}
    url = reverse("applications:applications") + f"?{urlencode(query_params, doseq=True)}"

    response = authorized_client.get(url)
    assert response.status_code == 200

    assertTemplateUsed(response, "applications/applications.html")
    assert len(get_applications(response)) == len(finalised_applications())


def test_get_archived_applications(authorized_client, mock_get_archived_applications):
    query_params = {"selected_filter": "archived_applications"}
    url = reverse("applications:applications") + f"?{urlencode(query_params, doseq=True)}"

    response = authorized_client.get(url)
    assert response.status_code == 200

    assertTemplateUsed(response, "applications/applications.html")
    assert len(get_applications(response)) == len(archived_applications())
