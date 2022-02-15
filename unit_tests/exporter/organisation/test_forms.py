import pytest
import requests
from unittest import mock
from django.core.files.uploadedfile import SimpleUploadedFile

from exporter.organisation import forms
from exporter.organisation.sites import forms as site_forms

from unit_tests.helpers import mocked_now
from unittest.mock import MagicMock

import django
from django.template import Context
from django.urls import reverse

from exporter.organisation.sites import views
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
        (
            {
                "expiry_date_0": 1,
                "expiry_date_1": 1,
                "expiry_date_2": 2010,
            },
            ["Expiry date must be in the future"],
        ),
        (
            {
                "expiry_date_0": 1,
                "expiry_date_1": 1,
                "expiry_date_2": 2030,
            },
            ["Expiry date is too far in the future"],
        ),
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
        (
            {
                "expiry_date_0": 1,
                "expiry_date_1": 1,
                "expiry_date_2": 2010,
            },
            ["Expiry date must be in the future"],
        ),
        (
            {
                "expiry_date_0": 1,
                "expiry_date_1": 1,
                "expiry_date_2": 2030,
            },
            ["Expiry date is too far in the future"],
        ),
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
    yield requests_mock.post(
        url=url, json={"site": {"name": "Test site", "id": "00000000-0000-0000-0000-000000000001"}}
    )


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
        (
            {"name": ["Enter the site name"]},
            {"name": ["Enter the site name"]},
        ),
        (
            {"address": {"address_line_1": ["Enter the address"]}},
            {"address_line_1": ["Enter the address"]},
        ),
        ({"name": ["Enter the site name"], "address": ["This field is required"]}, {"name": ["Enter the site name"]}),
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
        "address": {
            "address": "HQ,\nTest Street\nTest city\nSome postcode",
            "country": "FR",
        },
    }
    form = site_forms.NewSiteInternationalAddressForm(data=data, request=mock_request)
    assert form.is_valid()
    assert form.serialized_data == expected


def test_new_site_form_existing_sites(
    mock_request, mock_exporter_user_me, requests_mock, mock_post_site, organisation_pk
):
    data = {"are_you_sure": "True"}
    postcode = "SW1 7ES"
    url = f"/organisations/{organisation_pk}/sites/?exclude=&get_total_users=False&postcode=SW1+7ES"
    json = {
        "sites": [
            {"name": "Site 1"},
            {"name": "Site 2"},
        ]
    }
    requests_mock.get(client._build_absolute_uri(url), json=json)
    form = site_forms.NewSiteConfirmForm(data=data, request=mock_request, postcode=postcode)
    assert form.is_valid()
    context = {"back_link_url": reverse("organisation:sites:sites")}
    html = form.helper.render_layout(form, Context(context))
    for site in json["sites"]:
        assert site["name"] in html


def test_new_site_form_assign_users(
    mock_request, mock_exporter_user_me, requests_mock, mock_post_site, organisation_pk
):
    data = {"users": ["some-user-id", "another-user-id"]}
    json = [
        {
            "email": "john.smith@example.com",
            "id": "some-user-id",
            "first_name": "John",
            "last_name": "Smith",
        },
        {
            "email": "jane.doe@example.com",
            "id": "another-user-id",
            "first_name": "Jane",
            "last_name": "Doe",
        },
    ]
    url = f"/organisations/{organisation_pk}/users/?disable_pagination=True&exclude_permission=ADMINISTER_SITES"
    requests_mock.get(client._build_absolute_uri(url), json=json)
    form = site_forms.NewSiteAssignUsersForm(data=data, request=mock_request)
    assert form.is_valid()
    context = {"back_link_url": reverse("organisation:sites:sites")}
    html = form.helper.render_layout(form, Context(context))
    for user in json:
        assert user["first_name"] in html
        assert user["last_name"] in html


@pytest.mark.parametrize(
    "func,return_value,exp",
    [
        (views.show_domestic_site_form, {"location": "abroad"}, False),
        (views.show_domestic_site_form, {"location": "united_kingdom"}, True),
        (views.show_international_site_form, {"location": "united_kingdom"}, False),
        (views.show_international_site_form, {"location": "abroad"}, True),
        (views.show_add_site_confirmation_form, {"postcode": "SW1 7ES"}, True),
        (views.show_add_site_confirmation_form, {"postcode": None}, False),
    ],
)
def test_new_site_form_conditionals(func, return_value, exp, mock_request, requests_mock, organisation_pk):
    url = f"/organisations/{organisation_pk}/sites/?exclude=&get_total_users=False&postcode=SW1+7ES"
    json = {
        "sites": [
            {"name": "Site 1"},
            {"name": "Site 2"},
        ]
    }
    requests_mock.get(client._build_absolute_uri(url), json=json)
    wizard = views.NewSiteWizardView(request=mock_request)
    wizard.get_cleaned_data_for_step = MagicMock(return_value=return_value)
    assert func(wizard) == exp


class DummyForm(django.forms.Form):
    choice = django.forms.CharField()


def test_new_site_form_combine_form_data(mock_request, requests_mock, mock_post_site, organisation_pk):
    wizard = views.NewSiteWizardView(request=mock_request)

    form1 = DummyForm(data={"choice": "foo"})
    form1.serialized_data = MagicMock(return_value={"choice": "foo"})

    mock_form_list = [form1]
    response = wizard.done(mock_form_list)
    history = requests_mock.request_history
    url = client._build_absolute_uri(f"/organisations/{organisation_pk}/sites/")

    assert history[0].method == "POST"
    assert history[0].url == url
    assert response.url == reverse("organisation:sites:site", kwargs={"pk": "00000000-0000-0000-0000-000000000001"})


def test_new_site_form_redirect_if_not_confirm(mock_request, requests_mock, mock_post_site, organisation_pk):
    data = {"are_you_sure": "False"}
    postcode = "SW1 7ES"
    url = f"/organisations/{organisation_pk}/sites/?exclude=&get_total_users=False&postcode=SW1+7ES"
    json = {
        "sites": [
            {"name": "Site 1"},
            {"name": "Site 2"},
        ]
    }
    requests_mock.get(client._build_absolute_uri(url), json=json)
    form = site_forms.NewSiteConfirmForm(data=data, request=mock_request, postcode=postcode)
    form.is_valid()
    wizard = views.NewSiteWizardView(request=mock_request)
    wizard.steps = MagicMock()
    wizard.steps.current = views.CONFIRM
    result = wizard.render_next_step(form)
    assert result.url == reverse("organisation:sites:sites")


def test_new_site_form_request_postcode(mock_request, requests_mock, mock_post_site, organisation_pk):
    data = {"are_you_sure": "False"}
    postcode = "SW1 7ES"
    url = f"/organisations/{organisation_pk}/sites/?exclude=&get_total_users=False&postcode=SW1+7ES"
    json = {
        "sites": [
            {"name": "Site 1"},
            {"name": "Site 2"},
        ]
    }
    requests_mock.get(client._build_absolute_uri(url), json=json)
    form = site_forms.NewSiteConfirmForm(data=data, request=mock_request, postcode=postcode)
    form.is_valid()
    wizard = views.NewSiteWizardView(request=mock_request)
    wizard.request = "foo"
    wizard.storage = MagicMock()
    wizard.storage.get_step_data = MagicMock(return_value={"uk_address-postcode": "bar"})

    kwargs = wizard.get_form_kwargs(views.CONFIRM)
    assert kwargs == {
        "request": "foo",
        "postcode": "bar",
    }
