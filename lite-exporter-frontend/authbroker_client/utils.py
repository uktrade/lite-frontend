import functools
from urllib.parse import urljoin

from django.conf import settings
from django.shortcuts import redirect
from django.urls import reverse

from requests_oauthlib import OAuth2Session


TOKEN_SESSION_KEY = '_authbroker_token'
PROFILE_URL = urljoin(settings.AUTHBROKER_URL, 'sso/oauth2/user-profile/v1/')
INTROSPECT_URL = urljoin(settings.AUTHBROKER_URL, 'sso/oauth2/introspect/')
TOKEN_URL = urljoin(settings.AUTHBROKER_URL, 'sso/oauth2/token/')
AUTHORISATION_URL = urljoin(settings.AUTHBROKER_URL, 'sso/oauth2/authorize/')
TOKEN_CHECK_PERIOD_SECONDS = 60
SCOPE = 'profile'


def get_client(request, **kwargs):
    callback_url = reverse('authbroker_client:callback')
    redirect_uri = request.build_absolute_uri(callback_url)

    return OAuth2Session(
        settings.AUTHBROKER_CLIENT_ID,
        redirect_uri=redirect_uri,
        scope=SCOPE,
        token=request.session.get(TOKEN_SESSION_KEY, None),
        **kwargs)


def has_valid_token(client):
    """Does the session have a valid token?"""

    return client.authorized


def get_profile(client):
    return client.get(PROFILE_URL).json()


def authbroker_login_required(func):
    """Check that the current session has authenticated with the authbroker and has a valid token.
    This is different to the @login_required decorator in that it only checks for a valid authbroker Oauth2 token,
    not an authenticated django user."""

    @functools.wraps(func)
    def decorated(request):
        if not has_valid_token(get_client(request)):
            return redirect('authbroker:login')

        return func(request)
    return decorated
