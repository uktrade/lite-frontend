import os

import pytest
from dotenv import load_dotenv
from django.conf import settings
from django.test import Client

from core import client


DEFAULT_ENVFILE = "exporter.env"


def pytest_configure(config):
    """
    Load exporter env variables automagically
    """
    if not os.environ.get("PIPENV_DOTENV_LOCATION"):
        load_dotenv(dotenv_path=DEFAULT_ENVFILE, override=True)


@pytest.fixture
def mock_exporter_user(requests_mock):
    url = client._build_absolute_uri("/users/authenticate/")
    data = {
        "user": {
            "id": 123,
            "email": "foo@example.com",
            "first_name": "Foo",
            "last_name": "Bar",
            "status": "Active",
            "token": "foo",
            "lite_api_user_id": "d355428a-64cb-4347-853b-afcacee15d93",
        }
    }

    requests_mock.get(url=url, json=data)
    yield data


@pytest.fixture
def mock_exporter_user_me(requests_mock):
    url = client._build_absolute_uri("/users/me/")
    data = {
        "user": {
            "id": 123,
            "email": "foo@example.com",
            "first_name": "Foo",
            "last_name": "Bar",
            "status": "Active",
            "token": "foo",
            "lite_api_user_id": "d355428a-64cb-4347-853b-afcacee15d93",
            "organisations": [
                {
                    "id": "9bc26604-35ee-4383-9f58-74f8cab67443",
                    "name": "Archway Communications",
                    "joined_at": "2020-06-29T09:30:58.425994Z",
                    "status": {"key": "active", "value": "Active"},
                }
            ],
        },
        "role": {
            "id": "00000000-0000-0000-0000-000000000001",
            "permissions": [
                "ADMINISTER_USERS",
                "ADMINISTER_SITES",
                "EXPORTER_ADMINISTER_ROLES",
                "SUBMIT_LICENCE_APPLICATION",
                "SUBMIT_CLEARANCE_APPLICATION",
            ],
        },
    }

    requests_mock.get(url=url, json=data)
    yield data


@pytest.fixture
def authorized_client_factory(client: Client, settings, organisation_pk):
    """
    returns a factory to make a authorized client for a mock_exporter_user,

    the factory only expects the value of "user" inside the object returned by
    the mock_exporter_user fixture
    """

    def _inner(user):
        session = client.session
        session["first_name"] = user["first_name"]
        session["last_name"] = user["last_name"]
        session["user_token"] = user["token"]
        session["lite_api_user_id"] = user["lite_api_user_id"]
        session["email"] = user["email"]
        session["organisation"] = organisation_pk
        session[settings.TOKEN_SESSION_KEY] = {
            "access_token": "mock_access_token",
            "expires_in": 36000,
            "token_type": "Bearer",
            "scope": ["read", "write"],
            "refresh_token": "mock_refresh_token",
        }
        session.save()
        client.cookies[settings.SESSION_COOKIE_NAME] = session.session_key
        return client

    yield _inner


@pytest.fixture
def authorized_client(authorized_client_factory, mock_exporter_user):
    return authorized_client_factory(mock_exporter_user["user"])


@pytest.fixture
def mock_countries(requests_mock):
    url = client._build_absolute_uri("/static/countries/")
    # in relity there are around 275 countries
    data = {
        "countries": [
            {"id": "AE-AZ", "name": "Abu Dhabi", "type": "gov.uk Territory", "is_eu": False},
            {"id": "AF", "name": "Afghanistan", "type": "gov.uk Country", "is_eu": False},
            {"id": "AE-AJ", "name": "Ajman", "type": "gov.uk Territory", "is_eu": False},
        ]
    }

    requests_mock.get(url=url, json=data)
    yield data


@pytest.fixture
def mock_units(requests_mock):
    url = client._build_absolute_uri("/static/units/")
    data = {
        "units": {
            "GRM": "Gram(s)",
            "KGM": "Kilogram(s)",
            "NAR": "Number of articles",
            "MTK": "Square metre(s)",
            "MTR": "Metre(s)",
            "LTR": "Litre(s)",
            "MTQ": "Cubic metre(s)",
            "ITG": "Intangible",
        }
    }

    requests_mock.get(url=url, json=data)
    yield data


@pytest.fixture(autouse=True)
def mock_notifications(requests_mock):
    url = client._build_absolute_uri("/users/notifications/")
    data = {}
    requests_mock.get(url=url, json=data)
    yield data


@pytest.fixture(autouse=True)
def mock_has_existing_applications_and_licences_and_nlrs(requests_mock):
    url = client._build_absolute_uri("/applications/existing/")
    data = {"applications": True}
    requests_mock.get(url=url, json=data)
    yield data


@pytest.fixture()
def data_draft_standard_application(data_standard_case):
    return {
        "activity": None,
        "additional_documents": [],
        "agreed_to_foi": None,
        "case": data_standard_case["case"]["id"],
        "case_officer": None,
        "case_type": {
            "id": "00000000-0000-0000-0000-000000000004",
            "reference": {"key": "siel", "value": "Standard Individual Export Licence"},
            "sub_type": {"key": "standard", "value": "Standard Licence"},
            "type": {"key": "application", "value": "Application"},
        },
        "compliant_limitations_eu_ref": None,
        "consignee": None,
        "created_at": "2021-11-12T16:39:14.281840Z",
        "denial_matches": [],
        "destinations": {"data": "", "type": "end_user"},
        "end_user": None,
        "export_type": {"key": "", "value": None},
        "exporter_user_notification_count": {},
        "foi_reason": "",
        "goods": [],
        "goods_locations": {},
        "goods_recipients": "",
        "goods_starting_point": "",
        "have_you_been_informed": "no",
        "id": "a0cf9617-ff14-4562-8c87-a774816f1954",
        "inactive_parties": [],
        "informed_wmd_ref": None,
        "intended_end_use": None,
        "is_amended": False,
        "is_compliant_limitations_eu": None,
        "is_eu_military": None,
        "is_informed_wmd": None,
        "is_major_editable": True,
        "is_military_end_use_controls": None,
        "is_shipped_waybill_or_lading": True,
        "is_suspected_wmd": None,
        "is_temp_direct_control": False,
        "last_closed_at": None,
        "licence": None,
        "military_end_use_controls_ref": None,
        "name": "Locations test",
        "non_waybill_or_lading_route_details": None,
        "organisation": {
            "created_at": "2021-10-05T15:30:05.449251+01:00",
            "documents": [],
            "eori_number": "1234567890AAA",
            "flags": [],
            "id": "b07f02bd-4eba-43c5-99c8-c3fe805ed59c",
            "name": "Archway Communications",
            "phone_number": "",
            "primary_site": {
                "address": {
                    "address_line_1": "42 Question Road",
                    "address_line_2": "",
                    "city": "London",
                    "country": {
                        "id": "GB",
                        "is_eu": True,
                        "name": "United " "Kingdom",
                        "report_name": "",
                        "type": "gov.uk Country",
                    },
                    "id": "b8580cd7-9446-494e-8464-d0fb28d8e95c",
                    "postcode": "SW1A 0AA",
                    "region": "Greater London",
                },
                "id": "6febe516-ddb5-4604-ad57-760d8be3b6df",
                "name": "Headquarters",
                "records_located_at": {
                    "address": {
                        "address_line_1": "42 " "Question " "Road",
                        "address_line_2": "",
                        "city": "London",
                        "country": {"name": "United " "Kingdom"},
                        "postcode": "SW1A " "0AA",
                        "region": "Greater " "London",
                    },
                    "id": "6febe516-ddb5-4604-ad57-760d8be3b6df",
                    "name": "Headquarters",
                },
            },
            "registration_number": "09876543",
            "sic_number": "2345",
            "status": {"key": "active", "value": "Active"},
            "type": {"key": "commercial", "value": "Commercial Organisation"},
            "updated_at": "2021-10-05T15:30:05.454346+01:00",
            "vat_number": "GB123456789",
            "website": "",
        },
        "proposed_return_date": "2022-01-01",
        "reference_code": None,
        "reference_number_on_information_form": None,
        "sanction_matches": [],
        "sla_days": 0,
        "sla_remaining_days": None,
        "sla_updated_at": None,
        "status": {"id": "00000000-0000-0000-0000-000000000000", "key": "draft", "value": "draft"},
        "submitted_at": None,
        "submitted_by": "",
        "suspected_wmd_ref": None,
        "temp_direct_control_details": "",
        "temp_export_details": "",
        "third_parties": [],
        "trade_control_activity": {"key": None, "value": None},
        "trade_control_product_categories": [],
        "ultimate_end_users": [],
        "updated_at": "2021-11-15T12:46:03.018683Z",
        "usage": None,
    }


@pytest.fixture()
def mock_get_application(requests_mock, data_standard_case, data_draft_standard_application):
    url = client._build_absolute_uri(f"/applications/{data_standard_case['case']['id']}/")
    yield requests_mock.get(url=url, json=data_draft_standard_application)


@pytest.fixture()
def mock_put_application(requests_mock, data_standard_case):
    url = client._build_absolute_uri(f"/applications/{data_standard_case['case']['id']}/")
    yield requests_mock.put(url=url, json={})


@pytest.fixture()
def mock_put_application_route_of_goods(requests_mock, data_standard_case):
    url = client._build_absolute_uri(f"/applications/{data_standard_case['case']['id']}/route-of-goods/")
    yield requests_mock.put(url=url, json={})
