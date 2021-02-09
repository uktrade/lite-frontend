from unittest import mock

from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse

from core import client


@mock.patch("exporter.organisation.views.UploadFirearmsCertificate.handle_s3_upload", mock.Mock)
def test_upload_firearm_registered_dealer_certificate(authorized_client, requests_mock):
    requests_mock.post(client._build_absolute_uri(f"/organisations/1/documents/"))

    url = reverse("organisation:upload-firearms-certificate")
    data = {
        "file": SimpleUploadedFile("file.txt", b"abc", content_type="text/plain"),
        "reference_code": "1234",
        "expiry_date_day": 1,
        "expiry_date_month": 1,
        "expiry_date_year": 3333,
    }

    response = authorized_client.post(url, data)

    assert response.status_code == 302
    assert response.url == reverse("organisation:details")
    assert requests_mock.request_history[0].json() == {
        "expiry_date": "3333-01-01",
        "document_type": "rfd-certificate",
        "reference_code": "1234",
        "document": {"name": "file.txt", "s3_key": mock.ANY, "size": 0,},
    }


@mock.patch("exporter.organisation.views.UploadSectionFiveCertificate.handle_s3_upload", mock.Mock)
def test_upload_firearm_section_five_certificate(authorized_client, requests_mock):
    requests_mock.post(client._build_absolute_uri(f"/organisations/1/documents/"))

    url = reverse("organisation:upload-section-five-certificate")
    data = {
        "file": SimpleUploadedFile("file.txt", b"abc", content_type="text/plain"),
        "reference_code": "1234",
        "expiry_date_day": 1,
        "expiry_date_month": 1,
        "expiry_date_year": 3333,
    }

    response = authorized_client.post(url, data)

    assert response.status_code == 302
    assert response.url == reverse("organisation:details")
    assert requests_mock.request_history[0].json() == {
        "expiry_date": "3333-01-01",
        "document_type": "section-five-certificate",
        "reference_code": "1234",
        "document": {"name": "file.txt", "s3_key": mock.ANY, "size": 0,},
    }


@mock.patch("exporter.organisation.views.s3_client")
def test_download_docoument_on_organisation(mock_s3_client_class, authorized_client, requests_mock, settings):
    mock_s3_client_class().generate_presigned_url.return_value = "/the/document/url"
    requests_mock.get(
        client._build_absolute_uri(f"/organisations/1/document/00acebbf-2077-4b80-8b95-37ff7f46c6d0/"),
        json={"document": {"s3_key": "123"}},
    )

    url = reverse("organisation:document", kwargs={"pk": "00acebbf-2077-4b80-8b95-37ff7f46c6d0"})

    response = authorized_client.get(url)

    assert response.status_code == 302
    assert response.url == "/the/document/url"

    assert mock_s3_client_class().generate_presigned_url.call_count == 1
    assert mock_s3_client_class().generate_presigned_url.call_args_list == [
        mock.call("get_object", Params={"Bucket": settings.AWS_STORAGE_BUCKET_NAME, "Key": "123"}, ExpiresIn=15)
    ]
