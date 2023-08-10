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
        kwargs={"queue_pk": "566fd526-bd6d-40c1-94bd-60d10c967cf7", "pk": data_standard_case["case"]["id"]},
    )
@pytest.fixture
def paragraph_id():
    return uuid.uuid4()

@pytest.fixture
def mock_lettert_templates(requests_mock, data_standard_case, paragraph_id):
    case_id = data_standard_case["case"]["id"]
    url = client._build_absolute_uri(f"/letter-templates/?case={case_id}&page=1&decision=refuse")
    return requests_mock.get(url=url, json={"results": [{"id": str(paragraph_id)}]})

@pytest.fixture
def mock_lettert_template_details(requests_mock, paragraph_id):
    url = client._build_absolute_uri(f"/letter-templates/1234/")
    return requests_mock.get(url=url, json={"inform_letter_picklist": [{"id": paragraph_id, "name": "option1"}]})


def test_select_template_paragraph(
    authorized_client,
    url,
    mock_lettert_templates,
    mock_lettert_template_details,
    mock_gov_user,
):

    response = authorized_client.get(url)

    assert response.status_code == 200

def test_letter_edit(
    authorized_client,
    url,
    mock_lettert_templates,
    mock_lettert_template_details,
    mock_gov_user,
    paragraph_id,
    
):
    edit_letter_url = reverse(
        "cases:inform_edit_text",
        kwargs={"paragraph_id": str(paragraph_id)},
    )
    response = authorized_client.get(edit_letter_url)

    assert response.status_code == 200
