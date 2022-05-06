import datetime
import pytest
import uuid

from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse

from exporter.core.forms import CurrentFile
from exporter.core.helpers import decompose_date


@pytest.fixture(autouse=True)
def setup(mock_application_get, mock_good_get, mock_good_on_application_get):
    pass


@pytest.fixture(autouse=True)
def set_feature_flags(settings):
    settings.FEATURE_FLAG_ONLY_ALLOW_FIREARMS_PRODUCTS = True
    settings.FEATURE_FLAG_PRODUCT_2_0 = True


@pytest.fixture
def application(data_standard_case):
    return data_standard_case["case"]["data"]


@pytest.fixture
def section_one_document(good_on_application):
    return {
        "id": str(uuid.uuid4()),
        "name": "section_1_certificate.docx",
        "s3_key": "section_1_certificate.docx.s3_key",
        "safe": True,
        "document_type": "section-one-certificate",
        "good_on_application": good_on_application["id"],
    }


@pytest.fixture
def mock_section_one_document_get(requests_mock, section_one_document, application, good_id):
    url = f"/applications/{application['id']}/goods/{good_id}/documents/"
    return requests_mock.get(url, json={"documents": [section_one_document]})


@pytest.fixture
def edit_firearm_certificate_url(application, good_on_application):
    url = reverse(
        "applications:product_on_application_summary_edit_firearm_certificate",
        kwargs={
            "pk": application["id"],
            "good_on_application_pk": good_on_application["id"],
        },
    )
    return url


@pytest.fixture
def product_on_application_summary_url(application, good_on_application):
    url = reverse(
        "applications:product_on_application_summary",
        kwargs={
            "pk": application["id"],
            "good_on_application_pk": good_on_application["id"],
        },
    )
    return url


@pytest.fixture
def mock_good_on_application_put(requests_mock, good_on_application):
    url = f"/applications/good-on-application/{good_on_application['id']}/"
    return requests_mock.put(url, json={})


def test_edit_firearm_certificate_initial(
    authorized_client,
    application,
    good_id,
    section_one_document,
    mock_section_one_document_get,
    edit_firearm_certificate_url,
):
    response = authorized_client.get(edit_firearm_certificate_url)
    assert response.status_code == 200

    form = response.context["form"]
    initial = form.initial

    file = initial.pop("file")
    assert isinstance(file, CurrentFile)
    assert file.name == "section_1_certificate.docx"
    assert file.url == reverse(
        "applications:good-on-application-document",
        kwargs={
            "pk": application["id"],
            "good_pk": good_id,
            "doc_pk": section_one_document["id"],
        },
    )
    assert file.safe

    assert initial == {
        "section_certificate_date_of_expiry": datetime.date(2030, 12, 12),
        "section_certificate_missing": False,
        "section_certificate_missing_reason": "",
        "section_certificate_number": "12345",
    }


def test_edit_firearm_certificate_retaining_current_file(
    authorized_client,
    edit_firearm_certificate_url,
    product_on_application_summary_url,
    mock_section_one_document_get,
    mock_good_on_application_put,
):
    response = authorized_client.post(
        edit_firearm_certificate_url,
        data={
            "section_certificate_number": "67890",
            "section_certificate_missing": False,
            **decompose_date("section_certificate_date_of_expiry", datetime.date(2024, 1, 1)),
        },
    )

    assert response.status_code == 302
    assert response.url == product_on_application_summary_url

    assert mock_good_on_application_put.called_once
    assert mock_good_on_application_put.last_request.json() == {
        "firearm_details": {
            "section_certificate_date_of_expiry": "2024-01-01",
            "section_certificate_missing": False,
            "section_certificate_number": "67890",
        },
    }


def test_edit_firearm_certificate_retaining_upload_new_file(
    authorized_client,
    edit_firearm_certificate_url,
    product_on_application_summary_url,
    mock_section_one_document_get,
    mock_good_on_application_put,
    requests_mock,
    application,
    good_id,
    section_one_document,
    good_on_application,
):
    delete_good_on_application_matcher = requests_mock.delete(
        f"/applications/{application['id']}/goods/{good_id}/documents/{section_one_document['id']}/",
        json={},
    )

    post_good_on_application_document_matcher = requests_mock.post(
        f"/applications/{application['id']}/goods/{good_id}/documents/",
        status_code=201,
        json={},
    )

    post_application_document_matcher = requests_mock.post(
        f"/applications/{application['id']}/documents/",
        status_code=201,
        json={},
    )

    get_additional_documents_matcher = requests_mock.get(
        f"/applications/{application['id']}/documents/",
        status_code=200,
        json={
            "documents": [section_one_document],
        },
    )

    delete_additional_documents_matcher = requests_mock.delete(
        f"/applications/{application['id']}/documents/{section_one_document['id']}/",
        status_code=204,
        json={},
    )

    response = authorized_client.post(
        edit_firearm_certificate_url,
        data={
            "file": SimpleUploadedFile("firearm_certificate.pdf", b"This is the firearm certificate"),
            "section_certificate_number": "67890",
            "section_certificate_missing": False,
            **decompose_date("section_certificate_date_of_expiry", datetime.date(2024, 1, 1)),
        },
    )

    assert response.status_code == 302
    assert response.url == product_on_application_summary_url

    assert mock_good_on_application_put.called_once
    assert mock_good_on_application_put.last_request.json() == {
        "firearm_details": {
            "section_certificate_date_of_expiry": "2024-01-01",
            "section_certificate_missing": False,
            "section_certificate_number": "67890",
        },
    }

    assert delete_good_on_application_matcher.called_once

    assert get_additional_documents_matcher.called_once
    assert delete_additional_documents_matcher.called_once

    assert post_good_on_application_document_matcher.called_once
    assert post_good_on_application_document_matcher.last_request.json() == {
        "document_type": "section-one-certificate",
        "good_on_application": good_on_application["id"],
        "name": "firearm_certificate.pdf",
        "s3_key": "firearm_certificate.pdf",
        "size": 0,
    }

    assert post_application_document_matcher.called_once
    assert post_application_document_matcher.last_request.json() == {
        "description": "Firearm certificate for 'p1'",
        "document_type": "section-one-certificate",
        "name": "firearm_certificate.pdf",
        "s3_key": "firearm_certificate.pdf",
        "size": 0,
    }
