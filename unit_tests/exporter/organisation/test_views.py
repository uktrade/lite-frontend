import pytest
from unittest import mock
from datetime import date

from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse

from core import client


def test_upload_firearm_registered_dealer_certificate(authorized_client, requests_mock):
    requests_mock.post(client._build_absolute_uri(f"/organisations/1/documents/"))

    url = reverse("organisation:upload-firearms-certificate")
    data = {
        "file": SimpleUploadedFile("file.txt", b"abc", content_type="text/plain"),
        "reference_code": "1234",
        "expiry_date_day": 1,
        "expiry_date_month": 1,
        "expiry_date_year": 2025,
    }

    response = authorized_client.post(url, data)

    assert response.status_code == 302
    assert response.url == reverse("organisation:details")
    assert requests_mock.request_history[0].json() == {
        "expiry_date": "2025-01-01",
        "document_type": "rfd-certificate",
        "reference_code": "1234",
        "document": {"name": "file.txt", "s3_key": mock.ANY, "size": 0,},
    }


@pytest.mark.parametrize(
    "expiry_date,error",
    (
        ("2020-01-01", ["Expiry date must be in the future"]),  # Past
        ("2050-01-01", ["Expiry date is too far in the future"]),  # Too far in the future
    ),
)
def test_upload_firearm_registered_dealer_certificate_error(authorized_client, expiry_date, error):
    url = reverse("organisation:upload-firearms-certificate")
    expiry_date = date.fromisoformat(expiry_date)
    data = {
        "file": SimpleUploadedFile("file.txt", b"abc", content_type="text/plain"),
        "reference_code": "1234",
        "expiry_date_day": expiry_date.day,
        "expiry_date_month": expiry_date.month,
        "expiry_date_year": expiry_date.year,
    }
    response = authorized_client.post(url, data)

    assert response.status_code == 200
    assert response.context["errors"]["expiry_date"] == error


def test_upload_firearm_section_five_certificate(authorized_client, requests_mock):
    requests_mock.post(client._build_absolute_uri(f"/organisations/1/documents/"))

    url = reverse("organisation:upload-section-five-certificate")
    data = {
        "file": SimpleUploadedFile("file.txt", b"abc", content_type="text/plain"),
        "reference_code": "1234",
        "expiry_date_day": 1,
        "expiry_date_month": 1,
        "expiry_date_year": 2025,
    }

    response = authorized_client.post(url, data)

    assert response.status_code == 302
    assert response.url == reverse("organisation:details")
    assert requests_mock.request_history[0].json() == {
        "expiry_date": "2025-01-01",
        "document_type": "section-five-certificate",
        "reference_code": "1234",
        "document": {"name": "file.txt", "s3_key": mock.ANY, "size": 0},
    }


@pytest.mark.parametrize(
    "expiry_date,error",
    (
        ("2020-01-01", ["Expiry date must be in the future"]),  # Past
        ("2050-01-01", ["Expiry date is too far in the future"]),  # Too far in the future
    ),
)
def test_upload_firearm_section_five_certificate_error(authorized_client, expiry_date, error):
    url = reverse("organisation:upload-section-five-certificate")
    expiry_date = date.fromisoformat(expiry_date)
    data = {
        "file": SimpleUploadedFile("file.txt", b"abc", content_type="text/plain"),
        "reference_code": "1234",
        "expiry_date_day": expiry_date.day,
        "expiry_date_month": expiry_date.month,
        "expiry_date_year": expiry_date.year,
    }
    response = authorized_client.post(url, data)

    assert response.status_code == 200
    assert response.context["errors"]["expiry_date"] == error


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
