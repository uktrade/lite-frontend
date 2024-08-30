import pytest
from django.urls import reverse
from bs4 import BeautifulSoup

from core import client
from exporter.applications.constants import ApplicationStatus


@pytest.fixture(autouse=True)
def mock_get_application(requests_mock, data_standard_case):
    data_standard_case["case"]["data"]["status"] = {"key": ApplicationStatus.DRAFT, "value": "Draft"}
    applications_url = client._build_absolute_uri(f"/applications/{data_standard_case['case']['id']}/")
    requests_mock.get(url=applications_url, json=data_standard_case["case"]["data"])


@pytest.fixture
def mock_get_case_notes(application, requests_mock):
    return requests_mock.get(
        f"/cases/{application['id']}/case-notes/",
        json={"case_notes": []},
    )


@pytest.fixture
def summary_url(data_standard_case):
    return reverse("applications:summary", kwargs={"pk": data_standard_case["case"]["id"]})


@pytest.mark.parametrize(
    ("expected_headings", "expected_table_data"),
    [
        (
            [
                "Do you have a security approval?",
                "Products",
                "End use details",
                "End user",
                "Consignee",
                "Third parties",
                "Supporting documents",
                "Route of products",
                "Locations",
                "Temporary export details",
                "Notes",
            ],
            [
                "1.",
                "p1",
                "44",
                "ML1a, ML22b",
                "444.0 gram(s)",
                "£444.00",
                "2.",
                "p2",
                "44",
                "N/A",
                "444.0 gram(s)",
                "£444.00",
                "1.",
                "Intended end use",
                "44",
                "2.",
                "Informed to apply",
                "No",
                "3.",
                "Informed WMD",
                "No",
                "4.",
                "Suspect WMD",
                "No",
                "5.",
                "EU transfer licence",
                "No",
                "1.",
                "Third party",
                "Individual",
                "None",
                "44, United Kingdom",
                "N/A",
                "Consultant",
                "Attach document",
                "1.",
                "Shipped air waybill or lading",
                "No44",
                "1.",
                "44",
                "44, Brunei",
                "1.",
                "Products remaining under your direct control",
                "No44",
                "2.",
                "Date products returning to the UK",
                "2021-01-01",
            ],
        )
    ],
)
def test_application_summary_view(
    authorized_client, summary_url, mock_get_application, mock_get_case_notes, expected_headings, expected_table_data
):
    response = authorized_client.get(summary_url)

    assert response.status_code == 200
    soup = BeautifulSoup(response.content, "html.parser")
    headings_govuk_heading_m = soup.find_all("h2", class_="govuk-heading-m")
    headings_govuk_heading_m_text = [heading.text for heading in headings_govuk_heading_m]
    assert headings_govuk_heading_m_text == expected_headings
    table_data_govuk_table_cell = soup.find_all("td", class_="govuk-table__cell")
    table_data_govuk_table_cell_text = [data.text for data in table_data_govuk_table_cell]
    assert table_data_govuk_table_cell_text == expected_table_data


def test_application_summary_view_shows_ultimate_end_user_good_incorporated(
    data_standard_case, data_goa_good_incorporated, requests_mock, mock_get_case_notes, authorized_client, summary_url
):
    data_standard_case["case"]["data"]["goods"] = [data_goa_good_incorporated]

    applications_url = client._build_absolute_uri(f"/applications/{data_standard_case['case']['id']}/")
    requests_mock.get(url=applications_url, json=data_standard_case["case"]["data"])

    response = authorized_client.get(summary_url)
    assert response.status_code == 200
    soup = BeautifulSoup(response.content, "html.parser")
    headings_govuk_heading_m = soup.find_all("h2", class_="govuk-heading-m")
    headings_govuk_heading_m_text = [heading.text for heading in headings_govuk_heading_m]
    assert "Ultimate end-user" in headings_govuk_heading_m_text
    table_data_govuk_table_cell = soup.find_all("td", class_="govuk-table__cell")
    table_data_govuk_table_cell_text = [data.text for data in table_data_govuk_table_cell]
    assert "Ultimate End-user" in table_data_govuk_table_cell_text


def test_application_summary_view_shows_ultimate_end_user_onward_incorporated(
    data_standard_case, data_goa_onward_incorporated, requests_mock, mock_get_case_notes, authorized_client, summary_url
):
    data_standard_case["case"]["data"]["goods"] = [data_goa_onward_incorporated]

    applications_url = client._build_absolute_uri(f"/applications/{data_standard_case['case']['id']}/")
    requests_mock.get(url=applications_url, json=data_standard_case["case"]["data"])

    response = authorized_client.get(summary_url)
    assert response.status_code == 200
    soup = BeautifulSoup(response.content, "html.parser")
    headings_govuk_heading_m = soup.find_all("h2", class_="govuk-heading-m")
    headings_govuk_heading_m_text = [heading.text for heading in headings_govuk_heading_m]
    assert "Ultimate end-user" in headings_govuk_heading_m_text
    table_data_govuk_table_cell = soup.find_all("td", class_="govuk-table__cell")
    table_data_govuk_table_cell_text = [data.text for data in table_data_govuk_table_cell]
    assert "Ultimate End-user" in table_data_govuk_table_cell_text
