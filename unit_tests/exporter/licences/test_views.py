import pytest

from django.urls import reverse

from core.client import _build_absolute_uri


@pytest.fixture
def data_list_no_licence_required():
    return [
        {
            "count": 1,
            "total_pages": 1,
            "results": [
                {
                    "id": "66297b19-8753-4f37-8b6d-833b8f28727b",
                    "name": "rich-b82a61ea-3611-4504-9477-70e75-3b1ab.pdf",
                    "case_id": "f6911b67-c7ca-4e56-a11e-bf8194e9c6af",
                    "case_reference": "GBSIEL/2020/0003427/P",
                    "goods": [
                        {
                            "description": "Lentils",
                            "control_list_entries": [
                                {
                                    "rating": "ML1a",
                                    "text": "Rifles and combination guns, handguns, machine, sub-machine and volley...",
                                }
                            ],
                        }
                    ],
                    "destinations": [
                        {"party_name": "Tim Time", "country_name": "Ukraine"},
                        {"party_name": "Foo Bar", "country_name": "United Kingdom"},
                        {"party_name": "Dr. Bar Baz", "country_name": "United Kingdom"},
                        {"party_name": "April May", "country_name": "United Kingdom"},
                    ],
                    "advice_type": "no_licence_required",
                }
            ],
        }
    ]


@pytest.fixture
def data_list_open_general_licences():
    return [
        {
            "id": "3c3c01eb-1b49-4e50-a25d-1d1a0f263a74",
            "name": "aggregate out-of-the-box experiences",
            "description": "Talk standard evening happen blue information color population. Fly direction oil type team night.",
            "url": "https://www.gov.uk/government/publications/open-general-export-licence-military-goods-government-or-nato-end-use--6",
            "case_type": {
                "id": "00000000-0000-0000-0000-000000000002",
                "reference": {"key": "ogel", "value": "Open General Export Licence"},
                "type": {"key": "registration", "value": "Registration"},
                "sub_type": {"key": "open", "value": "Open Licence"},
            },
            "countries": [{"id": "GB", "name": "United Kingdom", "type": "gov.uk Country", "is_eu": True}],
            "control_list_entries": [
                {
                    "rating": "ML1a",
                    "text": "Rifles and combination guns, handguns, machine, sub-machine and volley guns",
                }
            ],
            "registration_required": True,
            "status": {"key": "active", "value": "Active"},
            "registrations": [],
            "created_at": "2020-08-18T20:42:27.985942+01:00",
            "updated_at": "2020-08-18T20:42:27.985942+01:00",
        }
    ]


@pytest.fixture
def data_list_licences():
    return {
        "count": 1,
        "total_pages": 1,
        "results": [
            {
                "id": "8379b6ba-06eb-4e0a-9331-c3adc650d4d0",
                "reference_code": "GBSIEL/2020/0002409/T",
                "status": {"key": "issued", "value": "Issued"},
                "application": {
                    "id": "02e181f4-a35c-441e-afee-cd9fe5fde26b",
                    "name": "25/09 - application 2",
                    "destinations": [
                        {
                            "name": "Jim",
                            "address": "Jim",
                            "country": {"id": "TN", "name": "Tunisia", "type": "gov.uk Country", "is_eu": False},
                        }
                    ],
                    "documents": [
                        {
                            "advice_type": {"key": "approve", "value": "Approve"},
                            "id": "be7d9a9a-c66c-4dec-88dc-462ec836d538",
                        }
                    ],
                },
                "goods": [
                    {
                        "good_on_application_id": "3bcfd636-da6b-4458-a812-f78af77cc8ba",
                        "usage": 0.0,
                        "description": "Example product",
                        "units": {"key": "MTR", "value": "Metre(s)"},
                        "applied_for_quantity": 1.0,
                        "applied_for_value": 1.0,
                        "licenced_quantity": 1.0,
                        "licenced_value": 1.0,
                        "applied_for_value_per_item": 1.0,
                        "licenced_value_per_item": 1.0,
                        "control_list_entries": [],
                        "advice": {"type": {"key": "approve", "value": "Approve"}, "text": "", "proviso": None},
                    }
                ],
            }
        ],
    }


@pytest.fixture(autouse=True)
def mock_list_licences(requests_mock, data_list_licences):
    url = _build_absolute_uri("/licences/?page=1")
    return requests_mock.get(url=url, json=data_list_licences)


@pytest.fixture(autouse=True)
def mock_list_no_licence_required(data_list_no_licence_required, requests_mock):
    url = _build_absolute_uri("/licences/nlrs/?page=1")
    return requests_mock.get(url=url, json=data_list_no_licence_required)


@pytest.fixture(autouse=True)
def mock_list_open_general_licences(data_list_open_general_licences, requests_mock):
    url = _build_absolute_uri(
        "/open-general-licences/?convert_to_options=False&registered=True&disable_pagination=True"
    )
    return requests_mock.get(url=url, json=data_list_open_general_licences)


@pytest.fixture
def client(authorized_client, mock_exporter_user, mock_control_list_entries, mock_countries):
    return authorized_client(mock_exporter_user["user"])


def test_open_and_standard_licences(client, data_list_licences):
    expected_filters = ["reference", "clc", "country", "end_user", "active_only", "licence_type"]

    response = client.get(reverse("licences:list-open-and-standard-licences"))
    assert response.status_code == 200
    assert response.context_data["data"] == data_list_licences
    assert [item.name for item in response.context_data["filters"].filters] == expected_filters


def test_open_general_licences(client, data_list_open_general_licences):
    expected_filters = ["name", "case_type", "control_list_entry", "country", "site", "active_only", "licence_type"]

    response = client.get(reverse("licences:list-open-general-licences"))
    assert response.status_code == 200
    assert response.context_data["data"] == data_list_open_general_licences
    assert [item.name for item in response.context_data["filters"].filters] == expected_filters


def test_no_licenece_required(client, data_list_no_licence_required):
    expected_filters = ["reference", "clc", "country", "end_user", "licence_type"]

    response = client.get(reverse("licences:list-no-licence-required"))
    assert response.status_code == 200
    assert response.context_data["data"] == data_list_no_licence_required
    assert [item.name for item in response.context_data["filters"].filters] == expected_filters


def test_clearances(client, data_list_licences):
    expected_filters = ["reference", "clc", "country", "end_user", "active_only", "licence_type"]

    response = client.get(reverse("licences:list-clearances"))
    assert response.status_code == 200
    assert response.context_data["data"] == data_list_licences
    assert [item.name for item in response.context_data["filters"].filters] == expected_filters
