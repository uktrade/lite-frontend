import pytest
from django.urls import reverse
from core import client
from uuid import uuid4
from bs4 import BeautifulSoup


@pytest.fixture(autouse=True)
def setup(requests_mock, mock_queue, mock_standard_case, mock_party_denial_search_results):
    yield


@pytest.mark.parametrize(("decision_key"), [("approve"), ("reject")])
def test_generate_decision_document_on_finalise_case(
    authorized_client,
    requests_mock,
    data_queue,
    data_standard_case,
    decision_key,
):
    # arrange: make sure the if statement is tested
    queue_id = data_queue["id"]
    case_id = data_standard_case["case"]["id"]
    document_template_id = str(uuid4())

    requests_mock.get(client._build_absolute_uri(f"/cases/{case_id}/additional-contacts/"), json=data_standard_case)
    requests_mock.get(client._build_absolute_uri(f"/cases/{case_id}/applicant/"), json=data_standard_case)
    requests_mock.get(
        client._build_absolute_uri(f"/letter-templates/?case={case_id}&page=1&decision={decision_key}"),
        json={
            "total_pages": 1,
            "results": [{"id": document_template_id, "name": "name", "layout": {"filename": "filename"}}],
        },
        complete_qs=True,
    )

    url = reverse(
        "cases:finalise_document_template",
        kwargs={"queue_pk": queue_id, "pk": case_id, "decision_key": decision_key},
    )

    response = authorized_client.get(url)

    soup = BeautifulSoup(response.content)

    assert response.status_code == 200

    # test back url
    assert soup.find(id="back-link").get("href") == f"/queues/{queue_id}/cases/{case_id}/finalise/generate-documents/"
    # test button name is Preview
    assert soup.find(id="button-Preview").text.strip() == "Preview"
    # test the post url on the form is as expected
    assert (
        soup.find("form").get("action")
        == f"/queues/{queue_id}/cases/{case_id}/finalise/{decision_key}/generate-document/{document_template_id}/preview/"
    )
