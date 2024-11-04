import pytest
from bs4 import BeautifulSoup
from django.urls import reverse

from core import client


@pytest.fixture(autouse=True)
def setup(requests_mock, mock_queue, mock_standard_case, mock_party_denial_search_results):
    yield


@pytest.fixture
def data_generated_document_id():
    return "2e0b4d2c-3a4b-4b00-8e5d-dac7fc285059"


@pytest.fixture
def data_generated_paragraph_id():
    return "90e2056f-b4df-41cb-8454-009cac9a788e"


@pytest.fixture
def get_document_url(data_standard_case, data_generated_document_id):
    case_id = data_standard_case["case"]["id"]
    return client._build_absolute_uri(f"/cases/{case_id}/generated-documents/{data_generated_document_id}")


@pytest.fixture
def mock_get_document(requests_mock, get_document_url, data_generated_document_id, mock_gov_user):
    return requests_mock.get(
        url=get_document_url, json={"template": data_generated_document_id, "text": "This is my text"}
    )


@pytest.fixture
def url(data_standard_case):
    return reverse(
        "cases:select-inform-template",
        kwargs={"queue_pk": data_standard_case["case"]["id"], "pk": data_standard_case["case"]["id"]},
    )


@pytest.fixture
def mock_letter_templates_case(requests_mock, data_standard_case):
    case_id = data_standard_case["case"]["id"]
    url = client._build_absolute_uri(f"/letter-templates/?case={case_id}&page=1&decision=inform")
    return requests_mock.get(
        url=url, json={"results": [{"id": "a5896319-9761-423d-88d1-a601f9d2d6e9", "name": "Inform letter"}]}
    )


@pytest.fixture
def mock_letter_template_details(requests_mock):
    url = client._build_absolute_uri(f"/letter-templates/a5896319-9761-423d-88d1-a601f9d2d6e9/")
    return requests_mock.get(
        url=url,
        json=(
            {
                "paragraph_details": [
                    {"id": "90e2056f-b4df-41cb-8454-009cac9a788e", "name": "option 1", "text": "option 1 text "},
                    {"id": "c4427ea6-f47d-4a4f-8498-9319f2fafb21", "name": "option 2", "text": "option 2 text "},
                ],
            }
        ),
    )


@pytest.fixture
def mock_letter_templates_case(requests_mock, data_standard_case):
    case_id = data_standard_case["case"]["id"]
    url = client._build_absolute_uri(f"/letter-templates/?case={case_id}&page=1&decision=inform")
    return requests_mock.get(
        url=url, json={"results": [{"id": "a5896319-9761-423d-88d1-a601f9d2d6e9", "name": "Inform letter"}]}
    )


def test_select_template_paragraph(
    authorized_client,
    url,
    mock_letter_templates_case,
    mock_letter_template_details,
    mock_gov_user,
    data_standard_case,
):
    response = authorized_client.get(url)
    response.context_data["form"].fields["select_template"].choices == [
        ["90e2056f-b4df-41cb-8454-009cac9a788e", "option 1"],
        ["c4427ea6-f47d-4a4f-8498-9319f2fafb21", "option 2"],
    ]

    assert response.status_code == 200

    case_id = data_standard_case["case"]["id"]
    back_link_url = reverse("cases:consolidate_view", kwargs={"queue_pk": case_id, "pk": case_id})
    assert response.context["back_link_url"] == back_link_url


def test_select_template_paragraph_invalid_letter_type(
    data_standard_case,
    requests_mock,
    authorized_client,
    url,
    mock_letter_template_details,
    mock_gov_user,
):

    case_id = data_standard_case["case"]["id"]
    mock_url = client._build_absolute_uri(f"/letter-templates/?case={case_id}&page=1&decision=inform")
    requests_mock.get(
        url=mock_url, json={"results": [{"id": "a5896319-9761-423d-88d1-a601f9d2d6e9", "name": "NotAvailable"}]}
    )

    with pytest.raises(KeyError):
        response = authorized_client.get(url)


def test_select_template_paragraph_send_form(
    authorized_client,
    url,
    mock_letter_templates_case,
    mock_letter_template_details,
    mock_gov_user,
):
    response = authorized_client.post(url, data={"select_template": "90e2056f-b4df-41cb-8454-009cac9a788e"})

    assert response.status_code == 302
    # confirms redirect
    assert "select-edit-text/90e2056f-b4df-41cb-8454-009cac9a788e" in response.url


@pytest.mark.parametrize(
    "paragraph_id, expected_text",
    (
        ("90e2056f-b4df-41cb-8454-009cac9a788e", "option 1 text "),
        ("c4427ea6-f47d-4a4f-8498-9319f2fafb21", "option 2 text "),
    ),
)
def test_letter_inform_edit_get(
    paragraph_id,
    expected_text,
    authorized_client,
    data_standard_case,
    mock_letter_templates_case,
    mock_letter_template_details,
    mock_gov_user,
):
    case_id = data_standard_case["case"]["id"]
    response = authorized_client.get(
        reverse(
            "cases:select-edit-text",
            kwargs={"queue_pk": case_id, "pk": case_id, "paragraph_id": paragraph_id},
        )
    )
    assert response.status_code == 200
    assert response.context["form"].initial["text"] == expected_text
    assert response.context["back_link_url"] == f"/queues/{case_id}/cases/{case_id}/advice/consolidate/view-advice/"


@pytest.fixture
def letter_edit_post_url(data_standard_case, data_generated_document_id):
    case_id = data_standard_case["case"]["id"]
    return reverse(
        "cases:edit-letter-text",
        kwargs={"queue_pk": case_id, "pk": case_id, "dpk": data_generated_document_id, "decision_key": "inform"},
    )


def test_letter_edit_post(
    letter_edit_post_url,
    authorized_client,
    mock_letter_templates_case,
    mock_letter_template_details,
    mock_gov_user,
    requests_mock,
    data_standard_case,
    mock_get_document,
):

    case_id = data_standard_case["case"]["id"]
    template = "a5896319-9761-423d-88d1-a601f9d2d6e9"
    text = "option%201%20text"
    url = client._build_absolute_uri(
        f"/cases/{case_id}/generated-documents/preview/?pk={case_id}&template={template}&text={text}&addressee="
    )
    requests_mock.get(url=url, json={"preview": ""})
    data = {"text": "option 1 text "}
    response = authorized_client.post(letter_edit_post_url, data)
    soup = BeautifulSoup(response.content, "html.parser")
    assert "Generate document" in soup.find(class_="govuk-heading-l").text

    assert response.status_code == 200


def test_letter_edit_post_failure(
    letter_edit_post_url,
    authorized_client,
    mock_letter_templates_case,
    mock_letter_template_details,
    mock_gov_user,
    requests_mock,
    data_standard_case,
    mock_get_document,
):

    case_id = data_standard_case["case"]["id"]
    template = "a5896319-9761-423d-88d1-a601f9d2d6e9"
    text = "option%201%20text"
    url = client._build_absolute_uri(
        f"/cases/{case_id}/generated-documents/preview/?pk={case_id}&template={template}&text={text}&addressee="
    )
    requests_mock.get(url=url, status_code=400, json={"preview": ""})
    data = {"text": "option 1 text "}
    response = authorized_client.post(letter_edit_post_url, data)
    assert response.status_code == 200
    soup = BeautifulSoup(response.content, "html.parser")
    assert "Document generation is not available at this time" in soup.find(class_="govuk-body").text


@pytest.fixture
def inform_letter_edit_post_url(data_standard_case, data_generated_paragraph_id):
    case_id = data_standard_case["case"]["id"]
    return reverse(
        "cases:select-edit-text",
        kwargs={"queue_pk": case_id, "pk": case_id, "paragraph_id": data_generated_paragraph_id},
    )


def test_letter_inform_edit_post(
    inform_letter_edit_post_url,
    authorized_client,
    mock_letter_templates_case,
    mock_letter_template_details,
    mock_gov_user,
    requests_mock,
    data_standard_case,
    mock_get_document,
):
    case_id = data_standard_case["case"]["id"]
    template = "a5896319-9761-423d-88d1-a601f9d2d6e9"
    text = "option%201%20text"
    url = client._build_absolute_uri(
        f"/cases/{case_id}/generated-documents/preview/?pk={case_id}&template={template}&text={text}&addressee="
    )
    requests_mock.get(url=url, status_code=200, json={"preview": ""})
    data = {"text": "option 1 text "}
    response = authorized_client.post(inform_letter_edit_post_url, data)
    assert response.status_code == 200
    soup = BeautifulSoup(response.content, "html.parser")
    assert "Generate document" in soup.find(class_="govuk-heading-l").text


def test_letter_edit_inform_post_failure(
    inform_letter_edit_post_url,
    authorized_client,
    mock_letter_templates_case,
    mock_letter_template_details,
    mock_gov_user,
    requests_mock,
    data_standard_case,
    mock_get_document,
):

    case_id = data_standard_case["case"]["id"]
    template = "a5896319-9761-423d-88d1-a601f9d2d6e9"
    text = "option%201%20text"
    url = client._build_absolute_uri(
        f"/cases/{case_id}/generated-documents/preview/?pk={case_id}&template={template}&text={text}&addressee="
    )
    requests_mock.get(url=url, status_code=400, json={"preview": ""})
    data = {"text": "option 1 text "}
    response = authorized_client.post(inform_letter_edit_post_url, data)
    assert response.status_code == 200
    soup = BeautifulSoup(response.content, "html.parser")
    assert "Document generation is not available at this time" in soup.find(class_="govuk-body").text
