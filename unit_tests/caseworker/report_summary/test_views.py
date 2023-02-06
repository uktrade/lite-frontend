import pytest
import re

from django.urls import reverse

from core import client

REPORT_SUMMARY_PREFIXES = "report_summary_prefixes"
REPORT_SUMMARY_SUBJECTS = "report_summary_subjects"

prefix_data = [
    {"id": "b0849a92-4611-4e5b-b076-03562b138fb5", "name": "components for"},  # /PS-IGNORE
    {"id": "1c2d9032-e565-4158-a054-0112e8fabe1c", "name": "countermeasure equipment for"},  # /PS-IGNORE
    {"id": "76c33f3f-1da8-4fde-b259-ada269b43d34", "name": "counter-countermeasure equipment for"},  # /PS-IGNORE
    {"id": "a4bb3d4d-1f6b-46a3-83fa-97a952fdd2c4", "name": "launching vehicles for"},  # /PS-IGNORE
]

subject_data = [
    {"id": "0f6fbc0f-ce20-4adb-9066-9a6547e5c372", "name": "NBC protective/defensive equipment"},  # /PS-IGNORE
    {"id": "97ebace4-0a4c-4ce3-ad46-cce85ea473e8", "name": "TV cameras and control equipment"},  # /PS-IGNORE
    {"id": "3f169d4d-ef33-4555-861e-3c8aaf0d1ae1", "name": "acoustic vibration test equipment"},  # /PS-IGNORE
]


def prefix_json_url_with_query(search_term=None):
    query = f"?name={search_term}" if search_term else ""
    return reverse("report_summary:prefix") + query


@pytest.fixture
def prefix_json_url():
    return prefix_json_url_with_query()


@pytest.fixture
def subject_json_url():
    return reverse("report_summary:subject")


@pytest.fixture
def mock_prefixes_get(requests_mock):
    return requests_mock.get("/static/report_summary/prefixes/", json={REPORT_SUMMARY_PREFIXES: prefix_data})


@pytest.fixture
def mock_subjects_get(requests_mock):
    return requests_mock.get("/static/report_summary/subjects/", json={REPORT_SUMMARY_SUBJECTS: subject_data})


def test_prefixes_json_view(authorized_client, prefix_json_url, mock_prefixes_get):
    response = authorized_client.get(prefix_json_url)

    assert response.status_code == 200

    data = response.json()
    assert REPORT_SUMMARY_PREFIXES in data
    prefixes = data[REPORT_SUMMARY_PREFIXES]
    assert len(prefixes) == len(prefix_data)

    for item in prefixes:
        assert item in prefix_data


@pytest.mark.parametrize(
    "name, search_term, expected_result",
    [
        (
            "single letter",
            "c",
            ["components for", "countermeasure equipment for", "counter-countermeasure equipment for"],
        ),
        ("two letters", "cou", ["countermeasure equipment for", "counter-countermeasure equipment for"]),
        ("narrowed to one result", "counter-", ["counter-countermeasure equipment for"]),
    ],
)
def test_prefixes_json_view_filters_by_name_param(
    name, authorized_client, mock_prefixes_get, search_term, expected_result
):
    response = authorized_client.get(prefix_json_url_with_query(search_term))

    assert response.status_code == 200

    data = response.json()
    assert REPORT_SUMMARY_PREFIXES in data
    prefixes = data[REPORT_SUMMARY_PREFIXES]
    assert len(prefixes) == len(expected_result)
    assert set([prefix["name"] for prefix in prefixes]) == set(expected_result)


def test_prefix_json_view_permission_not_required(
    authorized_client,
    prefix_json_url,
    mock_prefixes_get,
    mock_gov_user,
    requests_mock,
    gov_uk_user_id,
):
    mock_gov_user["user"]["role"]["permissions"] = []

    url = client._build_absolute_uri("/gov-users/")
    requests_mock.get(url=f"{url}me/", json=mock_gov_user)
    requests_mock.get(url=re.compile(f"{url}{gov_uk_user_id}/"), json=mock_gov_user)

    response = authorized_client.get(prefix_json_url)
    assert response.status_code == 200


def test_subjects_json_view(authorized_client, subject_json_url, mock_subjects_get):
    response = authorized_client.get(subject_json_url)

    assert response.status_code == 200

    data = response.json()
    assert REPORT_SUMMARY_SUBJECTS in data
    subjects = data[REPORT_SUMMARY_SUBJECTS]
    assert len(subjects) == len(subject_data)

    for item in subjects:
        assert item in subject_data


def test_subject_json_view_permission_not_required(
    authorized_client,
    subject_json_url,
    mock_subjects_get,
    mock_gov_user,
    requests_mock,
    gov_uk_user_id,
):
    mock_gov_user["user"]["role"]["permissions"] = []

    url = client._build_absolute_uri("/gov-users/")
    requests_mock.get(url=f"{url}me/", json=mock_gov_user)
    requests_mock.get(url=re.compile(f"{url}{gov_uk_user_id}/"), json=mock_gov_user)

    response = authorized_client.get(subject_json_url)
    assert response.status_code == 200
