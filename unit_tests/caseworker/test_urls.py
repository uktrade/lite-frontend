from uuid import uuid4

import pytest

from django.urls import reverse, NoReverseMatch

from unit_tests.helpers import reload_urlconf

CASEWORKER_MOCK_URL_NAMES = [
    "mock_sso:authorize",
    "mock_sso:token",
    "mock_sso:api_user_me",
]


def test_mock_sso_enabled_endpoints(settings):
    settings.MOCK_SSO_ACTIVATE_ENDPOINTS = True
    reload_urlconf(["caseworker.urls", settings.ROOT_URLCONF])

    for url_name in CASEWORKER_MOCK_URL_NAMES:
        reverse(url_name)


def test_mock_sso_disabled_endpoints(settings):
    settings.MOCK_SSO_ACTIVATE_ENDPOINTS = False
    reload_urlconf(["caseworker.urls", settings.ROOT_URLCONF])

    for url_name in CASEWORKER_MOCK_URL_NAMES:
        with pytest.raises(NoReverseMatch):
            reverse(url_name)
