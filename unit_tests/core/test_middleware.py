from unittest import mock

import pytest
from django.conf import settings
from authlib.oauth2 import OAuth2Error

from rest_framework.exceptions import AuthenticationFailed
from rest_framework import status
from rest_framework.response import Response
from requests.models import Response as RResponse

from core import middleware


def test_no_cache_middleware(rf):
    request = rf.get("/")
    get_response = mock.Mock(return_value=Response())
    instance = middleware.NoCacheMiddleware(get_response)
    response = instance(request)
    assert response["Cache-Control"] == "max-age=0, no-cache, no-store, must-revalidate, private"


@pytest.mark.parametrize(
    "url,response_code",
    [
        ("?return_to=hello", status.HTTP_200_OK),
        ("?return_to=hello/", status.HTTP_200_OK),
        ("?return_to=/hello", status.HTTP_200_OK),
        ("?return_to=/hello/", status.HTTP_200_OK),
        ("?return_to=http://example.com", status.HTTP_403_FORBIDDEN),
        ("?return_to=http://example.com/", status.HTTP_403_FORBIDDEN),
        ("?return_to=https://example.com/", status.HTTP_403_FORBIDDEN),
        ('?return_to=javascript:alert("hello!")', status.HTTP_403_FORBIDDEN),
        # Protocol-relative URL
        ("?return_to=////example.com", status.HTTP_403_FORBIDDEN),
        ("?return_to=///example.com", status.HTTP_403_FORBIDDEN),
        ("?return_to=//example.com", status.HTTP_403_FORBIDDEN),
    ],
)
def test_validate_return_to_middleware(rf, url, response_code):
    request = rf.get(url)
    get_response = mock.Mock(return_value=Response())
    response = middleware.ValidateReturnToMiddleware(get_response)(request)
    assert response.status_code == response_code


@mock.patch("core.middleware.cache")
def test_sso_introspection_middleware_success(mock_cache, rf):
    # Set up mock request and response
    request = rf.get("/")
    request.authbroker_client = mock.Mock()
    request.authbroker_client.token = {"access_token": "test"}
    request.authbroker_client.get = mock.Mock()
    request.session = {"lite_api_user_id": "test-user"}
    get_response = mock.Mock(return_value=Response())
    # Set up mock cache
    mock_cache.set = mock.Mock()
    mock_cache.get = mock.Mock(return_value=None)
    # Instantiate and call the middleware
    instance = middleware.AuthBrokerTokenIntrospectionMiddleware(get_response)
    # We should get a 200 and the token should be cached
    response = instance(request)
    assert response.status_code == status.HTTP_200_OK
    request.authbroker_client.get.assert_called_once_with(settings.AUTHBROKER_PROFILE_URL)
    mock_cache.get.assert_called_once_with("sso_introspection:test")
    mock_cache.set.assert_called_once_with("sso_introspection:test", True, timeout=300)
    # If get returns a value, cache will not be set
    mock_cache.set = mock.Mock()
    mock_cache.get = mock.Mock(return_value=True)
    response = instance(request)
    assert response.status_code == status.HTTP_200_OK
    mock_cache.get.assert_called_once_with("sso_introspection:test")
    mock_cache.set.assert_not_called()


@pytest.mark.parametrize(
    "status_code",
    (
        status.HTTP_400_BAD_REQUEST,
        status.HTTP_401_UNAUTHORIZED,
        status.HTTP_403_FORBIDDEN,
        status.HTTP_404_NOT_FOUND,
        status.HTTP_405_METHOD_NOT_ALLOWED,
        status.HTTP_406_NOT_ACCEPTABLE,
        status.HTTP_408_REQUEST_TIMEOUT,
    ),
)
@mock.patch("core.middleware.cache")
def test_sso_introspection_middleware_request_error(mock_cache, status_code, rf):
    # Set up mock request and response
    request = rf.get("/")
    request.authbroker_client = mock.Mock()
    request.authbroker_client.token = {"access_token": "test"}
    request.session = mock.Mock()
    get_response = mock.Mock(return_value=Response())
    # Set up mock SSO response
    response = RResponse()
    response.status_code = status_code
    request.authbroker_client.get = mock.Mock(return_value=response)
    # Mock cache
    mock_cache.get = mock.Mock(return_value=None)
    # Call the middleware
    instance = middleware.AuthBrokerTokenIntrospectionMiddleware(get_response)
    response = instance(request)
    assert response.status_code == status.HTTP_302_FOUND


@mock.patch("core.middleware.cache")
def test_sso_introspection_middleware_oauth_error(mock_cache, rf):
    # Set up mock request and response
    request = rf.get("/")
    request.authbroker_client = mock.Mock()
    request.authbroker_client.token = {"access_token": "test"}
    request.session = mock.Mock()
    get_response = mock.Mock(return_value=Response())
    # Set up mock SSO response
    request.authbroker_client.get = mock.Mock(side_effect=OAuth2Error())
    # Mock cache
    mock_cache.get = mock.Mock(return_value=None)
    # Call the middleware
    instance = middleware.AuthBrokerTokenIntrospectionMiddleware(get_response)
    response = instance(request)
    assert response.status_code == status.HTTP_302_FOUND


def test_x_robots_tag_middleware(rf):
    # Set up mock request and response
    request = rf.get("/")
    get_response = mock.Mock(return_value=Response())
    # Instantiate and call the middleware
    instance = middleware.XRobotsTagMiddleware(get_response)
    # We should get a 200 and the token should be cached
    response = instance(request)
    assert response.status_code == status.HTTP_200_OK
    assert response.headers["x-robots-tag"] == "noindex,nofollow"
