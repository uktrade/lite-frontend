import functools
from urllib.parse import urljoin

from django.conf import settings
from django.shortcuts import redirect
from django.urls import reverse
from requests_oauthlib import OAuth2Session

from core.auth.utils import get_client

PROFILE_URL = urljoin(settings.AUTHBROKER_URL, "sso/oauth2/user-profile/v1/")
INTROSPECT_URL = urljoin(settings.AUTHBROKER_URL, "sso/oauth2/introspect/")
TOKEN_CHECK_PERIOD_SECONDS = 60


def get_profile(client):
    return client.get(PROFILE_URL).json()


def authbroker_login_required(func):
    """Check that the current session has authenticated with the authbroker and has a valid token.
    This is different to the @login_required decorator in that it only checks for a valid authbroker Oauth2 token,
    not an authenticated django user."""

    @functools.wraps(func)
    def decorated(request):
        if not get_client(request).authorized:
            return redirect("auth:login")

        return func(request)

    return decorated
