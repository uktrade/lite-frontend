import pytest

from django.urls import reverse

from unit_tests.helpers import reload_urlconf
from spire import helpers


@pytest.fixture(autouse=True)
def mock_spire_application_get(requests_mock):
    data = {
        "results": [],
        "count": 0,
    }
    requests_mock.get(url=helpers.URL_APPLICATION, json=data)
    yield data


@pytest.mark.django_db
def test_feature_flag_on(settings, client, user):
    client.force_login(user)

    # given the feature flag is enabled
    settings.FEATURE_SPIRE_SEARCH_ON = True
    reload_urlconf()

    # when the spire page is requested
    response = client.get(reverse("spire:application-search"))

    # then it will be served
    assert response.status_code == 200


@pytest.mark.django_db
def test_feature_flag_off(settings, client, user):
    # enabling the feature to allow generating the url
    settings.FEATURE_SPIRE_SEARCH_ON = True
    reload_urlconf()
    url = reverse("spire:application-search")

    # given the feature flag is disabled
    settings.FEATURE_SPIRE_SEARCH_ON = False
    reload_urlconf()

    # when the spire page is requested
    response = client.get(url)

    # then it will not be served
    assert response.status_code == 404
