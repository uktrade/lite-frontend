import pytest
from django.urls import reverse
from bs4 import BeautifulSoup

from core import client


@pytest.fixture(autouse=True)
def mock_get_application(requests_mock, data_standard_case):
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


def test_application_summary_view(authorized_client, summary_url, mock_get_application, mock_get_case_notes):
    """
    This tests that the case data in data_standard_case is shown in the
    application summary view. It just checks for the presence of these strings
    and does not check the structure or layout. The test is intended to be a
    minimal amount of test coverage to catch regressions such as if any of
    these items stop being displayed in the application summary view.
    """
    response = authorized_client.get(summary_url)

    assert response.status_code == 200
    soup = BeautifulSoup(response.content, "html.parser")
    headings_govuk_heading_m = soup.find_all("h2", class_="govuk-heading-m")
    headings_govuk_heading_m_text = [heading.text for heading in headings_govuk_heading_m]
    assert headings_govuk_heading_m_text == [
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
        "Ultimate end-user",
        "Notes",
    ]
    table_data_govuk_table_cell = soup.find_all("td", class_="govuk-table__cell")
    table_data_govuk_table_cell_text = [data.text for data in table_data_govuk_table_cell]
    assert table_data_govuk_table_cell_text == [
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
        "1.",
        "Ultimate End-user",
        "Individual",
        "44, United Kingdom",
        "N/A",
        "Attach document",
    ]
