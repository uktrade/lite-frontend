import time

import jwt
import pytest
from django.urls import reverse

from unit_tests.helpers import reload_urlconf


@pytest.fixture(autouse=True)
def use_mock_sso(settings):
    # reload_urlconf is a little expensive, so while autouse=True is set
    # for these tests, this fixture should not be moved to conftest as-is.
    settings.MOCK_SSO_ACTIVATE_ENDPOINTS = True
    settings.MOCK_SSO_USER_EMAIL = "test-uat-user@digital.trade.gov.uk"
    settings.MOCK_SSO_USER_FIRST_NAME = "LITE"
    settings.MOCK_SSO_USER_LAST_NAME = "Testing"
    settings.MOCK_SSO_SECRET_KEY = "cd8a0206dee80a90c61bb1251637b4785e5716e13ce4d064fdd932ffc0546682"
    settings.AUTHBROKER_LOW_SECURITY = True

    reload_urlconf()


def test_authorize_endpoint_mock_sso(client):
    url = reverse("mock_sso:authorize")
    redirect_uri = "http://localhost/some-redirect/"
    state = "dummystate"
    get_params = {
        "response_type": "code",
        "client_id": "dummyid",
        "redirect_uri": redirect_uri,
        "scope": "read+write",
        "state": state,
    }

    response = client.get(url, get_params)

    assert response.status_code == 302
    assert response["Location"] == redirect_uri + f"?code=DUMMYCODE&state={state}"


def test_authorize_endpoint_mock_sso_bad_request(client):
    url = reverse("mock_sso:authorize")

    response = client.get(url, {})

    assert response.status_code == 400


def test_token_endpoint_mock_sso(client):
    url = reverse("mock_sso:token")

    response = client.post(url)

    assert response.status_code == 200
    assert response.json() == {"access_token": "DUMMYTOKEN", "token_type": "Bearer"}


def test_api_user_me_endpoint_mock_sso(settings, client):
    # Pre GovUK OneLogin SSO user info endpoint
    url = reverse("mock_sso:api_user_me")

    response = client.get(url)

    assert response.status_code == 200
    assert response.json() == {
        "email": settings.MOCK_SSO_USER_EMAIL,
        "contact_email": settings.MOCK_SSO_USER_EMAIL,
        "email_user_id": settings.MOCK_SSO_USER_EMAIL,
        "user_id": "20a0353f-a7d1-4851-9af8-1bcaff152b60",
        "first_name": settings.MOCK_SSO_USER_FIRST_NAME,
        "last_name": settings.MOCK_SSO_USER_LAST_NAME,
        "related_emails": [],
        "groups": [],
        "permitted_applications": [],
        "access_profiles": [],
    }


def test_api_userinfo_endpoint_mock_sso(settings, client):
    # GovUK OneLogin SSO user info endpoint
    # Test the UserInfo endpoint with a minimal client claim
    settings.MOCK_SSO_SECRET_KEY = "cd8a0206dee80a90c61bb1251637b4785e5716e13ce4d064fdd932ffc0546682"

    url = reverse("mock_sso:userinfo")

    # Build the client claim
    # Timestamps must be ints, representing seconds from the epoch
    issued_at = int(time.time())
    expiration_time = issued_at + 3600
    mock_client_id = "mock-client-id"
    secret_key = settings.MOCK_SSO_SECRET_KEY
    audience = "https://oidc.integration.account.gov.uk/token"

    # JWT spec: https://docs.sign-in.service.gov.uk/integrate-with-integration-environment/integrate-with-code-flow/#create-a-jwt
    core_identity_jwt_payload = {
        "iss": mock_client_id,
        "sub": mock_client_id,
        "aud": audience,
        "iat": issued_at,
        "exp": f"{expiration_time}",
        "jti": "dummy-jti",
    }

    response = client.get(url)

    assert response.status_code == 200

    response_data = response.json()
    # JWT needs special handling so remove it and verify rest of the data first
    core_identity_jwt = response_data.pop("https://vocab.account.gov.uk/v1/coreIdentityJWT")

    assert response_data == {
        "email": settings.MOCK_SSO_USER_EMAIL,
        "contact_email": settings.MOCK_SSO_USER_EMAIL,
        "email_user_id": settings.MOCK_SSO_USER_EMAIL,
        "user_id": "20a0353f-a7d1-4851-9af8-1bcaff152b60",
        "first_name": settings.MOCK_SSO_USER_FIRST_NAME,
        "last_name": settings.MOCK_SSO_USER_LAST_NAME,
        "related_emails": [],
        "groups": [],
        "permitted_applications": [],
        "access_profiles": [],
    }

    # Verify the round trip works (jwt verifies some fields, e.g. expiration must be an int not a float)
    actual_core_identity_payload = jwt.decode(core_identity_jwt, secret_key, "HS256", audience=audience)
    assert actual_core_identity_payload == core_identity_jwt_payload
