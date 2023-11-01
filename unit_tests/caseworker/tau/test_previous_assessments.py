import pytest
import re

from bs4 import BeautifulSoup
import rules

from django.urls import reverse

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
def tau_assessment_url(data_standard_case):
    return reverse(
        "cases:tau:home",
        kwargs={"queue_pk": "1b926457-5c9e-4916-8497-51886e51863a", "pk": data_standard_case["case"]["id"]},
    )


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
        "comment": "woop!",
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

    case_id = data_standard_case["case"]["id"]
    precedents_url = client._build_absolute_uri(f"/cases/{case_id}/good-precedents/")
    requests_mock.get(
        precedents_url,
        json={"results": results},
    )


@pytest.mark.parametrize(
    "feature_flag_active, expected_product_assessment_tab_url",
    ((True, "tau/previous-assessments/"), (False, "tau/")),
)
def test_previous_assessments_GET(
    feature_flag_active,
    expected_product_assessment_tab_url,
    settings,
    authorized_client,
    previous_assessments_url,
    data_queue,
    data_standard_case,
    mock_control_list_entries,
    mock_gov_user,
    mock_good_precedent_endpoint,
):
    settings.FEATURE_TAU_PREVIOUS_ASSESSMENTS = feature_flag_active
    response = authorized_client.get(previous_assessments_url)
    assert response.status_code == 200

    # Test elements of case info panel
    soup = BeautifulSoup(response.content, "html.parser")
    assert soup.find("a", id="tab-assessment")["href"].endswith(expected_product_assessment_tab_url)
    assert soup.find("h1", {"class": "govuk-heading-l"}).text == "Previously assessed products"
    table = soup.find("table", id="tau-form")
    assert table
    assert [td.text.strip().strip() for td in table.findAll("td", {"class": "readonly-field"})] == [
        "p1",
        "44",
        "ML1a",
        "Yes",
        "some regime",
        "some prefix some subject",
        "woop!",
        "No",
        "p2",
        "44",
        "ML1a",
        "Yes",
        "some regime",
        "some prefix some subject",
        "woop!",
        "No",
    ]
    table = soup.find("table", id="tau-form")


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
):
    mocked_assessment_endpoint = requests_mock.post(
        client._build_absolute_uri(f"/goods/control-list-entries/{data_standard_case['case']['id']}"), json={}
    )

    good_on_application_id = data_standard_case["case"]["data"]["goods"][0]["id"]
    data = {
        "form-TOTAL_FORMS": 1,
        "form-INITIAL_FORMS": 0,
        "form-0-use_latest_precedent": True,
        "form-0-good_on_application_id": good_on_application_id,
        "form-0-latest_precedent_id": "6daad1c3-cf97-4aad-b711-d5c9a9f4586e",
    }
    response = authorized_client.post(previous_assessments_url, data, follow=True)
    assert response.status_code == 200
    assert mocked_assessment_endpoint.last_request.json() == {
        "control_list_entries": data_good_precedent["control_list_entries"],
        "report_summary_subject": data_good_precedent["report_summary_subject"]["id"],
        "report_summary_prefix": data_good_precedent["report_summary_prefix"]["id"],
        "comment": data_good_precedent["comment"],
        "objects": [good_on_application_id],
        "is_good_controlled": data_good_precedent["is_good_controlled"],
        "regime_entries": [data_good_precedent["regime_entries"][0]["pk"]],
        "is_ncsc_military_information_security": data_good_precedent["is_ncsc_military_information_security"],
        "report_summary": data_good_precedent["report_summary"],
    }
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
):
    mocked_assessment_endpoint = requests_mock.post(
        client._build_absolute_uri(f"/goods/control-list-entries/{data_standard_case['case']['id']}"), json={}
    )

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
):
    mocked_assessment_endpoint = requests_mock.post(
        client._build_absolute_uri(f"/goods/control-list-entries/{data_standard_case['case']['id']}"), json={}
    )

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
):
    mocked_assessment_endpoint = requests_mock.post(
        client._build_absolute_uri(f"/goods/control-list-entries/{data_standard_case['case']['id']}"), json={}
    )

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
):
    return requests_mock.post(
        client._build_absolute_uri(f"/goods/control-list-entries/{data_standard_case['case']['id']}"),
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
):
    good_1 = data_standard_case["case"]["data"]["goods"][0]
    good_on_application_id_1 = good_1["id"]

    good_2 = data_standard_case["case"]["data"]["goods"][1]
    good_on_application_id_2 = good_2["id"]

    mocked_assessment_endpoint = requests_mock.post(
        client._build_absolute_uri(f"/goods/control-list-entries/{data_standard_case['case']['id']}"), json={}
    )

    data = {
        "form-TOTAL_FORMS": 2,
        "form-INITIAL_FORMS": 0,
        "form-0-use_latest_precedent": True,
        "form-0-good_on_application_id": good_on_application_id_1,
        "form-0-latest_precedent_id": "6daad1c3-cf97-4aad-b711-d5c9a9f4586e",
        "form-1-use_latest_precedent": True,
        "form-1-good_on_application_id": good_on_application_id_2,
        "form-1-latest_precedent_id": "6daad1c3-cf97-4aad-b711-d5c9a9f4586e",
    }

    response = authorized_client.post(previous_assessments_url, data, follow=True)
    assert response.status_code == 200

    assert mocked_assessment_endpoint.request_history[-2].json()["objects"] == [good_on_application_id_1]
    assert mocked_assessment_endpoint.last_request.json()["objects"] == [good_on_application_id_2]

    messages = [str(msg) for msg in response.context["messages"]]
    expected_message = "Assessed 2 products using previous assessments."
    assert messages == [expected_message]
