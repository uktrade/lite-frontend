from urllib.parse import urljoin

from django.conf import settings
from django.urls import reverse
from requests_oauthlib import OAuth2Session

PROFILE_URL = urljoin(settings.AUTHBROKER_URL, "sso/oauth2/user-profile/v1/")


def get_client(request, **kwargs):
    return OAuth2Session(
        settings.AUTHBROKER_CLIENT_ID,
        redirect_uri=request.build_absolute_uri(reverse("auth:callback")),
        scope=settings.AUTHBROKER_SCOPE,
        token=request.session.get(settings.TOKEN_SESSION_KEY, None),
        **kwargs,
    )


def get_profile(client):
    response = client.get(settings.AUTHBROKER_PROFILE_URL)  # .json()
    return response.json()
