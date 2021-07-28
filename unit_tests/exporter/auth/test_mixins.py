from unittest import mock
from bs4 import BeautifulSoup
from django.conf import settings
from django.views.generic.base import TemplateView
from django.urls import reverse

from core.auth.views import LoginRequiredMixin


def test_login_redirect_no_sso_auth(client, rf):

    class TestView(LoginRequiredMixin, TemplateView):
        template_name = "core/start.html"

    request = rf.get("/")
    request.authbroker_client = mock.Mock()
    request.authbroker_client.authorized = False
    response = TestView.as_view()(request)

    assert response.status_code == 302
    assert response.url == "/auth/login/?next=/"


def test_login_redirect_logged_in(client, rf):

    class TestView(LoginRequiredMixin, TemplateView):
        template_name = "core/start.html"

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
    response.render()

    assert response.status_code == 200

    soup = BeautifulSoup(response.content, "html.parser")
    assert "Export control account: sign in or set up" in soup.h1.string
