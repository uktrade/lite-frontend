import pytest

from django.urls import reverse

from core import client


@pytest.fixture(autouse=True)
def setup(
    mock_case,
    mock_queue,
    mock_cases_search,
    mock_cases_search_head,
    mock_control_list_entries,
    mock_regime_entries,
    mock_countries,
    mock_queues_list,
    mock_empty_bookmarks,
):
    return


@pytest.fixture
def data_generated_document_id():
    return "2e0b4d2c-3a4b-4b00-8e5d-dac7fc285059"


@pytest.fixture
def send_document_url(data_standard_case, data_generated_document_id):
    case_id = data_standard_case["case"]["id"]
    return client._build_absolute_uri(f"/cases/{case_id}/generated-documents/{data_generated_document_id}/send/")


@pytest.fixture
def mock_send_generated_document(requests_mock, send_document_url, mock_gov_user):
    return requests_mock.post(url=send_document_url, json={"notification_sent": False})


def test_send_existing_document(
    authorized_client,
    requests_mock,
    data_standard_case,
    send_document_url,
    queue_pk,
    data_generated_document_id,
):
    mock_send_generated_document_api_error = requests_mock.post(url=send_document_url, json={}, status_code=404)
    url = reverse(
        "cases:generate_document_send",
        kwargs={
            "queue_pk": queue_pk,
            "pk": data_standard_case["case"]["id"],
            "document_pk": data_generated_document_id,
        },
    )
    response = authorized_client.post(url, follow=True)
    assert response.status_code == 200
    messages = [str(msg) for msg in response.context["messages"]]
    expected_message = f"An error occurred when sending the document. Please try again later"
    assert response.redirect_chain[-1][0] == f"/queues/{queue_pk}/"
    assert messages == [expected_message]
    assert mock_send_generated_document_api_error.called
    assert (
        mock_send_generated_document_api_error.last_request.path
        == f"/cases/{data_standard_case['case']['id']}/generated-documents/{data_generated_document_id}/send/"
    )
    assert mock_send_generated_document_api_error.last_request.json() == {}


def test_send_existing_document_ok(
    authorized_client,
    data_standard_case,
    queue_pk,
    mock_send_generated_document,
    data_generated_document_id,
):
    url = reverse(
        "cases:generate_document_send",
        kwargs={
            "queue_pk": queue_pk,
            "pk": data_standard_case["case"]["id"],
            "document_pk": data_generated_document_id,
        },
    )
    response = authorized_client.post(url, follow=True)
    assert response.status_code == 200
    messages = [str(msg) for msg in response.context["messages"]]
    expected_message = f"Document sent to {data_standard_case['case']['data']['organisation']['name']}, {data_standard_case['case']['reference_code']}"
    assert response.redirect_chain[-1][0] == f"/queues/{queue_pk}/"
    assert messages == [expected_message]
    assert mock_send_generated_document.called
    assert (
        mock_send_generated_document.last_request.path
        == f"/cases/{data_standard_case['case']['id']}/generated-documents/{data_generated_document_id}/send/"
    )
    assert mock_send_generated_document.last_request.json() == {}
