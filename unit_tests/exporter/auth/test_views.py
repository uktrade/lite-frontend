from django.urls import reverse
from django.conf import settings
from django.utils.http import urlencode


def test_log_out_logged_in(authorized_client):
    session = authorized_client.session

    assert session[settings.TOKEN_SESSION_KEY]
    url = reverse("auth:logout")
    response = authorized_client.get(url)
    assert response.status_code == 302
    assert settings.TOKEN_SESSION_KEY not in authorized_client.session
    assert response.url == settings.LOGOUT_URL + "http://testserver/"


def test_log_out_gov_signout_with_token(authorized_client):
    session = authorized_client.session
    session[settings.TOKEN_SESSION_KEY].update({"id_token": "mock_id_token"})
    session.save()
    redirect_logout = urlencode({"id_token_hint": "mock_id_token", "post_logout_redirect_uri": "http://testserver/"})
    url = reverse("auth:logout")
    response = authorized_client.get(url)
    assert response.status_code == 302
    assert settings.TOKEN_SESSION_KEY not in authorized_client.session
    assert response.url == f"{settings.LOGOUT_URL}?{redirect_logout}"


def test_log_out_non_logged_in(client):
    url = reverse("auth:logout")
    response = client.get(url)
    assert response.status_code == 302
    assert response.url == "http://testserver/"
