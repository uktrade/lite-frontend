import pytest
from django.core.files.storage import Storage
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse
from unittest.mock import patch

from core import client
from exporter.core.constants import (
    SetPartyFormSteps,
    PartyDocumentType,
    DOCUMENT_TYPE_PARAM_ENGLISH_TRANSLATION,
    DOCUMENT_TYPE_PARAM_COMPANY_LETTERHEAD,
)


@pytest.fixture
def mock_application(requests_mock, data_standard_case):
    url = client._build_absolute_uri(f'/applications/{data_standard_case["case"]["id"]}/')
    yield requests_mock.get(url=url, json={"id": data_standard_case["case"]["id"]})


@pytest.fixture
def mock_party_create(requests_mock, data_standard_case):
    party_id = data_standard_case["case"]["data"]["end_user"]["id"]
    url = client._build_absolute_uri(f'/applications/{data_standard_case["case"]["id"]}/parties/')
    yield requests_mock.post(url=url, status_code=201, json={"end_user": {"id": party_id}})


@pytest.fixture
def mock_party_get(requests_mock, data_standard_case):
    end_user = data_standard_case["case"]["data"]["end_user"]
    url = client._build_absolute_uri(f'/applications/{data_standard_case["case"]["id"]}/parties/{end_user["id"]}/')
    yield requests_mock.get(url=url, json={"data": end_user})


@pytest.fixture
def mock_party_put(requests_mock, data_standard_case):
    end_user = data_standard_case["case"]["data"]["end_user"]
    url = client._build_absolute_uri(f'/applications/{data_standard_case["case"]["id"]}/parties/{end_user["id"]}/')
    yield requests_mock.put(url=url, json={})


@pytest.fixture
def mock_post_party_document(requests_mock, data_standard_case):
    party_id = data_standard_case["case"]["data"]["end_user"]["id"]
    url = client._build_absolute_uri(f'/applications/{data_standard_case["case"]["id"]}/parties/{party_id}/document/')
    yield requests_mock.post(url=url, status_code=201, json={})


@pytest.fixture(autouse=True)
def setup(
    mock_countries, mock_application, mock_party_create, mock_party_get, mock_party_put, mock_post_party_document
):
    class NoOpStorage(Storage):
        def save(self, name, content, max_length=None):
            return name

        def open(self, name, mode="rb"):
            return None

        def delete(self, name):
            pass

    with patch("exporter.applications.views.parties.end_users.SetPartyView.file_storage", new=NoOpStorage()):
        yield


@pytest.fixture
def url(data_standard_case):
    return reverse("applications:set_end_user", kwargs={"pk": data_standard_case["case"]["id"]})


def test_set_end_user_view(url, authorized_client, requests_mock, data_standard_case):
    party_id = data_standard_case["case"]["data"]["end_user"]["id"]

    resp = set_end_user(url, authorized_client)

    assert resp.status_code == 302
    assert resp.url == reverse(
        "applications:end_user_summary", kwargs={"pk": data_standard_case["case"]["id"], "obj_pk": party_id}
    )

    letterhead_data = requests_mock.request_history.pop().json()
    assert letterhead_data == {
        "type": PartyDocumentType.END_USER_COMPANY_LETTERHEAD_DOCUMENT,
        "name": f'{letterhead_data["name"]}',
        "s3_key": f'{letterhead_data["s3_key"]}',
        "size": 0,
    }

    translation_data = requests_mock.request_history.pop().json()
    assert translation_data == {
        "type": PartyDocumentType.END_USER_ENGLISH_TRANSLATION_DOCUMENT,
        "name": f'{translation_data["name"]}',
        "s3_key": f'{translation_data["s3_key"]}',
        "size": 0,
    }

    undertaking_data = requests_mock.request_history.pop().json()
    assert undertaking_data == {
        "type": PartyDocumentType.END_USER_UNDERTAKING_DOCUMENT,
        "name": f'{undertaking_data["name"]}',
        "s3_key": f'{undertaking_data["s3_key"]}',
        "size": 0,
    }

    _ = requests_mock.request_history.pop().json()
    end_user_data = requests_mock.request_history.pop().json()
    assert end_user_data == {
        "sub_type": "government",
        "sub_type_other": "",
        "name": "test_name",
        "website": "https://www.example.com",
        "address": "1 somewhere",
        "country": "US",
        "signatory_name_euu": "test signatory",
        "end_user_document_available": "True",
        "end_user_document_missing_reason": "",
        "product_differences_note": "",
        "document_in_english": "False",
        "document_on_letterhead": "False",
        "type": "end_user",
    }


def set_end_user(url, authorized_client):
    current_step_key = "set_end_user_view-current_step"
    response = authorized_client.get(url)
    assert not response.context["form"].errors

    response = authorized_client.post(
        url,
        data={
            f"{current_step_key}": SetPartyFormSteps.PARTY_SUB_TYPE,
            f"{SetPartyFormSteps.PARTY_SUB_TYPE}-sub_type": "government",
        },
    )
    assert not response.context["form"].errors

    response = authorized_client.post(
        url,
        data={
            f"{current_step_key}": SetPartyFormSteps.PARTY_NAME,
            f"{SetPartyFormSteps.PARTY_NAME}-name": "test_name",
        },
    )
    assert not response.context["form"].errors

    response = authorized_client.post(
        url,
        data={
            f"{current_step_key}": SetPartyFormSteps.PARTY_WEBSITE,
            f"{SetPartyFormSteps.PARTY_WEBSITE}-website": "https://www.example.com",
        },
    )
    assert not response.context["form"].errors

    response = authorized_client.post(
        url,
        data={
            f"{current_step_key}": SetPartyFormSteps.PARTY_ADDRESS,
            f"{SetPartyFormSteps.PARTY_ADDRESS}-address": "1 somewhere",
            f"{SetPartyFormSteps.PARTY_ADDRESS}-country": "US",
        },
    )
    assert not response.context["form"].errors

    response = authorized_client.post(
        url,
        data={
            f"{current_step_key}": SetPartyFormSteps.PARTY_SIGNATORY_NAME,
            f"{SetPartyFormSteps.PARTY_SIGNATORY_NAME}-signatory_name_euu": "test signatory",
        },
    )
    assert not response.context["form"].errors

    response = authorized_client.post(
        url,
        data={
            f"{current_step_key}": SetPartyFormSteps.PARTY_DOCUMENTS,
            f"{SetPartyFormSteps.PARTY_DOCUMENTS}-end_user_document_available": "True",
        },
    )
    assert not response.context["form"].errors

    party_doc = SimpleUploadedFile("party.pdf", b"file_content", content_type="application/pdf")
    response = authorized_client.post(
        url,
        data={
            f"{current_step_key}": SetPartyFormSteps.PARTY_DOCUMENT_UPLOAD,
            f"{SetPartyFormSteps.PARTY_DOCUMENT_UPLOAD}-party_document": party_doc,
            f"{SetPartyFormSteps.PARTY_DOCUMENT_UPLOAD}-document_in_english": "False",
            f"{SetPartyFormSteps.PARTY_DOCUMENT_UPLOAD}-document_on_letterhead": "False",
        },
    )
    assert not response.context["form"].errors

    translation_doc = SimpleUploadedFile("translation.pdf", b"file_content", content_type="application/pdf")
    response = authorized_client.post(
        url,
        data={
            f"{current_step_key}": SetPartyFormSteps.PARTY_ENGLISH_TRANSLATION_UPLOAD,
            f"{SetPartyFormSteps.PARTY_ENGLISH_TRANSLATION_UPLOAD}-party_eng_translation_document": translation_doc,
        },
    )
    assert not response.context["form"].errors

    letterhead_doc = SimpleUploadedFile("letterhead.pdf", b"file_content", content_type="application/pdf")
    response = authorized_client.post(
        url,
        data={
            f"{current_step_key}": SetPartyFormSteps.PARTY_COMPANY_LETTERHEAD_DOCUMENT_UPLOAD,
            f"{SetPartyFormSteps.PARTY_COMPANY_LETTERHEAD_DOCUMENT_UPLOAD}-party_letterhead_document": letterhead_doc,
        },
    )

    return response


@pytest.mark.parametrize(
    "url_name, data, expected",
    (
        ("end_user_edit_sub_type", {"sub_type": "commercial"}, {"sub_type": "commercial", "sub_type_other": ""}),
        ("end_user_edit_name", {"name": "John Doe"}, {"name": "John Doe"}),
        ("end_user_edit_website", {"website": "http://www.example.com"}, {"website": "http://www.example.com"}),
        (
            "end_user_edit_address",
            {"address": "12345", "country": "IN"},
            {"address": "12345", "country": "IN"},
        ),
        ("end_user_edit_signatory", {"signatory_name_euu": "John Doe"}, {"signatory_name_euu": "John Doe"}),
        (
            "end_user_document_option",
            {
                "end_user_document_available": False,
                "end_user_document_missing_reason": "Products details not available as they are not manufactured yet",
            },
            {
                "end_user_document_available": "False",
                "end_user_document_missing_reason": "Products details not available as they are not manufactured yet",
            },
        ),
        (
            "end_user_document_option",
            {
                "end_user_document_available": True,
                "end_user_document_missing_reason": "",
            },
            {
                "end_user_document_available": "True",
                "end_user_document_missing_reason": "",
            },
        ),
    ),
)
def test_edit_end_user(requests_mock, authorized_client, data_standard_case, url_name, data, expected):
    application_id = data_standard_case["case"]["id"]
    end_user = data_standard_case["case"]["data"]["end_user"]

    party_edit_url = reverse(
        f"applications:{url_name}",
        kwargs={"pk": application_id, "obj_pk": end_user["id"]},
    )
    response = authorized_client.post(party_edit_url, data=data)
    assert response.status_code == 302

    if url_name == "end_user_document_option":
        _ = requests_mock.request_history.pop()

    actual = requests_mock.request_history.pop().json()
    assert actual == expected


@pytest.fixture
def end_user_documents():
    return {
        DOCUMENT_TYPE_PARAM_ENGLISH_TRANSLATION: {
            "party_eng_translation_document": SimpleUploadedFile(
                "english_translation.pdf", b"file_content", content_type="application/pdf"
            )
        },
        DOCUMENT_TYPE_PARAM_COMPANY_LETTERHEAD: {
            "party_letterhead_document": SimpleUploadedFile(
                "company_letterhead.pdf", b"file_content", content_type="application/pdf"
            )
        },
    }


@pytest.mark.parametrize(
    "document_type, expected",
    (
        (
            DOCUMENT_TYPE_PARAM_ENGLISH_TRANSLATION,
            {"type": PartyDocumentType.END_USER_ENGLISH_TRANSLATION_DOCUMENT, "size": 0},
        ),
        (
            DOCUMENT_TYPE_PARAM_COMPANY_LETTERHEAD,
            {"type": PartyDocumentType.END_USER_COMPANY_LETTERHEAD_DOCUMENT, "size": 0},
        ),
    ),
)
def test_edit_end_user_document(
    requests_mock, authorized_client, data_standard_case, end_user_documents, document_type, expected
):
    application_id = data_standard_case["case"]["id"]
    end_user = data_standard_case["case"]["data"]["end_user"]

    data = end_user_documents[document_type]
    party_document_edit_url = reverse(
        f"applications:end_user_edit_document",
        kwargs={"pk": application_id, "obj_pk": end_user["id"], "document_type": document_type},
    )
    response = authorized_client.post(party_document_edit_url, data=data)
    assert response.status_code == 302

    actual = requests_mock.request_history.pop().json()
    assert actual == {
        "type": expected["type"],
        "name": actual["name"],
        "s3_key": actual["s3_key"],
        "size": expected["size"],
    }
