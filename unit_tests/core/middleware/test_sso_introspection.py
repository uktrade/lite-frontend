import jwt
import pytest

from unittest import mock

from authlib.oauth2 import OAuth2Error
from authlib.integrations.base_client.errors import OAuthError
from jwt import ExpiredSignatureError
from requests.exceptions import RequestException

from rest_framework import status
from rest_framework.response import Response

from requests.models import Response as RResponse

from core.middleware import AuthBrokerTokenIntrospectionMiddleware


@pytest.fixture()
def login_url(settings):
    settings.LOGIN_URL = "/login-url/"
    return settings.LOGIN_URL


@mock.patch("core.middleware.cache")
def test_sso_introspection_middleware_success(
    mock_cache,
    rf,
    settings,
):
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
    instance = AuthBrokerTokenIntrospectionMiddleware(get_response)
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
def test_sso_introspection_middleware_request_error(mock_cache, status_code, rf, login_url):
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
    instance = AuthBrokerTokenIntrospectionMiddleware(get_response)
    response = instance(request)
    assert response.status_code == status.HTTP_302_FOUND
    assert response.url == login_url


@pytest.mark.parametrize(
    "exception_class",
    (
        OAuth2Error,
        OAuthError,
        RequestException,
        ExpiredSignatureError,
    ),
)
@mock.patch("core.middleware.cache")
def test_sso_introspection_middleware_oauth_error(mock_cache, rf, login_url, exception_class):
    # Set up mock request and response
    request = rf.get("/")
    request.authbroker_client = mock.Mock()
    request.authbroker_client.token = {"access_token": "test"}
    request.session = mock.Mock()
    get_response = mock.Mock(return_value=Response())
    # Set up mock SSO response
    request.authbroker_client.get = mock.Mock(side_effect=exception_class())
    # Mock cache
    mock_cache.get = mock.Mock(return_value=None)
    # Call the middleware
    instance = AuthBrokerTokenIntrospectionMiddleware(get_response)
    response = instance(request)
    assert response.status_code == status.HTTP_302_FOUND
    assert response.url == login_url
    request.session.flush.assert_called()


@mock.patch("core.middleware.jwt.decode")
def test_sso_introspection_middleware_expired_refresh_token(mock_decode, rf, login_url):
    access_token = "test_access_token"
    refresh_token = "test_refresh_token"

    mock_decode.side_effect = jwt.ExpiredSignatureError()

    request = rf.get("/")
    request.authbroker_client = mock.Mock()
    request.authbroker_client.token = {
        "access_token": access_token,
        "refresh_token": refresh_token,
    }
    request.session = mock.Mock()

    get_response = mock.Mock(return_value=Response())
    instance = AuthBrokerTokenIntrospectionMiddleware(get_response)
    response = instance(request)

    mock_decode.assert_has_calls(
        [
            mock.call(
                access_token,
                options={"verify_signature": False, "verify_exp": True},
            ),
            mock.call(
                refresh_token,
                options={"verify_signature": False, "verify_exp": True},
            ),
        ]
    )

    assert response.status_code == status.HTTP_302_FOUND
    assert response.url == login_url
    request.session.flush.assert_called()
