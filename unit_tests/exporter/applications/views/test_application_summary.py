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


def test_application_summary_view(
    authorized_client,
    summary_url,
    mock_get_application,
    mock_get_case_notes,
):
    response = authorized_client.get(summary_url)

    assert response.status_code == 200

    soup = BeautifulSoup(response.content, "html.parser")

    sections = []
    for section in soup.select(".check-your-answers-section"):
        heading = section.select_one("h2").text.strip()

        definition_lists = []
        for definition_list in section.select(".govuk-summary-list"):
            items = []
            for div in definition_list.select(".govuk-summary-list__row"):
                items.append(
                    (
                        div.select_one(".govuk-summary-list__key").text.strip(),
                        div.select_one(".govuk-summary-list__value").text.strip(),
                    )
                )
            definition_lists.append(items)

        tables = []
        for table in section.select(".govuk-table"):
            headings = []
            for header_row in table.select(".govuk-table__head .govuk-table__row"):
                headings.append([cell.text.strip() for cell in header_row.select(".govuk-table__header")])

            rows = []
            for table_row in table.select(".govuk-table__body .govuk-table__row"):
                rows.append([cell.text.strip() for cell in table_row.select(".govuk-table__cell")])

            tables.append((headings, rows))

        sections.append(
            {
                "heading": heading,
                "definitions_lists": definition_lists if definition_lists else None,
                "tables": tables if tables else None,
            }
        )

    assert sections == [
        {
            "heading": "Do you have a security approval?",
            "definitions_lists": [[("Do you have an MOD security approval, such as F680 " "or F1686?", "No")]],
            "tables": None,
        },
        {
            "heading": "Products",
            "definitions_lists": None,
            "tables": [
                (
                    [["#", "Name", "Part number", "Control list entries", "Quantity", "Value"]],
                    [
                        ["1.", "p1", "44", "ML1a, ML22b", "444.0 gram(s)", "£444.00"],
                        ["2.", "p2", "44", "N/A", "444.0 gram(s)", "£444.00"],
                    ],
                )
            ],
        },
        {
            "heading": "End use details",
            "definitions_lists": None,
            "tables": [
                (
                    [["#", "Description", "Answer"]],
                    [
                        ["1.", "Intended end use", "44"],
                        ["2.", "Informed to apply", "No"],
                        ["3.", "Informed WMD", "No"],
                        ["4.", "Suspect WMD", "No"],
                        ["5.", "EU transfer licence", "No"],
                    ],
                )
            ],
        },
        {
            "heading": "End user",
            "definitions_lists": [
                [
                    ("Name", "End User"),
                    ("Type", "Individual"),
                    ("Address", "44, United Kingdom"),
                    ("Website", "N/A"),
                    ("Signatory name", "John Doe"),
                    (
                        "Do you have an end-user document?",
                        "No, I do not have an end-user undertaking or " "stockist undertaking",
                    ),
                    (
                        "Explain why you do not have an end-user undertaking " "or stockist undertaking",
                        "Products details not available as they are not " "manufactured yet",
                    ),
                ]
            ],
            "tables": None,
        },
        {
            "heading": "Consignee",
            "definitions_lists": [
                [
                    ("Name", "Consignee"),
                    ("Type", "Individual"),
                    ("Address", "44, Abu Dhabi"),
                    ("Website", "N/A"),
                    ("Document", "Attach document"),
                ]
            ],
            "tables": None,
        },
        {
            "heading": "Third parties",
            "definitions_lists": None,
            "tables": [
                (
                    [["#", "Name", "Type", "Descriptors", "Address", "Website", "Role", "Document"]],
                    [
                        [
                            "1.",
                            "Third party",
                            "Individual",
                            "None",
                            "44, United Kingdom",
                            "N/A",
                            "Consultant",
                            "Attach document",
                        ]
                    ],
                )
            ],
        },
        {
            "heading": "Supporting documents",
            "definitions_lists": None,
            "tables": None,
        },
        {
            "heading": "Route of products",
            "definitions_lists": None,
            "tables": [([["#", "Description", "Answer"]], [["1.", "Shipped air waybill or lading", "No44"]])],
        },
        {
            "heading": "Locations",
            "definitions_lists": None,
            "tables": [([["#", "Name", "Address"]], [["1.", "44", "44, Brunei"]])],
        },
        {
            "heading": "Temporary export details",
            "definitions_lists": None,
            "tables": [
                (
                    [["#", "Description", "Answer"]],
                    [
                        ["1.", "Products remaining under your direct control", "No44"],
                        ["2.", "Date products returning to the UK", "2021-01-01"],
                    ],
                )
            ],
        },
    ]


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
