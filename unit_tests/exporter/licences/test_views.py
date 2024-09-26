import pytest
import uuid

from pytest_django.asserts import assertTemplateUsed

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
def standard_licence():
    return {
        "id": "8379b6ba-06eb-4e0a-9331-c3adc650d4d0",
        "duration": 24,
        "reference_code": "GBSIEL/2020/0002409/T",
        "start_date": "2024-09-19",
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
        "document": {"id": "e9a09168-dca7-4d40-b06a-4e949a7f455c"},
        "goods": [
            {
                "good_on_application_id": "3bcfd636-da6b-4458-a812-f78af77cc8ba",
                "usage": 0.0,
                "description": "Example product",
                "name": "Example product name",
                "units": {"key": "MTR", "value": "Metre(s)"},
                "applied_for_quantity": 1.0,
                "applied_for_value": 1.0,
                "licenced_quantity": 1.0,
                "licenced_value": 1.0,
                "applied_for_value_per_item": 1.0,
                "licenced_value_per_item": 1.0,
                "control_list_entries": [
                    {"rating": "N1"},
                    {"rating": "N2"},
                ],
                "assessed_control_list_entries": [
                    {"rating": "R1a"},
                    {"rating": "MJ1"},
                ],
            }
        ],
    }


@pytest.fixture
def data_list_licences(standard_licence):
    return {
        "count": 1,
        "total_pages": 1,
        "results": [
            standard_licence,
        ],
    }


@pytest.fixture
def not_found_standard_licence_id():
    return uuid.uuid4()


@pytest.fixture
def other_error_standard_licence_id():
    return uuid.uuid4()


@pytest.fixture(autouse=True)
def mock_list_licences(requests_mock, data_list_licences):
    url = _build_absolute_uri("/licences/")
    return requests_mock.get(url=url, json=data_list_licences)


@pytest.fixture(autouse=True)
def mock_licence_detail(requests_mock, standard_licence):
    url = _build_absolute_uri(f"/licences/{standard_licence['id']}")
    return requests_mock.get(url=url, json=standard_licence)


@pytest.fixture(autouse=True)
def mock_not_found_licence_detail(requests_mock, not_found_standard_licence_id):
    url = _build_absolute_uri(f"/licences/{not_found_standard_licence_id}")
    return requests_mock.get(url=url, json={}, status_code=404)


@pytest.fixture(autouse=True)
def mock_other_error_licence_detail(requests_mock, other_error_standard_licence_id):
    url = _build_absolute_uri(f"/licences/{other_error_standard_licence_id}")
    return requests_mock.get(url=url, json={}, status_code=500)


@pytest.fixture(autouse=True)
def mock_list_no_licence_required(data_list_no_licence_required, requests_mock):
    url = _build_absolute_uri("/licences/nlrs/")
    return requests_mock.get(url=url, json=data_list_no_licence_required)


@pytest.fixture(autouse=True)
def mock_list_open_general_licences(data_list_open_general_licences, requests_mock):
    url = _build_absolute_uri(
        "/open-general-licences/?convert_to_options=False&registered=True&disable_pagination=True"
    )
    return requests_mock.get(url=url, json=data_list_open_general_licences)


@pytest.fixture
def client(authorized_client, mock_exporter_control_list_entries, mock_countries, mock_pv_gradings):
    return authorized_client


@pytest.fixture
def list_open_standard_licences_url():
    return reverse("licences:list-open-and-standard-licences")


@pytest.fixture
def standard_licence_url(standard_licence):
    return reverse("licences:licence", kwargs={"pk": standard_licence["id"]})


@pytest.fixture
def not_found_standard_licence_url(not_found_standard_licence_id):
    return reverse("licences:licence", kwargs={"pk": not_found_standard_licence_id})


@pytest.fixture
def other_error_standard_licence_url(other_error_standard_licence_id):
    return reverse("licences:licence", kwargs={"pk": other_error_standard_licence_id})


def test_open_and_standard_licences(client, data_list_licences, list_open_standard_licences_url, mock_list_licences):
    expected_filters = ["reference", "clc", "country", "end_user", "active_only", "licence_type"]
    session = client.session
    session["organisation_name"] = "test company"
    session.save()

    response = client.get(list_open_standard_licences_url)
    assert response.status_code == 200
    assert len(mock_list_licences.request_history) == 1
    assert mock_list_licences.last_request.qs == {"licence_type": ["licence"]}
    assert response.context_data["data"] == data_list_licences
    assert [item.name for item in response.context_data["filters"].filters] == expected_filters


def test_standard_licences_details(
    client, data_list_licences, list_open_standard_licences_url, mock_list_licences, beautiful_soup
):
    response = client.get(list_open_standard_licences_url)
    assert response.status_code == 200

    soup = beautiful_soup(response.content)

    licence_details_table = soup.find(id="licence-details-table")
    assert licence_details_table
    licence_rows = licence_details_table.select(".licence-details-table__licence_row")
    assert len(licence_rows) == len(data_list_licences["results"])
    for licence_row, licence_data in zip(licence_rows, data_list_licences["results"]):
        assert licence_row.attrs["id"] == f"licence-{licence_data['id']}"
        assert (
            licence_row.select_one(".licence-details-table__licence_reference_code").text
            == licence_data["reference_code"]
        )
        assert (
            licence_row.select_one(".licence-details-table__licence_application_name").text
            == licence_data["application"]["name"]
        )

        goods = licence_row.select(".licence-details-table__goods .app-expanded-row__item")
        for line_number, (good, good_data) in enumerate(zip(goods, licence_data["goods"]), start=1):
            assert good.select_one(".licence-details-table__good_line_number").text == f"{line_number}."
            assert [cle.text.replace(",", "").strip() for cle in good.select(".lite-inline-list li")] == [
                cle["rating"] for cle in good_data["assessed_control_list_entries"]
            ]
            assert good.select_one(".licence-details-table__good_name").text == good_data["name"]

        destinations = licence_row.select(".licence-details-table__destinations .app-expanded-row__item")
        for destination, destination_data in zip(destinations, licence_data["application"]["destinations"]):
            assert destination.text.strip() == f"{destination_data['name']} - {destination_data['country']['name']}"

        assert licence_row.select_one(".licence-details-table__licence-status").text == "Issued"

        documents = licence_row.select(".licence-details-table__application-documents")
        for document, document_data in zip(documents, licence_data["application"]["documents"]):
            document_link = document.select_one("#document-download")
            assert document_link.text == f"{document_data['advice_type']['value']}.pdf"
            assert document_link.attrs["href"] == reverse(
                "applications:download_generated_document",
                kwargs={"document_pk": document_data["id"], "case_pk": licence_data["application"]["id"]},
            )


def test_open_and_standard_licences_paging(client, list_open_standard_licences_url, mock_list_licences):
    session = client.session
    session["organisation_name"] = "test company"
    session.save()

    response = client.get(f"{list_open_standard_licences_url}?page=2")
    assert response.status_code == 200
    assert len(mock_list_licences.request_history) == 1
    assert mock_list_licences.last_request.qs == {
        "licence_type": ["licence"],
        "page": ["2"],
    }


def test_standard_licence_page(client, standard_licence_url):
    response = client.get(standard_licence_url)
    assert response.status_code == 200
    assertTemplateUsed("licences/licence.html")


def test_standard_licence_page_not_found(client, not_found_standard_licence_url):
    response = client.get(not_found_standard_licence_url)
    assert response.status_code == 404


def test_standard_licence_page_other_error(client, other_error_standard_licence_url):
    response = client.get(other_error_standard_licence_url)
    assert response.status_code == 200
    assertTemplateUsed("error.html")


def test_open_general_licences(client, data_list_open_general_licences, mock_list_open_general_licences):
    expected_filters = ["name", "case_type", "control_list_entry", "country", "site", "active_only", "licence_type"]

    response = client.get(reverse("licences:list-open-general-licences"))
    assert response.status_code == 200
    assert len(mock_list_open_general_licences.request_history) == 1
    assert mock_list_open_general_licences.last_request.qs == {
        "convert_to_options": ["false"],
        "disable_pagination": ["true"],
        "registered": ["true"],
    }
    assert response.context_data["data"] == data_list_open_general_licences
    assert [item.name for item in response.context_data["filters"].filters] == expected_filters


@pytest.fixture
def list_no_licence_required_url():
    return reverse("licences:list-no-licence-required")


def test_no_licence_required(
    client, data_list_no_licence_required, list_no_licence_required_url, mock_list_no_licence_required
):
    expected_filters = ["reference", "clc", "country", "end_user", "licence_type"]

    response = client.get(list_no_licence_required_url)
    assert response.status_code == 200
    assert len(mock_list_no_licence_required.request_history) == 1
    assert mock_list_no_licence_required.last_request.qs == {}
    assert response.context_data["data"] == data_list_no_licence_required
    assert [item.name for item in response.context_data["filters"].filters] == expected_filters


def test_no_licence_required_paging(client, list_no_licence_required_url, mock_list_no_licence_required):
    response = client.get(f"{list_no_licence_required_url}?page=2")
    assert response.status_code == 200
    assert len(mock_list_no_licence_required.request_history) == 1
    assert mock_list_no_licence_required.last_request.qs == {"page": ["2"]}


@pytest.fixture
def list_clearances_url():
    return reverse("licences:list-clearances")


def test_clearances(client, data_list_licences, list_clearances_url, mock_list_licences):
    expected_filters = ["reference", "clc", "country", "end_user", "active_only", "licence_type"]

    response = client.get(list_clearances_url)
    assert response.status_code == 200
    assert len(mock_list_licences.request_history) == 1
    assert mock_list_licences.last_request.qs == {"licence_type": ["clearance"]}
    assert response.context_data["data"] == data_list_licences
    assert [item.name for item in response.context_data["filters"].filters] == expected_filters


def test_clearances_paging(client, list_clearances_url, mock_list_licences):
    response = client.get(f"{list_clearances_url}?page=2")
    assert response.status_code == 200
    assert len(mock_list_licences.request_history) == 1
    assert mock_list_licences.last_request.qs == {"licence_type": ["clearance"], "page": ["2"]}
