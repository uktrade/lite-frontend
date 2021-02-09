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
