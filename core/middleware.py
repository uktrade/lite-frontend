import time
import logging

import requests
from s3chunkuploader.file_handler import UploadFailed
from urllib.parse import urlparse

from django.conf import settings
from django.contrib.auth import logout
from django.core.cache import cache
from django.shortcuts import redirect
from django.utils.cache import add_never_cache_headers
from oauthlib.oauth2 import OAuth2Error
from rest_framework.response import Response
from rest_framework import status
from requests.exceptions import RequestException

from lite_content.lite_internal_frontend.strings import cases
from lite_forms.generators import error_page


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

        return error_page(request, cases.Manage.Documents.AttachDocuments.FILE_TOO_LARGE)


class SessionTimeoutMiddleware:
    def __init__(self, get_response=None):
        self.get_response = get_response

    def __call__(self, request):
        start = request.session.get(SESSION_TIMEOUT_KEY, time.time())

        timeout = settings.SESSION_EXPIRE_SECONDS

        end = time.time()

        # Expire the session if more than start time + timeout time has occurred
        if end - start > timeout:
            request.session.flush()
            logout(request)
            return redirect(settings.LOGOUT_URL)

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
            except ValueError as e:
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
            if url.netloc != "" or url.scheme != "" or return_to.startswith("//"):
                return Response({"error": "Invalid return_to parameter"}, status=status.HTTP_400_BAD_REQUEST)
        response = self.get_response(request)
        return response


class AuthBrokerTokenIntrospectionMiddleware:
    """Introspect tokens to ensure that a user cannot continue to access LITE
    if their account is deleted from the sso service.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def introspect(self, request):
        client = request.authbroker_client
        token = client.token.get("access_token", "")
        cache_key = f"sso_introspection:{token}"
        cache_value = cache.get(cache_key)
        if cache_value is not None:
            return
        logger.info("Introspecting with SSO: %s", request.session.get("lite_api_user_id"))
        response = client.get(settings.AUTHBROKER_PROFILE_URL)
        response.raise_for_status()
        ttl = settings.AUTHBROKER_TOKEN_INTROSPECTION_TTL
        cache.set(cache_key, True, timeout=ttl)

    def __call__(self, request):
        # It is important to NOT run this middleware
        # when a user has not been authenticated.
        if not request.authbroker_client.authorized:
            return self.get_response(request)
        try:
            self.introspect(request)
        except (OAuth2Error, RequestException) as e:
            logger.error(
                "Introspecting with SSO failed for user %s: %s", request.session.get("lite_api_user_id"), str(e),
            )
            request.session.flush()
            return redirect(settings.LOGOUT_URL)
        return self.get_response(request)
