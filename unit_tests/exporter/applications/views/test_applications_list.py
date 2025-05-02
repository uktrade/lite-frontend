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


def standard_application_case_type_dict():
    return {
        "reference": {"key": "siel", "value": "Standard Individual Export Licence"},
        "sub_type": {"key": "standard", "value": "Standard Licence"},
    }


def f680_application_case_type_dict():
    return {
        "reference": {"key": "f680", "value": "MOD F680 Clearance"},
        "sub_type": {"key": "f680_clearance", "value": "MOD F680 Clearance"},
    }


def export_licence_case_type_dict():
    return {
        "reference": {"key": "export_licence", "value": "Export Licence"},
        "sub_type": None,
    }


def base_application_data(index, case_type):
    return {
        "id": str(uuid4()),
        "name": f"Application{index}",
        "export_type": {"key": "permanent", "value": "Permanent"},
        "exporter_user_notification_count": 0,
        "case_type": case_type,
    }


def draft_applications(case_type):
    return [
        {
            "status": {"id": "00000000-0000-0000-0000-000000000000", "key": "draft", "value": "Draft"},
            "reference_code": "",
            "submitted_by": "",
            "submitted_at": None,
            "updated_at": datetime.now().isoformat(),
            **base_application_data(index, case_type),
        }
        for index in range(5)
    ]


def submitted_applications(case_type):
    status_list = [
        {"id": "00000000-0000-0000-0000-000000000004", "key": "submitted", "value": "Submitted"},
        {"id": "00000000-0000-0000-0000-000000000003", "key": "initial_checks", "value": "Initial checks"},
        {"id": "00000000-0000-0000-0000-000000000002", "key": "under_review", "value": "Under review"},
        {"id": "00000000-0000-0000-0000-000000000001", "key": "ogd_advice", "value": "OGD Advice"},
    ]
    return [
        {
            "status": status_list[index],
            "reference_code": "GBSIEL/2024/000000{index}/P",
            "submitted_by": "Exporter user",
            "submitted_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat(),
            **base_application_data(index, case_type),
        }
        for index in range(len(status_list))
    ]


def finalised_applications(case_type):
    return [
        {
            "status": {"id": "00000000-0000-0000-0000-000000000009", "key": "finalised", "value": "Finalised"},
            "reference_code": f"GBSIEL/2024/000000{index}/P",
            "submitted_by": "Exporter user",
            "submitted_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat(),
            **base_application_data(index, case_type),
        }
        for index in range(8)
    ]


def archived_applications(case_type):
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
            **base_application_data(index, case_type),
        }
        for index in range(4)
    ]


@pytest.fixture
def mock_get_applications_factory(requests_mock):
    def _mock_get_applications_factory(status_type_dict, case_type_dict_func, selected_filter=None):
        drafts = status_type_dict(case_type_dict_func())

        url = "/applications/"
        if selected_filter:
            url = f"{url}?selected_filter={selected_filter}"

        return requests_mock.get(
            url,
            json={
                "count": len(drafts),
                "total_pages": 1,
                "results": drafts,
            },
        )

    return _mock_get_applications_factory


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
    sub_type = application["case_type"]["sub_type"]
    if sub_type:
        case_type = sub_type["value"]
    else:
        case_type = ""

    return {
        "name": application["name"],
        "exporter_user_notification_count": "",
        "reference_code": application["reference_code"],
        "submitted_by": application["submitted_by"],
        "submitted_at": (
            str_date(application["submitted_at"]) if application["submitted_at"] else str(application["submitted_at"])
        ),
        "updated_at": str_date(application["updated_at"]),
        "case_type": case_type,
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
            assert application[key] == col.text.strip()


@pytest.mark.parametrize(
    "case_type_dict",
    (
        standard_application_case_type_dict,
        f680_application_case_type_dict,
        export_licence_case_type_dict,
    ),
)
def test_get_applications(authorized_client, mock_get_applications_factory, case_type_dict):
    mock_get_applications_factory(submitted_applications, case_type_dict)

    url = reverse("applications:applications")
    response = authorized_client.get(url)
    assert response.status_code == 200

    assertTemplateUsed(response, "applications/applications.html")
    assert len(get_applications(response)) == len(submitted_applications(standard_application_case_type_dict()))


@pytest.mark.parametrize(
    "case_type_dict",
    (
        standard_application_case_type_dict,
        f680_application_case_type_dict,
        export_licence_case_type_dict,
    ),
)
def test_get_draft_applications(authorized_client, mock_get_applications_factory, case_type_dict):
    mock_get_applications_factory(draft_applications, case_type_dict, "draft_applications")

    query_params = {"selected_filter": "draft_applications"}
    url = reverse("applications:applications") + f"?{urlencode(query_params, doseq=True)}"

    response = authorized_client.get(url)
    assert response.status_code == 200

    assertTemplateUsed(response, "applications/applications.html")
    verify_application_data(response, draft_headers, draft_applications(case_type_dict()))


@pytest.mark.parametrize(
    "case_type_dict",
    (
        standard_application_case_type_dict,
        f680_application_case_type_dict,
        export_licence_case_type_dict,
    ),
)
def test_get_submitted_applications(authorized_client, mock_get_applications_factory, case_type_dict):
    mock_get_applications_factory(submitted_applications, case_type_dict, "submitted_applications")

    query_params = {"selected_filter": "submitted_applications"}
    url = reverse("applications:applications") + f"?{urlencode(query_params, doseq=True)}"

    response = authorized_client.get(url)
    assert response.status_code == 200

    assertTemplateUsed(response, "applications/applications.html")
    verify_application_data(response, headers, submitted_applications(case_type_dict()))


@pytest.mark.parametrize(
    "case_type_dict",
    (
        standard_application_case_type_dict,
        f680_application_case_type_dict,
        export_licence_case_type_dict,
    ),
)
def test_get_finalised_applications(authorized_client, mock_get_applications_factory, case_type_dict):
    mock_get_applications_factory(finalised_applications, case_type_dict, "finalised_applications")

    query_params = {"selected_filter": "finalised_applications"}
    url = reverse("applications:applications") + f"?{urlencode(query_params, doseq=True)}"

    response = authorized_client.get(url)
    assert response.status_code == 200

    assertTemplateUsed(response, "applications/applications.html")
    verify_application_data(response, headers, finalised_applications(case_type_dict()))


@pytest.mark.parametrize(
    "case_type_dict",
    (
        standard_application_case_type_dict,
        f680_application_case_type_dict,
        export_licence_case_type_dict,
    ),
)
def test_get_archived_applications(authorized_client, mock_get_applications_factory, case_type_dict):
    mock_get_applications_factory(archived_applications, case_type_dict, "archived_applications")

    query_params = {"selected_filter": "archived_applications"}
    url = reverse("applications:applications") + f"?{urlencode(query_params, doseq=True)}"

    response = authorized_client.get(url)
    assert response.status_code == 200

    assertTemplateUsed(response, "applications/applications.html")
    verify_application_data(response, headers, archived_applications(case_type_dict()))
