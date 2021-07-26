from bs4 import BeautifulSoup
from unittest import mock
from django.views.generic.base import View
from core.auth.views import LoginRequiredMixin


def test_login_redirect(client):
    response = client.get("/")
    assert response.status_code == 302
    assert response.url == "/auth/login/?next=/"


@mock.patch("caseworker.auth.services.authenticate_gov_user")
def test_login_redirect_no_gov_user(mock_auth_gov_user, client, rf):
    mock_auth_gov_user.return_value = {}, 403

    class TestView(LoginRequiredMixin, View):
        pass

    request = rf.get("/")
    request.authbroker_client = mock.Mock()
    request.authbroker_client.authorized = True
    request.requests_session = mock.Mock()
    request.requests_session.request = mock.Mock()
    request.session = {
        "first_name": "John",
        "last_name": "Smith",
        "user_token": "foo",
    }
    response = TestView.as_view()(request)

    assert response.status_code == 200

    soup = BeautifulSoup(response.content, "html.parser")
    assert "User not found" in soup
