from django.urls import reverse
from urllib.parse import urlsplit, parse_qs
import pytest


@pytest.mark.parametrize(
    "low_security, value",
    (
        (True, ["['Cl']"]),
        (False, None),
    ),
)
def test_logged_in_call_back_low_security(low_security, value, client, settings):
    settings.AUTHBROKER_LOW_SECURITY = low_security
    url = reverse("auth:login")
    response = client.get(url)
    assert response.status_code == 302
    query = urlsplit(response.url).query
    params = parse_qs(query)
    assert params.get("vtr") == value
