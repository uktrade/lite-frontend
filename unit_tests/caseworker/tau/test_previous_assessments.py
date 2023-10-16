import pytest
import re

from bs4 import BeautifulSoup
import rules

from django.urls import reverse

from core import client
from caseworker.tau import views


@pytest.fixture(autouse=True)
def setup(
    mock_queue,
    mock_case,
    mock_mtcr_entries_get,
    mock_wassenaar_entries_get,
    mock_nsg_entries_get,
    mock_cwc_entries_get,
    mock_ag_entries_get,
    mock_application_good_documents,
):
    yield


@pytest.fixture
def previous_assessments_url(data_standard_case):
    return reverse(
        "cases:tau:previous_assessments",
        kwargs={"queue_pk": "1b926457-5c9e-4916-8497-51886e51863a", "pk": data_standard_case["case"]["id"]},
    )


@pytest.fixture
def good_precedent(requests_mock, data_standard_case, data_queue):
    # Remove assessment from a good
    good = data_standard_case["case"]["data"]["goods"][0]
    good["is_good_controlled"] = None
    good["control_list_entries"] = []
    good["firearm_details"]["year_of_manufacture"] = "1930"

    case_id = data_standard_case["case"]["id"]
    precedents_url = client._build_absolute_uri(f"/cases/{case_id}/good-precedents/")
    requests_mock.get(
        precedents_url,
        json={
            "results": [
                {
                    "id": "6daad1c3-cf97-4aad-b711-d5c9a9f4586e",
                    "good": "8b730c06-ab4e-401c-aeb0-32b3c92e912c",
                    "application": case_id,
                    "queue": data_queue["id"],
                    "reference": data_standard_case["case"]["reference_code"],
                    "destinations": ["France"],
                    "control_list_entries": ["ML1a"],
                    "wassenaar": False,
                    "quantity": 10.0,
                    "value": "test-value",
                    "report_summary": "test-report-summary",
                    "submitted_at": "2021-06-21T11:27:36.145000Z",
                    "goods_starting_point": "GB",
                },
            ]
        },
    )


def test_previous_assessments_GET(
    authorized_client,
    previous_assessments_url,
    data_queue,
    data_standard_case,
    mock_control_list_entries,
    mock_gov_user,
    good_precedent,
):
    response = authorized_client.get(previous_assessments_url)
    assert response.status_code == 200

    # Test elements of case info panel
    soup = BeautifulSoup(response.content, "html.parser")
    assert soup.find("h1", {"class": "govuk-heading-l"}).text == "Previously assessed products"
    table = soup.find("table", id="tau-form")
    assert table
    assert [td.text.strip() for td in table.findAll("td", {"class": "readonly-field"})] == ["p1", "ML1a"]


def test_previous_assessments_GET_no_precedents(
    authorized_client,
    previous_assessments_url,
    data_queue,
    data_standard_case,
    mock_control_list_entries,
    mock_gov_user,
    requests_mock,
):
    # Remove assessment from a good
    good = data_standard_case["case"]["data"]["goods"][0]
    good["is_good_controlled"] = None
    good["control_list_entries"] = []
    good["firearm_details"]["year_of_manufacture"] = "1930"

    case_id = data_standard_case["case"]["id"]
    precedents_url = client._build_absolute_uri(f"/cases/{case_id}/good-precedents/")
    requests_mock.get(
        precedents_url,
        json={"results": []},
    )

    response = authorized_client.get(previous_assessments_url)
    assert response.status_code == 200

    # Test elements of case info panel
    soup = BeautifulSoup(response.content, "html.parser")
    assert soup.find("h1", {"class": "govuk-heading-l"}).text == "Previously assessed products"
    missing_message_paragraph = soup.find("p", id="previous-assessments-missing")
    assert missing_message_paragraph


def test_previous_assessments_POST(
    authorized_client,
    previous_assessments_url,
    data_queue,
    data_standard_case,
    mock_control_list_entries,
    mock_gov_user,
    good_precedent,
):
    response = authorized_client.post(previous_assessments_url, follow=False)
    assert response.status_code == 302
    # TODO: Flesh this out when the form submission is properly handled
    assert (
        response["location"]
        == "/queues/1b926457-5c9e-4916-8497-51886e51863a/cases/8fb76bed-fd45-4293-95b8-eda9468aa254/tau/"  # /PS-IGNORE
    )
