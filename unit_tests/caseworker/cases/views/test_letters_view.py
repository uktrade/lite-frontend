import pytest
from bs4 import BeautifulSoup
from django.urls import reverse

from core import client
import uuid


@pytest.fixture(autouse=True)
def setup(requests_mock, mock_queue, mock_standard_case, mock_party_denial_search_results):
    yield


@pytest.fixture
def url(data_standard_case):
    return reverse(
        "cases:finalisation_letters_select_inform_template",
        kwargs={"queue_pk": data_standard_case["case"]["id"], "pk": data_standard_case["case"]["id"]},
    )


@pytest.fixture
def mock_letter_templates_case(requests_mock, data_standard_case):
    case_id = data_standard_case["case"]["id"]
    url = client._build_absolute_uri(f"/letter-templates/?case={case_id}&page=1&decision=refuse")
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
    url = client._build_absolute_uri(f"/letter-templates/?case={case_id}&page=1&decision=refuse")
    return requests_mock.get(
        url=url, json={"results": [{"id": "a5896319-9761-423d-88d1-a601f9d2d6e9", "name": "Inform letter"}]}
    )


def test_select_template_paragraph(
    authorized_client,
    url,
    mock_letter_templates_case,
    mock_letter_template_details,
    mock_gov_user,
):
    response = authorized_client.get(url)
    response.context_data["form"].fields["select_template"].choices == [
        ["90e2056f-b4df-41cb-8454-009cac9a788e", "option 1"],
        ["c4427ea6-f47d-4a4f-8498-9319f2fafb21", "option 2"],
    ]

    assert response.status_code == 200


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
def test_letter_edit_get(
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
            "cases:inform_edit_text",
            kwargs={"queue_pk": case_id, "pk": case_id, "paragraph_id": paragraph_id},
        )
    )
    assert response.status_code == 200
    assert response.context["form"].fields["text"].initial == expected_text


@pytest.fixture
def letter_edit_post_url(data_standard_case):
    case_id = data_standard_case["case"]["id"]
    return reverse(
        "cases:inform_edit_text",
        kwargs={"queue_pk": case_id, "pk": case_id, "paragraph_id": "90e2056f-b4df-41cb-8454-009cac9a788e"},
    )


def test_letter_edit_post(
    letter_edit_post_url,
    authorized_client,
    mock_letter_templates_case,
    mock_letter_template_details,
    mock_gov_user,
    requests_mock,
    data_standard_case,
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
