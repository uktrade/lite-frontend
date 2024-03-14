import io
import uuid

from bs4 import BeautifulSoup
from unittest import mock

from django.http import StreamingHttpResponse
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile

from core import client
from unit_tests.helpers import mocked_now


@mock.patch("django.utils.timezone.now", side_effect=mocked_now)
def test_upload_firearm_registered_dealer_certificate(
    mock_timezone, authorized_client, mock_organisation_document_post
):
    url = reverse("organisation:upload-firearms-certificate")
    data = {
        "expiry_date_0": 1,  # day
        "expiry_date_1": 1,  # month
        "expiry_date_2": 2022,  # year
        "reference_code": "1234",
        "file": SimpleUploadedFile("file.txt", b"abc", content_type="text/plain"),
    }

    response = authorized_client.post(url, data)

    assert response.status_code == 302
    assert response.url == reverse("organisation:details")


@mock.patch("django.utils.timezone.now", side_effect=mocked_now)
def test_upload_section_five_certificate(mock_timezone, authorized_client, mock_organisation_document_post):
    url = reverse("organisation:upload-section-five-certificate")
    data = {
        "expiry_date_0": 1,  # day
        "expiry_date_1": 1,  # month
        "expiry_date_2": 2022,  # year
        "reference_code": "1234",
        "file": SimpleUploadedFile("file.txt", b"abc", content_type="text/plain"),
    }

    response = authorized_client.post(url, data)

    assert response.status_code == 302
    assert response.url == reverse("organisation:details")


def test_download_document_on_organisation(
    authorized_client,
    requests_mock,
    organisation_pk,
):
    requests_mock.get(
        client._build_absolute_uri(f"/organisations/{organisation_pk}/document/00acebbf-2077-4b80-8b95-37ff7f46c6d0/"),
        json={
            "id": "00acebbf-2077-4b80-8b95-37ff7f46c6d0",
            "document": {"id": str(uuid.uuid4()), "s3_key": "123", "name": "fakefile.doc"},
        },
    )
    requests_mock.get(
        client._build_absolute_uri(
            f"/organisations/{organisation_pk}/document/00acebbf-2077-4b80-8b95-37ff7f46c6d0/stream/"
        ),
        body=io.BytesIO(b"test"),
        headers={
            "Content-Type": "application/doc",
            "Content-Disposition": 'attachment; filename="fakefile.doc"',
        },
    )

    url = reverse("organisation:document", kwargs={"pk": "00acebbf-2077-4b80-8b95-37ff7f46c6d0"})

    response = authorized_client.get(url)
    assert response.status_code == 200
    assert isinstance(response, StreamingHttpResponse)
    assert response.headers["Content-Type"] == "application/doc"
    assert response.headers["Content-Disposition"] == 'attachment; filename="fakefile.doc"'
    assert b"".join(response.streaming_content) == b"test"


def test_new_site_form_view(authorized_client, mock_exporter_user_me):
    url = reverse("organisation:sites:new")
    response = authorized_client.get(url)
    assert response.status_code == 200


def test_upload_firearms_certificate_form_view_html_title(authorized_client):
    url = reverse("organisation:upload-firearms-certificate")
    response = authorized_client.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    assert soup.title.string.strip() == "Attach your registered firearms dealer certificate - LITE - GOV.UK"


def test_upload_section_five_certificate_form_view_html_title(authorized_client):
    url = reverse("organisation:upload-section-five-certificate")
    response = authorized_client.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    assert soup.title.string.strip() == "Attach your section five certificate - LITE - GOV.UK"
