import time
import logging
import requests
from urllib.parse import urlparse
import jwt
from authlib.oauth2 import OAuth2Error
from authlib.integrations.base_client.errors import OAuthError
from authlib.oauth2.rfc7523 import PrivateKeyJWT
from requests.exceptions import RequestException
from .ip_filter import get_client_ip

from django.conf import settings
from django.contrib.auth import logout
from django.core.cache import cache
from django.shortcuts import redirect
from django.utils.cache import add_never_cache_headers
from django.http import HttpResponseForbidden

from core.file_handler import UploadFailed
from lite_forms.generators import error_page
from json import JSONDecodeError

SESSION_TIMEOUT_KEY = "_session_timeout_seconds_"
logger = logging.getLogger(__name__)


class UploadFailedMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return response

    def process_exception(self, request, exception):
        if not isinstance(exception, UploadFailed):
            return None

        return error_page(
            request,
            exception.message,
        )


class SessionTimeoutMiddleware:
    def __init__(self, get_response=None):
        self.get_response = get_response

    def __call__(self, request):
        start = request.session.get(SESSION_TIMEOUT_KEY, time.time())

        timeout = settings.SESSION_EXPIRE_SECONDS

        end = time.time()

        # Expire the session if more than start time + timeout time has occurred
        if end - start > timeout:
            logger.info(
                "Session timeout force logout user: %s client_ip: %s",
                request.session.get("lite_api_user_id"),
                get_client_ip(request),
            )
            request.session.flush()
            logout(request)
            return redirect(settings.LOGIN_URL)

        request.session[SESSION_TIMEOUT_KEY] = end

        return self.get_response(request)


class RequestsSessionMiddleware:
    def __init__(self, get_response=None):
        self.get_response = get_response

    def __call__(self, request):
        # when making several requests to the same host, the underlying TCP connection will be reused, which can result
        # in a significant performance increase
        request.requests_session = requests.Session()
        return self.get_response(request)


class NoCacheMiddleware:
    """Tell the browser to not cache the pages, because otherwise information that should be kept private can be
    viewed by anyone with access to the files in the browser's cache directory.

    """

    def __init__(self, get_response=None):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        add_never_cache_headers(response)
        return response


class ValidateReturnToMiddleware:
    """We are using return_to parameter to override the backlink in the
    application journey. We need to validate if the return_to parameter is
    (1) a valid URL and (2) a relative URL.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        return_to = request.GET.get("return_to", None)
        if return_to is not None:
            try:
                url = urlparse(return_to)
            except ValueError:
                return HttpResponseForbidden("Unparseable return_to parameter")
            if url.netloc != "" or url.scheme != "" or return_to.startswith("//"):
                return HttpResponseForbidden("Invalid return_to parameter")
        response = self.get_response(request)
        return response


class AuthBrokerTokenIntrospectionMiddleware:
    """Introspect tokens to ensure that a user cannot continue to access LITE
    if their account is deleted from the sso service.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def get_token(self, request):
        is_new_token = False
        token = request.authbroker_client.token.get("access_token")
        try:
            logger.info(
                "Authentication:Service: Introspecting SSO decoding checking token: %s client_ip: %s",
                request.session.get("lite_api_user_id"),
                get_client_ip(request),
            )
            jwt.decode(token, options={"verify_signature": False, "verify_exp": True})
        except jwt.ExpiredSignatureError:
            # Token expired lets get a new one using refresh token
            # We making a big assumption here assuming client uses openid PrivateJWT auth method
            try:
                logger.info(
                    "Authentication:Service: Introspecting SSO decoding checking refresh token: %s client_ip: %s",
                    request.session.get("lite_api_user_id"),
                    get_client_ip(request),
                )
                refresh_token = request.authbroker_client.token.get("refresh_token")
                jwt.decode(refresh_token, options={"verify_signature": False, "verify_exp": True})
                logger.info(
                    "Authentication:Service: Introspecting SSO attempt token refresh: %s client_ip: %s",
                    request.session.get("lite_api_user_id"),
                    get_client_ip(request),
                )
                request.authbroker_client.token_endpoint_auth_method = PrivateKeyJWT(
                    token_endpoint=settings.AUTHBROKER_TOKEN_URL
                )

                new_jwt_token = request.authbroker_client.refresh_token(
                    url=settings.AUTHBROKER_TOKEN_URL,
                    code=request.session[f"{settings.TOKEN_SESSION_KEY}_auth_code"],
                    client_id=settings.AUTHBROKER_CLIENT_ID,
                )

                token = new_jwt_token.get("access_token")
                request.session[settings.TOKEN_SESSION_KEY] = dict(new_jwt_token)
                is_new_token = True
            except jwt.ExpiredSignatureError:
                logger.warning(
                    "Authentication:Service: Introspecting SSO refresh token expired: %s client_ip: %s",
                    request.session.get("lite_api_user_id"),
                    get_client_ip(request),
                    exc_info=True,
                )
                raise
        except jwt.DecodeError:
            # The client doesn't have the correct support for full JWT we will return the original token
            pass
        return token, is_new_token

    def client_introspect_call(self, request):
        logger.info(
            "Authentication:Service: Introspecting with SSO: %s client_ip: %s",
            request.session.get("lite_api_user_id"),
            get_client_ip(request),
        )
        response = request.authbroker_client.get(settings.AUTHBROKER_PROFILE_URL)
        response.raise_for_status()

    def introspect(self, request):
        # If refresh tokens are supported we will only return valid tokens here this to stop the call to the client
        # from failing because of short lived tokens
        token, is_new_token = self.get_token(request)
        cache_key = f"sso_introspection:{token}"
        cache_value = cache.get(cache_key)
        if cache_value is not None:
            return
        if not is_new_token:
            # This is to prevent another client call if only just received a new token
            self.client_introspect_call(request)

        logger.info(
            "Authentication:Service: Introspecting SSO set new cache key: %s client_ip: %s",
            request.session.get("lite_api_user_id"),
            get_client_ip(request),
        )
        ttl = settings.AUTHBROKER_TOKEN_INTROSPECTION_TTL
        cache.set(cache_key, True, timeout=ttl)

    def __call__(self, request):
        # It is important to NOT run this middleware
        # when a user has not been authenticated.
        if not request.authbroker_client.token:
            return self.get_response(request)
        try:
            self.introspect(request)
        except (OAuth2Error, OAuthError, RequestException, jwt.ExpiredSignatureError) as e:
            logger.warning(
                "Authentication:Service: Introspecting with SSO failed for user %s: :%s : %s",
                request.session.get("lite_api_user_id"),
                get_client_ip(request),
                str(e),
            )

            request.session.flush()
            return redirect(settings.LOGIN_URL)
        return self.get_response(request)


class XRobotsTagMiddleware:
    """Adds X-Robots-Tag"""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        response["X-Robots-Tag"] = ",".join(["noindex", "nofollow"])
        return response


class HttpErrorHandlerMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return response

    def process_exception(self, request, exception):
        if isinstance(exception, requests.HTTPError):
            logger.info(exception.response.text)
            try:
                description = exception.response.json().get("errors")
                if description:
                    return error_page(request, description)
            # AttributeError is to catch text is json serializable
            except (JSONDecodeError, AttributeError):
                pass
        return None
