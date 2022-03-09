import uuid
from unittest.mock import patch

import pytest
from django.core.files.storage import Storage
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse

from exporter.core.constants import SetPartyFormSteps, PartyDocumentType


@pytest.fixture(autouse=True)
def setup():
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
    party_id = str(uuid.uuid4())
    requests_mock.post(
        f'/applications/{data_standard_case["case"]["id"]}/parties/',
        status_code=201,
        json={"end_user": {"id": party_id}},
    )
    requests_mock.post(
        f'/applications/{data_standard_case["case"]["id"]}/parties/{party_id}/document/', status_code=201, json={}
    )
    requests_mock.post(
        f'/applications/{data_standard_case["case"]["id"]}/parties/{party_id}/document/', status_code=201, json={}
    )
    requests_mock.post(
        f'/applications/{data_standard_case["case"]["id"]}/parties/{party_id}/document/', status_code=201, json={}
    )
    # The API request to retrieve the list of countries for the PartyAddressForm
    requests_mock.get("/static/countries/?exclude=GB", json={"countries": [{"id": "usa", "name": "USA"}]})

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

    end_user_data = requests_mock.request_history.pop().json()
    assert end_user_data == {
        "sub_type": "government",
        "sub_type_other": "",
        "name": "test_name",
        "website": "https://www.example.com",
        "address": "1 somewhere",
        "country": "usa",
        "signatory_name_euu": "test signatory",
        "end_user_document_available": "True",
        "end_user_document_missing_reason": "",
        "description": "",
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
            f"{SetPartyFormSteps.PARTY_ADDRESS}-country": "usa",
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
