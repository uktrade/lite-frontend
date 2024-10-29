import pytest
from bs4 import BeautifulSoup
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
def data_generated_template_id():
    return "a5896319-9761-423d-88d1-a601f9d2d6e9"


@pytest.fixture
def send_document_url(data_standard_case, data_generated_document_id):
    case_id = data_standard_case["case"]["id"]
    return client._build_absolute_uri(f"/cases/{case_id}/generated-documents/{data_generated_document_id}/send/")


@pytest.fixture
def mock_send_generated_document(requests_mock, send_document_url, mock_gov_user):
    return requests_mock.post(
        url=send_document_url,
        json={"notification_sent": False, "document": {"template": "foobar123", "advice_type": None, "text": ""}},
    )


@pytest.fixture
def mock_send_generated_inform_letter(requests_mock, send_document_url, mock_gov_user):
    return requests_mock.post(
        url=send_document_url,
        json={"notification_sent": False, "document": {"template": "foobar123", "advice_type": "inform", "text": ""}},
    )


@pytest.fixture
def generated_document_create_url(data_standard_case):
    case_id = data_standard_case["case"]["id"]
    return client._build_absolute_uri(f"/cases/{case_id}/generated-documents/")


@pytest.fixture
def finalise_document_create_url(data_standard_case, data_generated_document_id, queue_pk):
    case_id = data_standard_case["case"]["id"]
    return reverse(
        "cases:finalise_document_create",
        kwargs={
            "queue_pk": queue_pk,
            "pk": data_standard_case["case"]["id"],
            "tpk": data_generated_document_id,
            "decision_key": "inform",
        },
    )


@pytest.fixture
def get_document_url(data_standard_case, data_generated_document_id):
    case_id = data_standard_case["case"]["id"]
    return client._build_absolute_uri(f"/cases/{case_id}/generated-documents/{data_generated_document_id}")


@pytest.fixture
def get_preview_url(data_standard_case, data_generated_document_id):
    case_id = data_standard_case["case"]["id"]
    text = "This is my text"
    return client._build_absolute_uri(
        f"/cases/{case_id}/generated-documents/preview/?pk={case_id}&template={data_generated_document_id}&text=This%20is%20my%20text&addressee="
    )


@pytest.fixture
def mock_get_document(requests_mock, get_document_url, data_generated_document_id, mock_gov_user):
    return requests_mock.get(
        url=get_document_url, json={"template": data_generated_document_id, "text": "This is my text"}
    )


@pytest.fixture
def mock_preview_document(requests_mock, get_preview_url, mock_gov_user):
    return requests_mock.get(url=get_preview_url, json={"preview": ""})


@pytest.fixture
def mock_preview_fail(requests_mock, get_preview_url, mock_gov_user):
    return requests_mock.get(url=get_preview_url, status_code=400, json={"preview": ""})


def test_send_existing_document_error(
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


def test_send_existing_inform_letter_ok(
    authorized_client,
    data_standard_case,
    queue_pk,
    mock_send_generated_inform_letter,
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
    expected_message = f"Inform letter sent to {data_standard_case['case']['data']['organisation']['name']}, {data_standard_case['case']['reference_code']}"
    assert response.redirect_chain[-1][0] == f"/queues/{queue_pk}/"
    assert messages == [expected_message]
    assert mock_send_generated_inform_letter.called
    assert (
        mock_send_generated_inform_letter.last_request.path
        == f"/cases/{data_standard_case['case']['id']}/generated-documents/{data_generated_document_id}/send/"
    )
    assert mock_send_generated_inform_letter.last_request.json() == {}


def test_finalise_document_create_return_url(
    authorized_client,
    data_standard_case,
    queue_pk,
    generated_document_create_url,
    finalise_document_create_url,
    requests_mock,
):

    mock_send_generated_document_create = requests_mock.post(
        url=generated_document_create_url, json={}, status_code=201
    )

    return_to_case_url = reverse("queues:cases", kwargs={"queue_pk": data_standard_case["case"]["id"]})
    response = authorized_client.post(finalise_document_create_url, data={"return_url": return_to_case_url})
    assert response.status_code == 302
    assert response.url == return_to_case_url


def test_finalise_document_create_error(
    authorized_client,
    generated_document_create_url,
    finalise_document_create_url,
    requests_mock,
):
    mock_send_generated_document_create = requests_mock.post(
        url=generated_document_create_url, json={}, status_code=200
    )

    response = authorized_client.post(finalise_document_create_url)
    assert response.status_code == 200
    assert response.context[0]["description"] == "Document generation is not available at this time"


def test_finalise_document_create(
    authorized_client,
    generated_document_create_url,
    finalise_document_create_url,
    queue_pk,
    requests_mock,
    data_standard_case,
):
    mock_send_generated_document_create = requests_mock.post(
        url=generated_document_create_url, json={}, status_code=201
    )

    pk = data_standard_case["case"]["id"]
    response = authorized_client.post(finalise_document_create_url)
    redirect_url = reverse("cases:finalise_documents", kwargs={"queue_pk": queue_pk, "pk": pk})
    assert response.status_code == 302
    assert response.url == redirect_url


@pytest.mark.parametrize(
    "document_data, expected",
    (
        (
            {"documents": {"refuse": {"value": "Refuse"}, "inform": {"value": "Inform"}}},
            {"refuse": {"value": "Refuse"}},
        ),
        (
            {"documents": {"refuse": {"value": "Refuse"}, "nla": {"value": "nla"}}},
            {"refuse": {"value": "Refuse"}, "nla": {"value": "nla"}},
        ),
    ),
)
def test_finalise_documents(
    document_data,
    expected,
    authorized_client,
    queue_pk,
    requests_mock,
    data_standard_case,
):
    pk = data_standard_case["case"]["id"]

    mock_send_generated_document_create = requests_mock.get(
        url=f"/cases/{pk}/final-advice-documents/", json=document_data
    )

    finalisation_document_url = reverse("cases:finalise_documents", kwargs={"queue_pk": queue_pk, "pk": pk})
    response = authorized_client.get(finalisation_document_url)

    assert response.status_code == 200
    assert response.context["decisions"] == expected


def test_preview_view(
    authorized_client,
    data_standard_case,
    queue_pk,
    mock_get_document,
    mock_preview_document,
    data_generated_document_id,
):
    url = reverse(
        "cases:generate_document_preview_view",
        kwargs={
            "queue_pk": queue_pk,
            "pk": data_standard_case["case"]["id"],
            "decision_key": "refuse",
            "dpk": data_generated_document_id,
        },
    )
    response = authorized_client.get(url, follow=True)
    assert response.status_code == 200
    soup = BeautifulSoup(response.content, "html.parser")
    assert "Generate document" in soup.find(class_="govuk-heading-l").text


def test_preview_view_failure(
    authorized_client,
    data_standard_case,
    queue_pk,
    mock_get_document,
    mock_preview_fail,
    data_generated_document_id,
):
    url = reverse(
        "cases:generate_document_preview_view",
        kwargs={
            "queue_pk": queue_pk,
            "pk": data_standard_case["case"]["id"],
            "decision_key": "refuse",
            "dpk": data_generated_document_id,
        },
    )
    response = authorized_client.get(url)
    assert response.status_code == 200
    soup = BeautifulSoup(response.content, "html.parser")
    assert "Document generation is not available at this time" in soup.find(class_="govuk-body").text
