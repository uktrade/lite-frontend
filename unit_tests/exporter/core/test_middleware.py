import pytest
from unittest import mock
from django.http import HttpResponse
from django.urls import reverse

from rest_framework.response import Response
from rest_framework import status

from core.exceptions import ServiceError
from exporter.core.middleware import ServiceErrorHandler, OrganisationRedirectMiddleWare


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


def test_organisation_middleware_logout_accessible(rf):
    # Set up mock request and response
    request = rf.get(reverse("auth:logout"))
    request.authbroker_client = mock.Mock()
    request.authbroker_client.token = {"access_token": "test"}
    request.authbroker_client.get = mock.Mock()
    request.session = {"lite_api_user_id": "test-user"}
    get_response = mock.Mock(return_value=Response())

    # Instantiate and call the middleware
    instance = OrganisationRedirectMiddleWare(get_response)
    # We should get a 200 use to allowed to log out
    response = instance(request)
    assert response.status_code == status.HTTP_200_OK


def test_organisation_middleware_user_no_name(rf):
    # Set up mock request and response
    request = rf.get("/")
    request.authbroker_client = mock.Mock()
    request.authbroker_client.token = {"access_token": "test"}
    request.authbroker_client.get = mock.Mock()
    request.session = {}
    get_response = mock.Mock(return_value=Response())

    # Instantiate and call the middleware
    instance = OrganisationRedirectMiddleWare(get_response)
    # We should get a 200 use to allowed to log out
    response = instance(request)
    assert response.status_code == 302
    assert response.url == reverse("core:register_name")


def test_organisation_middleware_user_directs_to_registration(rf):
    # Set up mock request and response
    request = rf.get("/")
    request.authbroker_client = mock.Mock()
    request.authbroker_client.token = {"access_token": "test"}
    request.authbroker_client.get = mock.Mock()
    request.session = {"first_name": "first_name", "second_name": "second_name"}
    get_response = mock.Mock(return_value=Response())

    # Instantiate and call the middleware
    instance = OrganisationRedirectMiddleWare(get_response)
    # We should get a 200 use to allowed to log out
    response = instance(request)
    assert response.status_code == 302
    assert response.url == reverse("core:register_an_organisation_triage")


@mock.patch("exporter.core.middleware.get_user")
def test_organisation_middleware_user_org_in_review(mock_get_user, rf):
    # Set up mock request and response
    request = rf.get("/")
    request.authbroker_client = mock.Mock()
    request.authbroker_client.token = {"access_token": "test"}
    request.authbroker_client.get = mock.Mock()
    request.session = {"user_token": "xyz"}
    get_response = mock.Mock(return_value=Response())
    mock_get_user.return_value = {"organisations": [{"status": {"key": "in_review"}}]}
    # Instantiate and call the middleware
    instance = OrganisationRedirectMiddleWare(get_response)
    # We should get a 200 use to allowed to log out
    response = instance(request)
    assert response.status_code == 302
    assert response.url == reverse("core:register_an_organisation_confirm") + "?animate=True"
