import os

import pytest
from dotenv import load_dotenv
from django.conf import settings
from conf import exporter
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
def lite_api_user_id():
    return "d355428a-64cb-4347-853b-afcacee15d93"


@pytest.fixture
def mock_exporter_user(requests_mock, lite_api_user_id):
    url = client._build_absolute_uri("/users/authenticate/")
    data = {
        "user": {
            "id": 123,
            "email": "foo@example.com",
            "first_name": "Foo",
            "last_name": "Bar",
            "status": "Active",
            "token": "foo",
            "lite_api_user_id": lite_api_user_id,
        }
    }

    requests_mock.get(url=url, json=data)
    yield data


@pytest.fixture
def mock_exporter_user_me(requests_mock, lite_api_user_id):
    url = client._build_absolute_uri("/users/me/")
    data = {
        "user": {
            "id": 123,
            "email": "foo@example.com",
            "first_name": "Foo",
            "last_name": "Bar",
            "status": "Active",
            "token": "foo",
            "lite_api_user_id": lite_api_user_id,
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


@pytest.fixture()
def mock_get_profile(requests_mock, mock_exporter_user):
    url = exporter.AUTHBROKER_PROFILE_URL
    yield requests_mock.get(url=url, json={"sub": "123456789xyzqpr", "email": mock_exporter_user["user"]["email"]})


@pytest.fixture(autouse=True)
def mock_authenticate_user_save(requests_mock, mock_exporter_user):
    url = client._build_absolute_uri("/user/authenticate/")
    yield requests_mock.post(url=url)


@pytest.fixture
def mock_countries(requests_mock):
    url = client._build_absolute_uri("/static/countries/")
    # in relity there are around 275 countries
    data = {
        "countries": [
            {"id": "AE-AZ", "name": "Abu Dhabi", "type": "gov.uk Territory", "is_eu": False},
            {"id": "AF", "name": "Afghanistan", "type": "gov.uk Country", "is_eu": False},
            {"id": "AE-AJ", "name": "Ajman", "type": "gov.uk Territory", "is_eu": False},
            {"id": "IN", "name": "India", "type": "gov.uk Territory", "is_eu": False},
            {"id": "US", "name": "United States", "type": "gov.uk Territory", "is_eu": False},
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
