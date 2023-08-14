import pytest
from bs4 import BeautifulSoup
from django.urls import reverse

from core import client
import uuid


@pytest.fixture(autouse=True)
def setup(requests_mock, mock_queue, mock_standard_case, mock_party_denial_search_results):
    yield


@pytest.fixture
def paragraph_id():
    return uuid.uuid4()


@pytest.fixture
def url(data_standard_case):
    return reverse(
        "cases:finalisation_letters_select_inform_template",
        kwargs={"queue_pk": data_standard_case["case"]["id"], "pk": data_standard_case["case"]["id"]},
    )


@pytest.fixture
def letter_edit_url(data_standard_case, paragraph_id):
    case_id = data_standard_case["case"]["id"]

    return reverse(
        "cases:inform_edit_text",
        kwargs={"queue_pk": case_id, "pk": case_id, "paragraph_id": paragraph_id},
    )


@pytest.fixture
def mock_letter_templates_case(requests_mock, data_standard_case, paragraph_id):
    case_id = data_standard_case["case"]["id"]
    url = client._build_absolute_uri(f"/letter-templates/?case={case_id}&page=1&decision=refuse")
    return requests_mock.get(
        url=url, json={"results": [{"id": "a5896319-9761-423d-88d1-a601f9d2d6e9", "name": "Inform letter"}]}
    )


@pytest.fixture
def mock_letter_template_details(requests_mock, paragraph_id):
    url = client._build_absolute_uri(f"/letter-templates/a5896319-9761-423d-88d1-a601f9d2d6e9/")
    return requests_mock.get(
        url=url,
        json=(
            {
                "template": {
                    "id": "a5896319-9761-423d-88d1-a601f9d2d6e9",
                    "name": "Inform letter",
                    "paragraph_details": [
                        {"id": "90e2056f-b4df-41cb-8454-009cac9a788e", "name": "option 1", "text": "option 1 text "},
                        {"id": "c4427ea6-f47d-4a4f-8498-9319f2fafb21", "name": "option 2", "text": "option 2 text "},
                    ],
                }
            }
        ),
    )


def test_select_template_paragraph(
    authorized_client,
    url,
    mock_letter_templates_case,
    mock_letter_template_details,
    mock_gov_user,
):

    response = authorized_client.get(url)
    response.context_data['form'].fields['select_template'].choices == [['90e2056f-b4df-41cb-8454-009cac9a788e', 'option 1'], ['c4427ea6-f47d-4a4f-8498-9319f2fafb21', 'option 2']]
     
    assert response.status_code == 200

def test_select_template_paragraph_send_form(
    authorized_client,
    url,
    mock_letter_templates_case,
    mock_letter_template_details,
    mock_gov_user,
):

    response = authorized_client.post(url, data = {})

    assert response.status_code == 200

def test_letter_edit(
    authorized_client,
    letter_edit_url,
    mock_letter_templates_case,
    mock_letter_template_details,
    mock_gov_user,
    paragraph_id,
):

    response = authorized_client.get(letter_edit_url)

    assert response.status_code == 200
