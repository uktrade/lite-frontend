from django.conf import settings
from django.urls import reverse


def test_mock_authorize(client):
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


def test_mock_authorize_bad_request(client):
    url = reverse("mock_sso:authorize")

    response = client.get(url, {})

    assert response.status_code == 400


def test_mock_token(client):
    url = reverse("mock_sso:token")

    response = client.post(url)

    assert response.status_code == 200
    assert response.json() == {"access_token": "DUMMYTOKEN", "token_type": "Bearer"}


def test_mock_api_user_me(client):
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
