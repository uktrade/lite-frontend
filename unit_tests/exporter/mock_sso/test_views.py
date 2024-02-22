import pytest
import uuid

from unittest.mock import patch
from urllib import parse

from bs4 import BeautifulSoup

from django.conf import settings
from django.urls import reverse


@pytest.fixture(autouse=True)
def configure_settings(settings):
    try:
        del settings.MOCK_SSO_USER_EMAIL
    except AttributeError:
        pass
    settings.MOCK_SSO_USER_FIRST_NAME = "test"
    settings.MOCK_SSO_USER_LAST_NAME = "user"


@pytest.fixture
def state():
    return "dummystate"


@pytest.fixture
def redirect_uri():
    return "http://localhost/some-redirect/"


@pytest.fixture
def get_params(redirect_uri, state):
    return {
        "response_type": "code",
        "client_id": "dummyid",
        "redirect_uri": redirect_uri,
        "scope": "read+write",
        "state": state,
    }


@pytest.fixture
def authorize_url():
    return reverse("mock_sso:authorize")


@pytest.fixture
def token_url():
    return reverse("mock_sso:token")


@pytest.fixture
def email():
    return "explicit-test-email@example.com"  # /PS-IGNORE


@pytest.fixture
def settings_email(settings):
    email = "default-email@example.com"  # /PS-IGNORE
    settings.MOCK_SSO_USER_EMAIL = email
    return email


@patch("core.mock_sso.views.uuid")
def test_mock_authorize(mock_uuid, client, redirect_uri, state, authorize_url, get_params, email):
    code = str(uuid.uuid4())
    mock_uuid.uuid4.return_value = code
    assert parse.urljoin(settings.AUTHBROKER_URL, authorize_url) == settings.AUTHBROKER_AUTHORIZATION_URL

    response = client.get(authorize_url, get_params)
    assert response.status_code == 200
    soup = BeautifulSoup(response.content, "html.parser")
    assert soup.find("input", {"name": "email"})
    assert soup.find("form").attrs["action"] == ""

    response = client.post(f"{authorize_url}?{parse.urlencode(get_params)}", data={"email": email})
    assert response.status_code == 302
    assert response["Location"] == redirect_uri + f"?code={code}&state={state}"


@patch("core.mock_sso.views.uuid")
def test_mock_authorize_default_email(
    mock_uuid, settings_email, client, redirect_uri, state, authorize_url, get_params
):
    code = str(uuid.uuid4())
    mock_uuid.uuid4.return_value = code
    response = client.get(authorize_url, get_params)
    assert response.status_code == 302
    assert response["Location"] == redirect_uri + f"?code={code}&state={state}"


@patch("core.mock_sso.views.uuid")
def test_mock_authorize_pulls_from_session_on_multiple_requests(
    mock_uuid, client, redirect_uri, state, authorize_url, get_params, email
):
    code = str(uuid.uuid4())
    mock_uuid.uuid4.return_value = code
    assert parse.urljoin(settings.AUTHBROKER_URL, authorize_url) == settings.AUTHBROKER_AUTHORIZATION_URL

    response = client.get(authorize_url, get_params)
    assert response.status_code == 200

    response = client.post(f"{authorize_url}?{parse.urlencode(get_params)}", data={"email": email})
    assert response.status_code == 302
    assert response["Location"] == redirect_uri + f"?code={code}&state={state}"

    response = client.get(authorize_url, get_params)
    assert response.status_code == 302
    assert response["Location"] == redirect_uri + f"?code={code}&state={state}"


def test_mock_authorize_bad_request(client, authorize_url):
    response = client.get(authorize_url, {})

    assert response.status_code == 400


@patch("core.mock_sso.views.uuid")
def test_mock_token(mock_uuid, client, authorize_url, get_params, token_url, email):
    code = str(uuid.uuid4())
    mock_uuid.uuid4.return_value = code
    client.post(f"{authorize_url}?{parse.urlencode(get_params)}", data={"email": email})

    assert parse.urljoin(settings.AUTHBROKER_URL, token_url) == settings.AUTHBROKER_TOKEN_URL

    access_token = str(uuid.uuid4())
    mock_uuid.uuid4.return_value = access_token
    response = client.post(token_url, data={"code": code})

    assert response.status_code == 200
    assert response.json() == {"access_token": access_token, "token_type": "Bearer", "id_token": "DUMMYIDTOKEN"}


@patch("core.mock_sso.views.uuid")
def test_mock_api_user_me(mock_uuid, client, get_params, authorize_url, token_url, email):
    code = str(uuid.uuid4())
    mock_uuid.uuid4.return_value = code
    client.post(f"{authorize_url}?{parse.urlencode(get_params)}", data={"email": email})

    access_token = str(uuid.uuid4())
    mock_uuid.uuid4.return_value = access_token
    client.post(token_url, data={"code": code})

    url = reverse("mock_sso:api_user_me")
    assert parse.urljoin(settings.AUTHBROKER_URL, url) == settings.AUTHBROKER_PROFILE_URL

    response = client.get(url, headers={"Authorization": f"Bearer {access_token}"})

    assert response.status_code == 200
    assert response.json() == {
        "email": email,
        "contact_email": email,
        "email_user_id": email,
        "user_id": "20a0353f-a7d1-4851-9af8-1bcaff152b60",
        "first_name": settings.MOCK_SSO_USER_FIRST_NAME,
        "last_name": settings.MOCK_SSO_USER_LAST_NAME,
        "related_emails": [],
        "groups": [],
        "permitted_applications": [],
        "access_profiles": [],
    }


@patch("core.mock_sso.views.uuid")
def test_mock_api_user_me_default_email(mock_uuid, settings_email, client, get_params, authorize_url, token_url):
    code = str(uuid.uuid4())
    mock_uuid.uuid4.return_value = code
    client.get(f"{authorize_url}?{parse.urlencode(get_params)}")

    access_token = str(uuid.uuid4())
    mock_uuid.uuid4.return_value = access_token
    client.post(token_url, data={"code": code})

    url = reverse("mock_sso:api_user_me")
    assert parse.urljoin(settings.AUTHBROKER_URL, url) == settings.AUTHBROKER_PROFILE_URL

    response = client.get(url, headers={"Authorization": f"Bearer {access_token}"})

    assert response.status_code == 200
    assert response.json() == {
        "email": settings_email,
        "contact_email": settings_email,
        "email_user_id": settings_email,
        "user_id": "20a0353f-a7d1-4851-9af8-1bcaff152b60",
        "first_name": settings.MOCK_SSO_USER_FIRST_NAME,
        "last_name": settings.MOCK_SSO_USER_LAST_NAME,
        "related_emails": [],
        "groups": [],
        "permitted_applications": [],
        "access_profiles": [],
    }


def test_mock_logout(client):
    url = reverse("mock_sso:logout")
    assert parse.urljoin(settings.AUTHBROKER_URL, url) == settings.LOGOUT_URL

    response = client.get(f"{url}?post_logout_redirect_uri=http://example.com")

    assert response.status_code == 302
    assert response.url == "http://example.com"
