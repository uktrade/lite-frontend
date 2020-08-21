import functools
from urllib.parse import urljoin

from django.conf import settings
from django.shortcuts import redirect
from django.urls import reverse
from requests_oauthlib import OAuth2Session

PROFILE_URL = urljoin(settings.AUTHBROKER_URL, "sso/oauth2/user-profile/v1/")
INTROSPECT_URL = urljoin(settings.AUTHBROKER_URL, "sso/oauth2/introspect/")
TOKEN_URL = urljoin(settings.AUTHBROKER_URL, "sso/oauth2/token/")
AUTHORISATION_URL = urljoin(settings.AUTHBROKER_URL, "sso/oauth2/authorize/")
TOKEN_CHECK_PERIOD_SECONDS = 60


from requests_oauthlib import OAuth2Session


def get_client(request, **kwargs):
    return OAuth2Session(
        settings.AUTHBROKER_CLIENT_ID,
        redirect_uri=request.build_absolute_uri(reverse("auth:callback")),
        scope=settings.AUTHBROKER_SCOPE,
        token=request.session.get(settings.TOKEN_SESSION_KEY, None),
        **kwargs,
    )
