from django.conf import settings
from django.urls import reverse
from authlib.integrations.requests_client import OAuth2Session
from requests.exceptions import HTTPError


def get_client(request, **kwargs):

    return OAuth2Session(
        client_id=settings.AUTHBROKER_CLIENT_ID,
        client_secret=settings.AUTHBROKER_CLIENT_SECRET,
        redirect_uri=request.build_absolute_uri(reverse("auth:callback")),
        scope=settings.AUTHBROKER_SCOPE,
        token=request.session.get(settings.TOKEN_SESSION_KEY, None),
        **kwargs,
    )


def get_profile(client):
    try:
        response = client.get(settings.AUTHBROKER_PROFILE_URL)
        response.raise_for_status()
    except HTTPError as ex:
        raise ex
    return response.json()
