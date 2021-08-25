import pytest
import requests
from unittest import mock
from django.core.files.uploadedfile import SimpleUploadedFile

from exporter.organisation import forms
from exporter.organisation.sites import forms as site_forms

from unit_tests.helpers import mocked_now
from core import client


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


@pytest.fixture
def mock_request(rf, authorized_client):
    request = rf.get("/")
    request.session = authorized_client.session
    request.requests_session = requests.Session()
    yield request


@pytest.fixture()
def mock_post_site(requests_mock, organisation_pk):
    url = client._build_absolute_uri(f"/organisations/{organisation_pk}/sites/")
    yield requests_mock.post(url=url, json={})


@pytest.fixture()
def mock_validate_site(requests_mock, organisation_pk):
    url = client._build_absolute_uri(f"/organisations/{organisation_pk}/sites/")
    yield requests_mock.post(url=url, json={})


def test_new_site_form_location(mock_request, mock_exporter_user_me, mock_post_site):
    data = {
        "location": "united_kingdom",
    }
    expected = {
        "location": "united_kingdom",
    }
    form = site_forms.NewSiteLocationForm(data=data, request=mock_request)
    assert form.is_valid()
    assert form.serialized_data == expected


def test_new_site_form_uk_address(mock_request, mock_exporter_user_me, mock_post_site):
    data = {
        "location": "united_kingdom",
        "name": "Test site",
        "phone_number": "+4401234567",
        "website": "https://example.com",
        "address": "",
        "address_line_1": "HQ building",
        "address_line_2": "1 Test street",
        "city": "London",
        "region": "Greater London",
        "postcode": "SW1 6FG",
        "country": "GB",
    }
    expected = {
        "name": "Test site",
        "phone_number": "+4401234567",
        "website": "https://example.com",
        "address": {
            "address_line_1": "HQ building",
            "address_line_2": "1 Test street",
            "city": "London",
            "postcode": "SW1 6FG",
            "region": "Greater London",
        },
    }
    form = site_forms.NewSiteUKAddressForm(data=data, request=mock_request)
    assert form.is_valid()
    assert form.serialized_data == expected


@pytest.mark.parametrize(
    "api_errors,form_errors",
    [
        ({"name": ["Enter the site name"]}, {"name": ["Enter the site name"]},),
        ({"address": {"address_line_1": ["Enter the address"]}}, {"address_line_1": ["Enter the address"]},),
    ],
)
def test_new_site_form_uk_address_errors(
    api_errors, form_errors, mock_request, requests_mock, mock_exporter_user_me, organisation_pk
):
    data = {
        "location": "united_kingdom",
        "name": "",
        "phone_number": "+4401234567",
        "website": "https://example.com",
        "address": "",
        "address_line_1": "HQ building",
        "address_line_2": "1 Test street",
        "city": "London",
        "region": "Greater London",
        "postcode": "SW1 6FG",
        "country": "GB",
    }
    form = site_forms.NewSiteUKAddressForm(data=data, request=mock_request)
    url = client._build_absolute_uri(f"/organisations/{organisation_pk}/sites/")
    requests_mock.post(url=url, json={"errors": api_errors})
    assert not form.is_valid()
    assert form.errors == form_errors


def test_new_site_form_overseas_address(mock_request, mock_exporter_user_me, mock_post_site, mock_get_countries):
    data = {
        "location": "abroad",
        "name": "Test site",
        "phone_number": "+4401234567",
        "website": "https://example.com",
        "address": "HQ,\nTest Street\nTest city\nSome postcode",
        "address_line_1": "",
        "address_line_2": "",
        "city": "",
        "region": "",
        "postcode": "",
        "country": "FR",
    }
    expected = {
        "name": "Test site",
        "phone_number": "+4401234567",
        "website": "https://example.com",
        "address": {"address": "HQ,\nTest Street\nTest city\nSome postcode", "country": "FR",},
    }
    form = site_forms.NewSiteInternationalAddressForm(data=data, request=mock_request)
    assert form.is_valid()
    assert form.serialized_data == expected
