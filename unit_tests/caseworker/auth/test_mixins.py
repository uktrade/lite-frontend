from bs4 import BeautifulSoup
from unittest import mock
from django.views.generic.base import View
from core.auth.views import LoginRequiredMixin


def test_login_redirect(client):
    response = client.get("/")
    assert response.status_code == 302
    assert response.url == "/auth/login/?next=/"


@mock.patch("core.client.post")
def test_login_redirect_no_gov_user(mock_post, client, rf):
    data = mock.MagicMock()
    data.status_code = 403
    mock_post.return_value = data

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
    assert "User not found" in soup.h1.string
    assert "You are not registered to use this system" in soup.select(".govuk-body")[0]


@mock.patch("core.client.post")
def test_login_redirect_some_other_error(mock_post, client, rf):
    data = mock.MagicMock()
    data.status_code = 500
    mock_post.return_value = data

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
    assert "An error occurred" in soup.h1.string
