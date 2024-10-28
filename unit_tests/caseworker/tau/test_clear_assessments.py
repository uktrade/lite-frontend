from django.urls import reverse
import pytest


@pytest.fixture(autouse=True)
def setup(mock_queue, mock_case):
    yield


@pytest.fixture
def url(data_queue, data_standard_case):
    return reverse(
        "cases:tau:clear_assessments",
        kwargs={
            "queue_pk": data_queue["id"],
            "pk": data_standard_case["case"]["id"],
        },
    )


def get_cells(soup, table_id):
    return [td.text for td in soup.find(id=table_id).find_all("td")]


def test_tau_clear_auth(authorized_client, url, mock_control_list_entries, mock_precedents_api):
    """GET edit should return 200 with an authorised client"""
    response = authorized_client.get(url)
    assert response.status_code == 200


def test_tau_clear_noauth(client, url):
    """GET edit should return 302 with an unauthorised client"""
    response = client.get(url)
    assert response.status_code == 302


def test_form(
    authorized_client,
    url,
    data_standard_case,
    requests_mock,
    mock_assessment_put,
    mock_control_list_entries,
    mock_precedents_api,
):
    """
    Tests the submission of a valid form only. More tests on the form itself are in test_forms.py
    """
    # Remove assessment from a good
    good = data_standard_case["case"]["data"]["goods"][0]
    good["is_good_controlled"] = None
    good["control_list_entries"] = []
    edit_good = data_standard_case["case"]["data"]["goods"][1]
    edit_good["control_list_entries"] = [{"rating": "ML1"}, {"rating": "ML1a"}]
    # Get the clear form
    response = authorized_client.get(url)
    assert response.status_code == 200
    # Post to clear assessments
    response = authorized_client.post(url)

    # Check response and API payload
    assert response.status_code == 302
    assert (
        response.url
        == "/queues/00000000-0000-0000-0000-000000000001/cases/8fb76bed-fd45-4293-95b8-eda9468aa254/tau/previous-assessments/"
    )
    assert mock_assessment_put.last_request.json() == [
        {
            "control_list_entries": [],
            "is_good_controlled": None,
            "report_summary": None,
            "report_summary_prefix": None,
            "report_summary_subject": None,
            "comment": None,
            "regime_entries": [],
            "is_ncsc_military_information_security": None,
            "id": "6daad1c3-cf97-4aad-b711-d5c9a9f4586e",
        }
    ]


def test_no_precedent_redirect_to_tau(
    authorized_client,
    url,
    data_standard_case,
    requests_mock,
    mock_assessment_put,
    mock_control_list_entries,
    mock_good_precedent_endpoint_empty,
):
    response = authorized_client.get(url)
    assert response.status_code == 200

    response = authorized_client.post(url)
    assert response.status_code == 302
    assert (
        response.url == "/queues/00000000-0000-0000-0000-000000000001/cases/8fb76bed-fd45-4293-95b8-eda9468aa254/tau/"
    )
