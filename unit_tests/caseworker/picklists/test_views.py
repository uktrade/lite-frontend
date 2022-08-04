import pytest
import re

from django.urls import reverse

from core import client


@pytest.fixture
def picklists_json_url():
    return reverse("picklists:picklists_json")


@pytest.fixture
def mock_picklist_get(requests_mock):
    return requests_mock.get("/picklist/", json={"results": []})


def test_picklist_json_view(authorized_client, picklists_json_url, mock_picklist_get):
    response = authorized_client.get(picklists_json_url)
    assert response.status_code == 200
    assert mock_picklist_get.last_request.qs == {
        "type": ["proviso"],
        "page": ["1"],
        "disable_pagination": ["false"],
        "show_deactivated": ["false"],
    }


def test_picklist_json_view_permission_not_required(
    authorized_client,
    picklists_json_url,
    mock_picklist_get,
    mock_gov_user,
    requests_mock,
    gov_uk_user_id,
):
    mock_gov_user["user"]["role"]["permissions"] = []

    url = client._build_absolute_uri("/gov-users/")
    requests_mock.get(url=f"{url}me/", json=mock_gov_user)
    requests_mock.get(url=re.compile(f"{url}{gov_uk_user_id}/"), json=mock_gov_user)

    response = authorized_client.get(picklists_json_url)
    assert response.status_code == 200
