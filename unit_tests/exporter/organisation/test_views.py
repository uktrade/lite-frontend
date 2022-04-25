from unittest import mock
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


@mock.patch("exporter.organisation.views.s3_client")
def test_download_docoument_on_organisation(
    mock_s3_client_class, authorized_client, requests_mock, settings, organisation_pk
):
    mock_s3_client_class().generate_presigned_url.return_value = "/the/document/url"
    requests_mock.get(
        client._build_absolute_uri(f"/organisations/{organisation_pk}/document/00acebbf-2077-4b80-8b95-37ff7f46c6d0/"),
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


def test_new_site_form_view(authorized_client, mock_exporter_user_me):
    url = reverse("organisation:sites:new")
    response = authorized_client.get(url)
    assert response.status_code == 200
