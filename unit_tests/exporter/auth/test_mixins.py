from unittest import mock
from bs4 import BeautifulSoup
from django.views.generic.base import View
from django.urls import reverse

from core.auth.views import LoginRequiredMixin


class MockResponse:
    def __init__(self, data, status_code):
        self.data = data
        self.status_code = status_code

    def json(self):
        return self.data


@mock.patch("core.client.post")
def test_login_redirect_bad_request(mock_post, client, rf):
    mock_response = MockResponse(
        data={
            "errors": "Something went wrong"
        },
        status_code=400
    )
    mock_post.return_value = mock_response

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
    assert "Something went wrong" in soup.select(".govuk-body")[0]


@mock.patch("core.client.post")
def test_login_redirect_unauthorised(mock_post, client, rf):
    mock_response = MockResponse(
        data={},
        status_code=401
    )
    mock_post.return_value = mock_response

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

    assert response.status_code == 302
    assert response.url == reverse("core:register_an_organisation_triage")


@mock.patch("core.client.post")
def test_login_redirect_other_error(mock_post, client, rf):
    mock_response = MockResponse(
        data={},
        status_code=500
    )
    mock_post.return_value = mock_response

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
