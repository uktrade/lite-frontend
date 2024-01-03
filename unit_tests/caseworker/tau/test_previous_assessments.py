import pytest
import re
from urllib.parse import urlparse

from bs4 import BeautifulSoup
import rules

from django.urls import reverse

from caseworker.core.constants import ALL_CASES_QUEUE_ID
from core import client
from caseworker.tau import views
from core.exceptions import ServiceError


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
def good_precedent_url(data_good_precedent):
    url = (
        reverse("cases:tau:home", kwargs={"pk": data_good_precedent["application"], "queue_pk": ALL_CASES_QUEUE_ID})
        + "#good-"
        + data_good_precedent["id"]
    )
    return url


@pytest.fixture
def data_good_precedent(data_standard_case, data_queue):
    case_id = data_standard_case["case"]["id"]
    return {
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
        "is_good_controlled": True,
        "regime_entries": [{"pk": "regime-0001", "name": "some regime"}],
        "report_summary_prefix": {"id": "0001", "name": "some prefix"},
        "report_summary_subject": {"id": "0002", "name": "some subject"},
        "comment": "some assessment note",
        "is_ncsc_military_information_security": False,
    }


@pytest.fixture
def mock_good_precedent_endpoint(requests_mock, data_standard_case, data_good_precedent, data_queue):
    case_id = data_standard_case["case"]["id"]

    data_good_precedent_copy = data_good_precedent.copy()
    data_good_precedent_copy["good"] = "6a7fc61f-698b-46b6-9876-6ac0fddfb1a2"

    results = [data_good_precedent, data_good_precedent_copy]

    # Remove assessment from a good
    good = data_standard_case["case"]["data"]["goods"][0]
    good["is_good_controlled"] = None
    good["control_list_entries"] = []
    good["firearm_details"]["year_of_manufacture"] = "1930"

    good_1 = data_standard_case["case"]["data"]["goods"][1]
    good_1["is_good_controlled"] = None
    good_1["control_list_entries"] = []

    precedents_url = client._build_absolute_uri(f"/cases/{case_id}/good-precedents/")
    requests_mock.get(
        precedents_url,
        json={"results": results},
    )


@pytest.fixture
def mock_single_good_precedent_endpoint(requests_mock, data_standard_case, data_good_precedent, data_queue):
    case_id = data_standard_case["case"]["id"]

    # Single good with previous assessment
    results = [data_good_precedent]

    # Remove assessment from a good
    good = data_standard_case["case"]["data"]["goods"][0]
    good["is_good_controlled"] = None
    good["control_list_entries"] = []
    good["firearm_details"]["year_of_manufacture"] = "1930"

    # Remove assessment from other good
    good = data_standard_case["case"]["data"]["goods"][1]
    good["is_good_controlled"] = None
    good["control_list_entries"] = []

    precedents_url = client._build_absolute_uri(f"/cases/{case_id}/good-precedents/")
    requests_mock.get(
        precedents_url,
        json={"results": results},
    )


def test_previous_assessments_GET(
    settings,
    authorized_client,
    previous_assessments_url,
    data_queue,
    data_standard_case,
    mock_control_list_entries,
    mock_gov_user,
    mock_good_precedent_endpoint,
):
    response = authorized_client.get(previous_assessments_url)
    assert response.status_code == 200

    # Test elements of case info panel
    soup = BeautifulSoup(response.content, "html.parser")
    assert soup.find("a", id="tab-assessment")["href"].endswith("tau/previous-assessments/")
    assert soup.find("h1", {"class": "govuk-heading-l"}).text == "Product assessment"

    table = soup.find("table", id="tau-form")
    assert table
    table_rows = table.select("tbody tr")
    assert len(table_rows) == 2

    def get_td_text(table_row):
        return [td.text.strip().strip() for td in table_row.findAll("td", {"class": "readonly-field"})]

    assert get_td_text(table_rows[0]) == [
        "1.",
        "p1 44",
        data_standard_case["case"]["reference_code"],
        "ML1a",
        "Yes",
        "some regime",
        "some prefix some subject",
        "No",
        "some assessment note",
    ]
    assert get_td_text(table_rows[1]) == [
        "2.",
        "p2 44",
        data_standard_case["case"]["reference_code"],
        "ML1a",
        "Yes",
        "some regime",
        "some prefix some subject",
        "No",
        "some assessment note",
    ]

    notification_banner = soup.find("p", class_="govuk-notification-banner__heading")
    assert notification_banner.get_text() == "2 products going from Great Britain to Abu Dhabi and United Kingdom."


def test_previous_assessments_GET_single_precedent_and_single_new_product(
    authorized_client,
    previous_assessments_url,
    data_queue,
    good_precedent_url,
    data_standard_case,
    mock_control_list_entries,
    mock_gov_user,
    mock_single_good_precedent_endpoint,
):
    response = authorized_client.get(previous_assessments_url)
    assert response.status_code == 200

    # Test elements of case info panel
    soup = BeautifulSoup(response.content, "html.parser")
    assert soup.find("h1", {"class": "govuk-heading-l"}).text == "Product assessment"

    table = soup.find("table", id="tau-form")
    assert table
    table_rows = table.select("tbody tr")
    assert len(table_rows) == 2

    def get_case_links():
        return [
            anchor.attrs["href"]
            for anchor in table.findAll("a", href=lambda value: "good-" in urlparse(value).fragment)
        ]

    def get_td_text(table_row):
        return [td.text.strip().strip() for td in table_row.findAll("td", {"class": "readonly-field"})]

    assert get_td_text(table_rows[0]) == [
        "1.",
        "p1 44",
        data_standard_case["case"]["reference_code"],
        "ML1a",
        "Yes",
        "some regime",
        "some prefix some subject",
        "No",
        "some assessment note",
    ]
    assert get_td_text(table_rows[1]) == ["2.", "p2 44  NOT YET ASSESSED", "", "", "", "", "", "", ""]

    notification_banner = soup.find("p", class_="govuk-notification-banner__heading")
    assert notification_banner.get_text() == "2 products going from Great Britain to Abu Dhabi and United Kingdom."

    expected_case_links = [good_precedent_url]
    case_links = get_case_links()

    assert case_links == expected_case_links


def test_previous_assessments_GET_no_precedents(
    authorized_client,
    previous_assessments_url,
    data_queue,
    data_standard_case,
    mock_control_list_entries,
    mock_gov_user,
    requests_mock,
):
    """If there are no precedents then the previous assessments page should redirect to the all assessments page"""
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
    assert response.status_code == 302
    assert (
        response["location"]
        == "/queues/1b926457-5c9e-4916-8497-51886e51863a/cases/8fb76bed-fd45-4293-95b8-eda9468aa254/tau/"  # /PS-IGNORE
    )


def test_previous_assessments_POST(
    authorized_client,
    previous_assessments_url,
    data_queue,
    data_standard_case,
    mock_control_list_entries,
    mock_gov_user,
    mock_good_precedent_endpoint,
    data_good_precedent,
    requests_mock,
    tau_assessment_url,
    api_make_assessment_url,
):
    mocked_assessment_endpoint = requests_mock.put(api_make_assessment_url, json={})

    good_on_application_id = data_standard_case["case"]["data"]["goods"][0]["id"]
    data = {
        "form-TOTAL_FORMS": 1,
        "form-INITIAL_FORMS": 0,
        "form-0-use_latest_precedent": True,
        "form-0-good_on_application_id": good_on_application_id,
        "form-0-latest_precedent_id": "6daad1c3-cf97-4aad-b711-d5c9a9f4586e",
        "form-0-comment": "test comment",
    }
    response = authorized_client.post(previous_assessments_url, data, follow=True)
    assert response.status_code == 200
    assert mocked_assessment_endpoint.last_request.json() == [
        {
            "control_list_entries": data_good_precedent["control_list_entries"],
            "report_summary_subject": data_good_precedent["report_summary_subject"]["id"],
            "report_summary_prefix": data_good_precedent["report_summary_prefix"]["id"],
            "comment": "test comment",
            "id": good_on_application_id,
            "is_good_controlled": data_good_precedent["is_good_controlled"],
            "regime_entries": [data_good_precedent["regime_entries"][0]["pk"]],
            "is_ncsc_military_information_security": data_good_precedent["is_ncsc_military_information_security"],
            "report_summary": data_good_precedent["report_summary"],
        }
    ]
    messages = [str(msg) for msg in response.context["messages"]]
    expected_message = "Assessed 1 products using previous assessments."
    assert messages == [expected_message]
    assert response.redirect_chain[-1][0] == tau_assessment_url


def test_previous_assessments_POST_mismatched_latest_precedent(
    authorized_client,
    previous_assessments_url,
    data_queue,
    data_standard_case,
    mock_control_list_entries,
    mock_gov_user,
    mock_good_precedent_endpoint,
    requests_mock,
    api_make_assessment_url,
):
    mocked_assessment_endpoint = requests_mock.put(api_make_assessment_url, json={})

    good_on_application_id = data_standard_case["case"]["data"]["goods"][0]["id"]
    data = {
        "form-TOTAL_FORMS": 1,
        "form-INITIAL_FORMS": 0,
        "form-0-use_latest_precedent": True,
        "form-0-good_on_application_id": good_on_application_id,
        "form-0-latest_precedent_id": "00000000-0000-0000-0000-000000000001",
    }
    response = authorized_client.post(previous_assessments_url, data)
    assert response.status_code == 200
    assert not mocked_assessment_endpoint.called
    assert response.context["formset"].non_form_errors() == [
        "A new assessment was made which supersedes your chosen previous assessment."
    ]


def test_previous_assessments_POST_no_products_selected(
    authorized_client,
    previous_assessments_url,
    data_queue,
    data_standard_case,
    mock_control_list_entries,
    mock_gov_user,
    mock_good_precedent_endpoint,
    data_good_precedent,
    requests_mock,
    tau_assessment_url,
    api_make_assessment_url,
):
    mocked_assessment_endpoint = requests_mock.put(api_make_assessment_url, json={})

    good_on_application_id = data_standard_case["case"]["data"]["goods"][0]["id"]
    data = {
        "form-TOTAL_FORMS": 1,
        "form-INITIAL_FORMS": 0,
        "form-0-use_latest_precedent": False,
        "form-0-good_on_application_id": good_on_application_id,
        "form-0-latest_precedent_id": "6daad1c3-cf97-4aad-b711-d5c9a9f4586e",
    }
    response = authorized_client.post(previous_assessments_url, data, follow=True)
    assert response.status_code == 200
    assert not mocked_assessment_endpoint.called
    assert response.redirect_chain[-1][0] == tau_assessment_url


def test_previous_assessments_POST_form_invalid(
    authorized_client,
    previous_assessments_url,
    data_queue,
    data_standard_case,
    mock_control_list_entries,
    mock_gov_user,
    mock_good_precedent_endpoint,
    data_good_precedent,
    requests_mock,
    api_make_assessment_url,
):
    mocked_assessment_endpoint = requests_mock.put(api_make_assessment_url, json={})

    good_on_application_id = data_standard_case["case"]["data"]["goods"][0]["id"]
    data = {
        "form-TOTAL_FORMS": 1,
        "form-INITIAL_FORMS": 0,
        "form-0-use_latest_precedent": False,
        "form-0-good_on_application_id": good_on_application_id,
        "form-0-latest_precedent_id": "invalid-uuid",
    }
    response = authorized_client.post(previous_assessments_url, data)
    assert response.status_code == 200
    assert not mocked_assessment_endpoint.called
    assert response.context["formset"].forms[0].errors == {"latest_precedent_id": ["Enter a valid UUID."]}


@pytest.mark.parametrize(
    "is_system_queue",
    (
        True,
        False,
    ),
)
def test_case_assign_me_button_when_user_is_already_assigned(
    is_system_queue,
    authorized_client,
    data_queue,
    data_standard_case,
    mock_gov_user,
    assign_user_to_case,
    mock_good_precedent_endpoint,
    previous_assessments_url,
):
    # Ported from test_case_assign_me_button_when_user_is_already_assigned in test_case_details

    data_queue["is_system_queue"] = is_system_queue
    assign_user_to_case(
        mock_gov_user,
        data_standard_case,
    )

    response = authorized_client.get(previous_assessments_url)
    assert response.status_code == 200

    html = BeautifulSoup(response.content, "html.parser")
    needs_allocation = html.find(id="allocation-warning")

    assert not needs_allocation


@pytest.mark.parametrize(
    "is_system_queue",
    (
        True,
        False,
    ),
)
def test_case_assign_me_button_when_user_is_not_assigned(
    is_system_queue,
    authorized_client,
    data_queue,
    data_standard_case,
    mock_gov_user,
    mock_good_precedent_endpoint,
    previous_assessments_url,
):
    # Ported from test_case_assign_me_button_when_user_is_not_assigned in test_case_details

    data_queue["is_system_queue"] = is_system_queue
    response = authorized_client.get(previous_assessments_url)
    assert response.status_code == 200

    html = BeautifulSoup(response.content, "html.parser")
    needs_allocation = html.find(id="allocation-warning")
    banner_form = html.find("form", attrs={"class": "app-case-warning-banner__action-form"})

    assert "You need to allocate yourself or someone else to this case to work on it" in needs_allocation.text
    assert needs_allocation.find(id="allocate-case-link").text == "Allocate case"
    if not is_system_queue:
        assert needs_allocation.find(id="allocate-to-me-button").text == "Allocate to me"
        assert banner_form.find(id="id_return_to").get("value") == f"http://testserver{previous_assessments_url}"
        assert banner_form.find(id="id_case_id").get("value") == data_standard_case["case"]["id"]
        assert banner_form.find(id="id_user_id").get("value") == mock_gov_user["user"]["id"]


@pytest.fixture
def mock_previous_assessments_POST_failure(
    requests_mock,
    data_standard_case,
    api_make_assessment_url,
):
    return requests_mock.put(
        api_make_assessment_url,
        json={},
        status_code=500,
    )


def test_previous_assessments_POST_failure(
    authorized_client,
    mock_previous_assessments_POST_failure,
    mock_good_precedent_endpoint,
    previous_assessments_url,
    data_standard_case,
):
    good_on_application_id = data_standard_case["case"]["data"]["goods"][0]["id"]
    data = {
        "form-TOTAL_FORMS": 1,
        "form-INITIAL_FORMS": 0,
        "form-0-use_latest_precedent": True,
        "form-0-good_on_application_id": good_on_application_id,
        "form-0-latest_precedent_id": "6daad1c3-cf97-4aad-b711-d5c9a9f4586e",
    }

    with pytest.raises(ServiceError) as ex:
        response = authorized_client.post(previous_assessments_url, data, follow=True)

    assert ex.value.status_code == 500
    assert str(ex.value) == "Error assessing good with previous assessments"
    assert ex.value.user_message == "Unexpected error assessing good with previous assessments"


def test_multiple_previous_assesments_POST(
    authorized_client,
    requests_mock,
    data_standard_case,
    previous_assessments_url,
    mock_good_precedent_endpoint,
    mock_control_list_entries,
    api_make_assessment_url,
):
    additional_good = {
        "id": "6daad1c3-5b71-44e3-9022-bb57c351081f",
        "good": {
            "id": "6a7fc61f-54d4-471e-bf37-c00e2ef126c1",
            "name": "test",
            "control_list_entries": [
                {
                    "id": "0b9116c2-3aa0-49fb-a590-944b47312345",
                    "rating": "ML1a",
                    "text": "test",
                }
            ],
            "is_good_controlled": {"key": "True", "value": "Yes"},
            "flags": [],
            "documents": [
                {
                    "id": "6c48a2cc-1ed9-49a5-8ca7-df8af5fc2335",
                    "name": "data_sheet.pdf",
                    "description": "product data sheet",
                    "safe": True,
                }
            ],
            "status": {"key": "verified", "value": "Verified"},
            "item_category": {"key": "group2_firearms", "value": "Firearm"},
            "is_document_available": True,
            "firearm_details": {},
            "is_precedent": False,
        },
        "quantity": 1.0,
        "unit": {"key": "NAR", "value": "Items"},
        "value": "1",
        "flags": [],
        "is_good_controlled": None,
        "control_list_entries": [],
        "precedents": [],
        "latest_precedent": None,
    }

    data_standard_case["case"]["data"]["goods"].append(additional_good)
    good_1 = data_standard_case["case"]["data"]["goods"][0]
    good_on_application_id_1 = good_1["id"]

    good_2 = data_standard_case["case"]["data"]["goods"][1]
    good_on_application_id_2 = good_2["id"]

    mocked_assessment_endpoint = requests_mock.put(api_make_assessment_url, json={})

    data = {
        "form-TOTAL_FORMS": 3,
        "form-INITIAL_FORMS": 0,
        "form-0-use_latest_precedent": True,
        "form-0-good_on_application_id": good_on_application_id_1,
        "form-0-latest_precedent_id": "6daad1c3-cf97-4aad-b711-d5c9a9f4586e",
        "form-1-use_latest_precedent": True,
        "form-1-good_on_application_id": good_on_application_id_2,
        "form-1-latest_precedent_id": "6daad1c3-cf97-4aad-b711-d5c9a9f4586e",
        "form-2-use_latest_precedent": "",
        "form-2-good_on_application_id": data_standard_case["case"]["data"]["goods"][2]["id"],
        "form-2-latest_precedent_id": "",
    }

    response = authorized_client.post(previous_assessments_url, data, follow=True)
    assert response.status_code == 200

    request_body = mocked_assessment_endpoint.request_history[0].json()
    assert request_body[0]["id"] == good_on_application_id_1
    assert request_body[1]["id"] == good_on_application_id_2

    messages = [str(msg) for msg in response.context["messages"]]
    expected_message = "Assessed 2 products using previous assessments."
    assert messages == [expected_message]
