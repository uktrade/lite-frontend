import functools
from urllib.parse import urljoin

from django.shortcuts import redirect
from django.urls import reverse
from django.conf import settings

from requests_oauthlib import OAuth2Session

PROFILE_URL = urljoin(settings.AUTHBROKER_URL, "/api/v1/user/me/")
INTROSPECT_URL = urljoin(settings.AUTHBROKER_URL, "o/introspect/")
TOKEN_CHECK_PERIOD_SECONDS = 60


def get_profile(client):
    response = client.get(PROFILE_URL)  # .json()
    return response.json()
