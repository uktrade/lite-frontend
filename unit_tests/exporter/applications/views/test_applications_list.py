import pytest

from datetime import datetime

from bs4 import BeautifulSoup
from faker import Faker
from urllib.parse import urlencode
from uuid import uuid4

from django.urls import reverse
from pytest_django.asserts import assertTemplateUsed

from core.builtins.custom_tags import str_date

faker = Faker()


draft_headers = [
    {"key": "name", "value": "Your reference"},
    {"key": "exporter_user_notification_count", "value": ""},
    {"key": "reference_code", "value": "ECJU reference"},
    {"key": "case_type", "value": "Type"},
    {"key": "submitted_at", "value": "Date submitted"},
    {"key": "updated_at", "value": "Last updated"},
    {"key": "status", "value": "Status"},
]
headers = [
    {"key": "name", "value": "Your reference"},
    {"key": "exporter_user_notification_count", "value": ""},
    {"key": "submitted_by", "value": "Submitted by"},
    {"key": "reference_code", "value": "ECJU reference"},
    {"key": "case_type", "value": "Type"},
    {"key": "submitted_at", "value": "Date submitted"},
    {"key": "updated_at", "value": "Last updated"},
    {"key": "status", "value": "Status"},
]


def base_application_data(index):
    return {
        "id": str(uuid4()),
        "name": f"Application{index}",
        "export_type": {"key": "permanent", "value": "Permanent"},
        "exporter_user_notification_count": 0,
        "case_type": {"sub_type": {"key": "standard", "value": "Standard Licence"}},
    }

def base_f680_application_data():
    return {
        "id": str(uuid4()),
        "name": f"F680 Application",
        "export_type": {"key": "permanent", "value": "Permanent"},
        "exporter_user_notification_count": 0,
        "case_type": {"sub_type": {"key": "f680_clearance", "value": "MOD F680 Clearance"}},
    }


def draft_applications():
    draft_applications = [
        {
            "status": {"id": "00000000-0000-0000-0000-000000000000", "key": "draft", "value": "Draft"},
            "reference_code": "",
            "submitted_by": "",
            "submitted_at": None,
            "updated_at": datetime.now().isoformat(),
            **base_application_data(index),
        }
        for index in range(5)
    ]
    draft_applications.append(
        {
            "status": {"id": "00000000-0000-0000-0000-000000000000", "key": "draft", "value": "Draft"},
            "reference_code": "",
            "submitted_by": "",
            "submitted_at": None,
            "updated_at": datetime.now().isoformat(),
            **base_f680_application_data(),
        }
    )
    return draft_applications

def submitted_applications():
    return [
        {
            "status": {"id": "00000000-0000-0000-0000-000000000004", "key": "submitted", "value": "Submitted"},
            "reference_code": "GBSIEL/2024/0000004/P",
            "submitted_by": "Exporter user",
            "submitted_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat(),
            **base_application_data(0),
        },
        {
            "status": {
                "id": "00000000-0000-0000-0000-000000000003",
                "key": "initial_checks",
                "value": "Initial checks",
            },
            "reference_code": "GBSIEL/2024/0000003/P",
            "submitted_by": "Exporter user",
            "submitted_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat(),
            **base_application_data(1),
        },
        {
            "status": {"id": "00000000-0000-0000-0000-000000000002", "key": "under_review", "value": "Under review"},
            "reference_code": "GBSIEL/2024/0000002/P",
            "submitted_by": "Exporter user",
            "submitted_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat(),
            **base_application_data(2),
        },
        {
            "status": {"id": "00000000-0000-0000-0000-000000000001", "key": "ogd_advice", "value": "OGD Advice"},
            "reference_code": "GBSIEL/2024/0000001/P",
            "submitted_by": "Exporter user",
            "submitted_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat(),
            **base_application_data(3),
        },
    ]


def finalised_applications():
    return [
        {
            "status": {"id": "00000000-0000-0000-0000-000000000009", "key": "finalised", "value": "Finalised"},
            "reference_code": f"GBSIEL/2024/000000{index}/P",
            "submitted_by": "Exporter user",
            "submitted_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat(),
            **base_application_data(index),
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
            "submitted_by": "Exporter user",
            "submitted_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat(),
            **base_application_data(index),
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


def get_formatted_data(application):
    """Returns formatted data of required fields for each application"""
    return {
        "name": application["name"],
        "exporter_user_notification_count": "",
        "reference_code": application["reference_code"],
        "submitted_by": application["submitted_by"],
        "submitted_at": (
            str_date(application["submitted_at"]) if application["submitted_at"] else str(application["submitted_at"])
        ),
        "updated_at": str_date(application["updated_at"]),
        "case_type": application["case_type"]["sub_type"]["value"],
        "status": application["status"]["value"],
    }


def verify_application_data(response, headers, expected):
    soup = BeautifulSoup(response.content, "html.parser")
    rows = soup.find("tbody", {"class": "govuk-table__body"}).find_all("tr", recursive=False)

    # check we have expected number of applications for this status
    assert len(rows) == len(expected)

    # Check for each application the data is as expected
    for row_index, item in enumerate(expected):
        soup = BeautifulSoup(rows[row_index].encode("utf-8"), "html.parser")
        columns = soup.find("tr", {"class": "govuk-table__row"}).find_all("td", recursive=False)
        assert len(columns) == len(headers)

        application = get_formatted_data(item)
        for col_index, col in enumerate(columns):
            key = headers[col_index]["key"]
            assert application[key] in col.text


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
    verify_application_data(response, draft_headers, draft_applications())


def test_get_submitted_applications(authorized_client, mock_get_submitted_applications):
    query_params = {"selected_filter": "submitted_applications"}
    url = reverse("applications:applications") + f"?{urlencode(query_params, doseq=True)}"

    response = authorized_client.get(url)
    assert response.status_code == 200

    assertTemplateUsed(response, "applications/applications.html")
    verify_application_data(response, headers, submitted_applications())


def test_get_finalised_applications(authorized_client, mock_get_finalised_applications):
    query_params = {"selected_filter": "finalised_applications"}
    url = reverse("applications:applications") + f"?{urlencode(query_params, doseq=True)}"

    response = authorized_client.get(url)
    assert response.status_code == 200

    assertTemplateUsed(response, "applications/applications.html")
    verify_application_data(response, headers, finalised_applications())


def test_get_archived_applications(authorized_client, mock_get_archived_applications):
    query_params = {"selected_filter": "archived_applications"}
    url = reverse("applications:applications") + f"?{urlencode(query_params, doseq=True)}"

    response = authorized_client.get(url)
    assert response.status_code == 200

    assertTemplateUsed(response, "applications/applications.html")
    verify_application_data(response, headers, archived_applications())
