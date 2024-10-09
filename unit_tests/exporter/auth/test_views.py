import pytest

from django.conf import settings
from django.urls import reverse
from django.utils.http import urlencode


@pytest.fixture
def mock_get_authbroker_client(mocker):
    mock_get_authbroker_client = mocker.patch("core.auth.middleware.get_authbroker_client")
    mock_get_authbroker_client.return_value.authbroker_client.return_value.fetch_token.return_value = {"token": "dict"}
    yield mock_get_authbroker_client


@pytest.fixture
def home_url():
    return reverse("core:home")


@pytest.fixture
def login_url():
    return reverse("auth:login")


@pytest.fixture
def callback_url():
    return reverse("auth:callback")


@pytest.fixture
def register_name_url():
    return reverse("core:register_name")


@pytest.fixture
def register_an_organisation_triage_url():
    return reverse("core:register_an_organisation_triage")


@pytest.fixture
def logout_url():
    return reverse("auth:logout")


@pytest.fixture()
def mock_authenticate_exporter_user_error(requests_mock):
    yield requests_mock.post(url="/users/authenticate/", status_code=401, json={})


def test_callback_no_auth_code(authorized_client, callback_url, login_url, caplog):
    response = authorized_client.get(callback_url)
    assert response.status_code == 302
    assert response.url == login_url
    assert ("ERROR", "No auth code from authbroker") in [(r.levelname, r.msg) for r in caplog.records]


def test_callback_no_state_in_session(authorized_client, callback_url, caplog):
    response = authorized_client.get(f"{callback_url}?code=authcode12345")
    assert response.status_code == 400
    assert ("ERROR", "No state found in session") in [(r.levelname, r.msg) for r in caplog.records]


def test_callback_state_differs_to_session(authorized_client, callback_url, caplog, settings):
    session = authorized_client.session
    session[f"{settings.TOKEN_SESSION_KEY}_oauth_state"] = "state_key"
    session.save()

    response = authorized_client.get(f"{callback_url}?code=authcode12345&state=different_state_key")
    assert response.status_code == 400
    assert ("ERROR", "Session state and passed back state differ") in [(r.levelname, r.msg) for r in caplog.records]


def test_callback_no_user_in_db_name_set(
    authorized_client,
    callback_url,
    settings,
    mocker,
    register_an_organisation_triage_url,
    mock_get_authbroker_client,
):
    session = authorized_client.session
    session[f"{settings.TOKEN_SESSION_KEY}_oauth_state"] = "state_key"
    session.save()

    mock_authenticate_user = mocker.patch("exporter.auth.views.AuthCallbackView.authenticate_user")
    mock_authenticate_user.return_value = {}, 401

    mock_user_profile = mocker.patch(
        "exporter.auth.views.AuthCallbackView.user_profile",
        new_callable=mocker.PropertyMock,
    )
    mock_user_profile.return_value = {
        "email": "email@example.com",
    }
    response = authorized_client.get(f"{callback_url}?code=authcode12345&state=state_key")
    assert response.status_code == 302
    assert response.url == register_an_organisation_triage_url


def test_callback_no_user_in_db_no_name_set(
    authorized_client,
    callback_url,
    settings,
    mocker,
    mock_get_authbroker_client,
    mock_authenticate_exporter_user_error,
    register_name_url,
):
    session = authorized_client.session
    session[f"{settings.TOKEN_SESSION_KEY}_oauth_state"] = "state_key"
    del session["first_name"]
    session.save()

    mock_user_profile = mocker.patch(
        "exporter.auth.views.AuthCallbackView.user_profile",
        new_callable=mocker.PropertyMock,
    )
    mock_user_profile.return_value = {
        "email": "email@example.com",
    }
    response = authorized_client.get(f"{callback_url}?code=authcode12345&state=state_key")
    assert response.status_code == 302
    assert response.url == register_name_url


def test_callback_success_no_name_set(
    authorized_client,
    callback_url,
    settings,
    mocker,
    mock_get_authbroker_client,
    register_name_url,
):
    session = authorized_client.session
    session[f"{settings.TOKEN_SESSION_KEY}_oauth_state"] = "state_key"
    session.save()

    mock_authenticate_user = mocker.patch("exporter.auth.views.AuthCallbackView.authenticate_user")
    mock_authenticate_user.return_value = {
        "token": "token_12345",
        "lite_api_user_id": "lite_api_user_id_12345",
        "first_name": None,
        "last_name": None,
    }, 200

    mock_user_profile = mocker.patch(
        "exporter.auth.views.AuthCallbackView.user_profile",
        new_callable=mocker.PropertyMock,
    )
    mock_user_profile.return_value = {
        "email": "email@example.com",
    }

    response = authorized_client.get(f"{callback_url}?code=authcode12345&state=state_key")
    assert response.status_code == 302
    assert response.url == register_name_url

    session = authorized_client.session
    assert session["user_token"] == "token_12345"
    assert session["lite_api_user_id"] == "lite_api_user_id_12345"
    assert session["email"] == "email@example.com"


def test_callback_success(
    authorized_client,
    callback_url,
    settings,
    mocker,
    mock_get_authbroker_client,
    home_url,
):
    session = authorized_client.session
    session[f"{settings.TOKEN_SESSION_KEY}_oauth_state"] = "state_key"
    session.save()

    mock_authenticate_user = mocker.patch("exporter.auth.views.AuthCallbackView.authenticate_user")
    mock_authenticate_user.return_value = {
        "token": "token_12345",
        "lite_api_user_id": "lite_api_user_id_12345",
        "first_name": "Firstname",
        "last_name": "Lastname",
    }, 200

    mock_user_profile = mocker.patch(
        "exporter.auth.views.AuthCallbackView.user_profile",
        new_callable=mocker.PropertyMock,
    )
    mock_user_profile.return_value = {
        "email": "email@example.com",
    }

    response = authorized_client.get(f"{callback_url}?code=authcode12345&state=state_key")
    assert response.status_code == 302
    assert response.url == home_url

    session = authorized_client.session
    assert session["user_token"] == "token_12345"
    assert session["lite_api_user_id"] == "lite_api_user_id_12345"
    assert session["email"] == "email@example.com"
    assert session["first_name"] == "Firstname"
    assert session["last_name"] == "Lastname"


def test_log_out_logged_in(authorized_client, logout_url):
    session = authorized_client.session

    assert session[settings.TOKEN_SESSION_KEY]
    response = authorized_client.get(logout_url)
    assert response.status_code == 302
    assert settings.TOKEN_SESSION_KEY not in authorized_client.session
    assert response.url == settings.LOGOUT_URL + "http://testserver/"


def test_log_out_gov_signout_with_token(authorized_client, logout_url):
    session = authorized_client.session
    session[settings.TOKEN_SESSION_KEY].update({"id_token": "mock_id_token"})
    session.save()
    redirect_logout = urlencode({"id_token_hint": "mock_id_token", "post_logout_redirect_uri": "http://testserver/"})
    response = authorized_client.get(logout_url)
    assert response.status_code == 302
    assert settings.TOKEN_SESSION_KEY not in authorized_client.session
    assert response.url == f"{settings.LOGOUT_URL}?{redirect_logout}"


def test_log_out_non_logged_in(client, logout_url):
    response = client.get(logout_url)
    assert response.status_code == 302
    assert response.url == "http://testserver/"
