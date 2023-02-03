import pytest
import re

from django.urls import reverse

from core import client

REPORT_SUMMARY_PREFIXES = "report_summary_prefixes"

prefix_data = [
    {"id": "b0849a92-4611-4e5b-b076-03562b138fb5", "name": "components for"},  # /PS-IGNORE
    {"id": "76c33f3f-1da8-4fde-b259-ada269b43d34", "name": "counter-countermeasure equipment for"},  # /PS-IGNORE
    {"id": "a4bb3d4d-1f6b-46a3-83fa-97a952fdd2c4", "name": "launching vehicles for"},  # /PS-IGNORE
]


@pytest.fixture
def prefix_json_url():
    return reverse("report_summary:prefix")


@pytest.fixture
def mock_prefixes_get(requests_mock):
    return requests_mock.get("/static/report_summary/prefixes/", json={REPORT_SUMMARY_PREFIXES: prefix_data})


def test_prefixes_json_view(authorized_client, prefix_json_url, mock_prefixes_get):
    response = authorized_client.get(prefix_json_url)

    assert response.status_code == 200

    data = response.json()
    assert REPORT_SUMMARY_PREFIXES in data
    prefixes = data[REPORT_SUMMARY_PREFIXES]
    assert len(prefixes) == 3

    for item in prefixes:
        assert item in prefix_data


def test_prefix_json_view_permission_not_required(
    authorized_client,
    prefix_json_url,
    mock_prefixes_get,
    mock_gov_user,
    requests_mock,
    gov_uk_user_id,
):
    mock_gov_user["user"]["role"]["permissions"] = []

    url = client._build_absolute_uri("/gov-users/")
    requests_mock.get(url=f"{url}me/", json=mock_gov_user)
    requests_mock.get(url=re.compile(f"{url}{gov_uk_user_id}/"), json=mock_gov_user)

    response = authorized_client.get(prefix_json_url)
    assert response.status_code == 200
