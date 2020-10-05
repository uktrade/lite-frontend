import pytest

from django.conf import settings
from django.test import Client

from core import client


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
def authorized_client_factory(client: Client, settings):
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
