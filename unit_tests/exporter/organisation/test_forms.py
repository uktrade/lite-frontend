import pytest
from unittest import mock
from django.core.files.uploadedfile import SimpleUploadedFile

from exporter.organisation import forms

from unit_tests.helpers import mocked_now


@mock.patch("django.utils.timezone.now", side_effect=mocked_now)
def test_upload_firearm_registered_dealer_certificate_form(mock_timezone, requests_mock):
    data = {
        "expiry_date_0": 1,  # day
        "expiry_date_1": 1,  # month
        "expiry_date_2": 2022,  # year
        "reference_code": "1234",
    }

    file = {
        "file": SimpleUploadedFile("file.txt", b"abc", content_type="text/plain"),
    }

    form = forms.UploadFirearmsCertificateForm(data, file)
    assert form.is_valid()


@mock.patch("django.utils.timezone.now", side_effect=mocked_now)
def test_upload_section_five_certificate_form(mock_timezone, requests_mock):
    data = {
        "expiry_date_0": 1,  # day
        "expiry_date_1": 1,  # month
        "expiry_date_2": 2022,  # year
        "reference_code": "1234",
    }

    file = {
        "file": SimpleUploadedFile("file.txt", b"abc", content_type="text/plain"),
    }

    form = forms.UploadSectionFiveCertificateForm(data, file)
    assert form.is_valid()


@mock.patch("django.utils.timezone.now", side_effect=mocked_now)
@pytest.mark.parametrize(
    "expiry_date,error",
    (
        ({"expiry_date_0": 1, "expiry_date_1": 1, "expiry_date_2": 2010,}, ["Expiry date must be in the future"],),
        ({"expiry_date_0": 1, "expiry_date_1": 1, "expiry_date_2": 2030,}, ["Expiry date is too far in the future"],),
    ),
)
def test_upload_firearm_registered_dealer_certificate_error(mock_timezone, authorized_client, expiry_date, error):
    data = {
        "file": SimpleUploadedFile("file.txt", b"abc", content_type="text/plain"),
        "reference_code": "1234",
        **expiry_date,
    }
    file = {
        "file": SimpleUploadedFile("file.txt", b"abc", content_type="text/plain"),
    }
    form = forms.UploadFirearmsCertificateForm(data, file)

    assert not form.is_valid()
    assert form.errors["expiry_date"] == error


@mock.patch("django.utils.timezone.now", side_effect=mocked_now)
@pytest.mark.parametrize(
    "expiry_date,error",
    (
        ({"expiry_date_0": 1, "expiry_date_1": 1, "expiry_date_2": 2010,}, ["Expiry date must be in the future"],),
        ({"expiry_date_0": 1, "expiry_date_1": 1, "expiry_date_2": 2030,}, ["Expiry date is too far in the future"],),
    ),
)
def test_upload_section_five_certificate_error(mock_timezone, authorized_client, expiry_date, error):
    data = {
        "file": SimpleUploadedFile("file.txt", b"abc", content_type="text/plain"),
        "reference_code": "1234",
        **expiry_date,
    }
    file = {
        "file": SimpleUploadedFile("file.txt", b"abc", content_type="text/plain"),
    }
    form = forms.UploadSectionFiveCertificateForm(data, file)

    assert not form.is_valid()
    assert form.errors["expiry_date"] == error
