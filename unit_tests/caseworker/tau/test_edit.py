from bs4 import BeautifulSoup
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
import pytest
from http import HTTPStatus
from core import client


@pytest.fixture(autouse=True)
def setup(mock_queue, mock_case):
    yield


@pytest.fixture
def url(data_queue, data_standard_case):
    return reverse(
        "cases:tau:edit",
        kwargs={
            "queue_pk": data_queue["id"],
            "pk": data_standard_case["case"]["id"],
            "good_id": data_standard_case["case"]["data"]["goods"][1]["id"],
        },
    )


@pytest.fixture
def mock_cle_post(requests_mock, data_standard_case):
    yield requests_mock.post(
        client._build_absolute_uri(f"/goods/control-list-entries/{data_standard_case['case']['id']}"), json={}
    )


@pytest.fixture
def mock_internal_docs_matcher(requests_mock, data_standard_case):
    good_id = data_standard_case["case"]["data"]["goods"][1]["id"]
    internal_doc_url = client._build_absolute_uri(
        f"/goods/document_internal_good_on_application_detail/4955a24f-9142-47ad-9fc2-5f862a2f8df1/"
    )

    return {
        "POST": requests_mock.post(
            client._build_absolute_uri(f"/goods/document_internal_good_on_application/{good_id}/"),
            json={},
            status_code=HTTPStatus.CREATED,
        ),
        "GET": requests_mock.get(internal_doc_url, json={}),
        "DELETE": requests_mock.delete(internal_doc_url, json={}),
        "PUT": requests_mock.put(internal_doc_url, json={}),
    }


def get_cells(soup, table_id):
    return [td.text for td in soup.find(id=table_id).find_all("td")]


def test_tau_edit_auth(authorized_client, url, mock_control_list_entries, mock_precedents_api):
    """GET edit should return 200 with an authorised client"""
    response = authorized_client.get(url)
    assert response.status_code == 200


def test_tau_home_noauth(client, url):
    """GET edit should return 302 with an unauthorised client"""
    response = client.get(url)
    assert response.status_code == 302


def test_form(
    authorized_client,
    url,
    data_standard_case,
    requests_mock,
    mock_cle_post,
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
    # Get the edit form
    response = authorized_client.get(url)
    soup = BeautifulSoup(response.content, "html.parser")

    # Check if the form fields contain sane values
    edit_good = data_standard_case["case"]["data"]["goods"][1]
    # Check control list entries
    edit_good_cle = [cle["rating"] for cle in edit_good["control_list_entries"]]
    form_cle = [cle.attrs["value"] for cle in soup.find("form").find_all("option") if "selected" in cle.attrs]
    assert edit_good_cle == form_cle
    # Check report summary
    assert edit_good["report_summary"] == soup.find("form").find(id="report_summary").attrs["value"]
    # Check comments
    assert edit_good["comment"] == soup.find("form").find(id="id_comment").text.strip()

    # Post the form with changes to data and a new file
    response = authorized_client.post(
        url, data={"report_summary": "test", "does_not_have_control_list_entries": True, "comment": "test"}
    )

    # Check response and API payload
    assert response.status_code == 302
    assert requests_mock.last_request.json() == {
        "control_list_entries": [],
        "report_summary": "test",
        "comment": "test",
        "current_object": "6daad1c3-cf97-4aad-b711-d5c9a9f4586e",
        "objects": ["6a7fc61f-698b-46b6-9876-6ac0fddfb1a2"],
        "is_good_controlled": False,
        "is_wassenaar": False,
    }


def test_form_new_file(
    authorized_client,
    url,
    data_standard_case,
    requests_mock,
    mock_cle_post,
    mock_internal_docs_matcher,
    mock_precedents_api,
):

    evidence_file = SimpleUploadedFile("test.pdf", b"file_content", content_type="application/pdf")
    response = authorized_client.post(
        url,
        data={
            "report_summary": "test",
            "does_not_have_control_list_entries": True,
            "comment": "test",
            "evidence_file": evidence_file,
            "evidence_file_title": "new title",
        },
    )
    assert response.status_code == 302
    assert mock_internal_docs_matcher["POST"].last_request.json() == {
        "name": "test.pdf",
        "s3_key": mock_internal_docs_matcher["POST"].last_request.json()["s3_key"],
        "size": 0,
        "document_title": "new title",
    }


def test_form_new_edit_file(
    authorized_client,
    url,
    data_standard_case,
    requests_mock,
    mock_cle_post,
    mock_internal_docs_matcher,
    mock_precedents_api,
):

    evidence_file = SimpleUploadedFile("test.pdf", b"file_content", content_type="application/pdf")

    # upload a new file
    response = authorized_client.post(
        url,
        data={
            "report_summary": "test",
            "does_not_have_control_list_entries": True,
            "comment": "test",
            "evidence_file": evidence_file,
            "evidence_file_title": "new edit title",
        },
    )

    assert response.status_code == 302

    assert mock_internal_docs_matcher["POST"].last_request.json() == {
        "name": "test.pdf",
        "s3_key": mock_internal_docs_matcher["POST"].last_request.json()["s3_key"],
        "size": 0,
        "document_title": "new edit title",
    }

    # upload a replacement file
    edit_good = data_standard_case["case"]["data"]["goods"][1]

    edit_good["good_application_internal_documents"] = [
        {
            "id": "4955a24f-9142-47ad-9fc2-5f862a2f8df1",
            "name": "test.pdf",
            "s3_key": "test_123.jpg",
            "size": 0,
            "document_title": "new title",
        }
    ]

    evidence_file = SimpleUploadedFile("test_new.pdf", b"file_content", content_type="application/pdf")

    response = authorized_client.post(
        url,
        data={
            "report_summary": "test",
            "does_not_have_control_list_entries": True,
            "comment": "test",
            "evidence_file": evidence_file,
            "evidence_file_title": "new file replacement",
        },
    )

    assert response.status_code == 302
    assert mock_internal_docs_matcher["DELETE"].called_once
    assert mock_internal_docs_matcher["POST"].last_request.json() == {
        "name": "test_new.pdf",
        "s3_key": mock_internal_docs_matcher["POST"].last_request.json()["s3_key"],
        "size": 0,
        "document_title": "new file replacement",
    }
    # Now lets just edit the evidence file title

    response = authorized_client.post(
        url,
        data={
            "report_summary": "test",
            "does_not_have_control_list_entries": True,
            "comment": "test",
            "evidence_file_title": "new edit title 2",
        },
    )

    assert response.status_code == 302

    assert mock_internal_docs_matcher["PUT"].last_request.json() == {
        "document_title": "new edit title 2",
    }
