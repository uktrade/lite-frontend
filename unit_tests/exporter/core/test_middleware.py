from unittest import mock
import pytest

from django.conf import settings
from django.urls import reverse
from django.http import HttpResponse

from rest_framework.response import Response
from core.exceptions import ServiceError

from exporter.core.middleware import ServiceErrorHandler

from exporter.core.middleware import OrganisationRedirectMiddleWare


@pytest.fixture
def mock_token_request(rf):
    request = rf.get("/")
    request.authbroker_client = mock.Mock()
    request.authbroker_client.token = {"access_token": "test"}
    request.session = {}
    request.authbroker_client.get = mock.Mock()
    request.path_info = mock.Mock()
    request.path_info.startswith = mock.Mock(return_value=False)
    # Set up mock request and response
    return request


@pytest.fixture
def mock_get_user():
    yield mock.patch("exporter.core.middleware.get_user", {"organisations": []})


@pytest.mark.parametrize(
    "url",
    [
        "/register-an-organisation/draft-confirmation/",
        "/auth/logout/",
        "/register-an-organisation/confirm/",
        "/register-an-organisation/edit/name",
    ],
)
def test_organisation_redirect_ignore_paths(rf, url):
    request = rf.get(url)
    get_response = mock.Mock(return_value=Response())
    instance = OrganisationRedirectMiddleWare(get_response)
    response = instance(request)
    assert response.status_code == 200


def test_organisation_redirect_logged_in(mock_token_request):
    # Instantiate and call the middleware
    get_response = mock.Mock(return_value=Response())
    instance = OrganisationRedirectMiddleWare(get_response)
    response = instance(mock_token_request)
    assert response.status_code == 200


@mock.patch("exporter.core.middleware.get_user", return_value={"organisations": []})
def test_organisation_redirect_logged_in_no_orgs(mock_get_user, mock_token_request):
    # Set up mock request and response
    mock_token_request.session = {"user_token": "12345"}
    get_response = mock.Mock(return_value=Response())

    mock_get_user.return_value = {"organisations": []}
    # Instantiate and call the middleware
    instance = OrganisationRedirectMiddleWare(get_response)
    response = instance(mock_token_request)
    mock_get_user.called_once()
    assert response.status_code == 200


@mock.patch("exporter.core.middleware.get_user")
def test_organisation_redirect_logged_in_draft_org(mock_get_user, mock_token_request):
    # Set up mock request and response
    mock_token_request.session = {"user_token": "12345"}
    mock_get_user.return_value = {"organisations": [{"status": {"key": "draft"}}]}
    get_response = mock.Mock(return_value=Response())

    # Instantiate and call the middleware
    instance = OrganisationRedirectMiddleWare(get_response)
    response = instance(mock_token_request)
    mock_get_user.called_once()
    assert response.status_code == 302
    assert response.url == reverse("core:register_draft_confirm")


@mock.patch("exporter.core.middleware.get_user")
def test_organisation_redirect_logged_in_review(mock_get_user, mock_token_request):
    # Set up mock request and response
    mock_token_request.session = {"user_token": "12345"}
    mock_get_user.return_value = {"organisations": [{"status": {"key": "in_review"}}]}
    get_response = mock.Mock(return_value=Response())

    # Instantiate and call the middleware
    instance = OrganisationRedirectMiddleWare(get_response)
    response = instance(mock_token_request)
    mock_get_user.called_once()
    assert response.status_code == 302
    assert response.url == reverse("core:register_an_organisation_confirm") + "?animate=True"


def test_service_error_handler_non_service_error_exception(rf, mocker):
    get_response = mocker.MagicMock()
    service_error_handler = ServiceErrorHandler(get_response)

    request = rf.get("/")
    not_service_error = Exception()
    assert service_error_handler.process_exception(request, not_service_error) is None


def test_service_error_handler_service_error(rf, mocker, caplog, settings):
    settings.DEBUG = False
    get_response = mocker.MagicMock()
    service_error_handler = ServiceErrorHandler(get_response)

    request = rf.get("/")
    response = HttpResponse("OK")
    mock_error_page = mocker.patch("exporter.core.middleware.error_page")
    mock_error_page.return_value = response

    service_error = ServiceError(
        "Exception message",
        500,
        "Bad request",
        "Logger message",
        "Error message",
    )
    handler_response = service_error_handler.process_exception(request, service_error)

    assert handler_response == response
    assert ("ERROR", "Logger message") in [(r.levelname, r.msg) for r in caplog.records]
    mock_error_page.assert_called_with(request, "Error message")


def test_service_error_handler_service_error_with_debug(rf, mocker, caplog, settings):
    settings.DEBUG = True
    get_response = mocker.MagicMock()
    service_error_handler = ServiceErrorHandler(get_response)

    request = rf.get("/")
    response = HttpResponse("OK")
    mock_error_page = mocker.patch("exporter.core.middleware.error_page")
    mock_error_page.return_value = response

    service_error = ServiceError(
        "Exception message",
        500,
        "Bad request",
        "Logger message",
        "Error message",
    )

    with pytest.raises(ServiceError) as exception_info:
        service_error_handler.process_exception(request, service_error)

    assert exception_info.value == service_error
    assert ("ERROR", "Logger message") in [(r.levelname, r.msg) for r in caplog.records]
