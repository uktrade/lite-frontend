from copy import deepcopy
import pytest
from django.urls import reverse

from core import client


@pytest.fixture(autouse=True)
def setup(mock_get_application):
    yield


def test_locations_summary_no_data_redirect_to_form(data_draft_standard_application, authorized_client):
    url = reverse("applications:location", kwargs={"pk": data_draft_standard_application["id"]})
    response = authorized_client.get(url)
    assert response.status_code == 302
    assert response.url == reverse("applications:edit_location", kwargs={"pk": data_draft_standard_application["id"]})


def test_locations_summary_old_locations(data_draft_standard_application, authorized_client, requests_mock):
    application_url = client._build_absolute_uri(f"/applications/{data_draft_standard_application['id']}/")
    application = deepcopy(data_draft_standard_application)
    application["goods_locations"] = {
        "type": "external_locations",
        "data": [
            {
                "id": "149edce6-529e-41c1-a4b3-48df06bfe5a1",
                "name": "44",
                "address": "44",
                "country": {"id": "BN", "name": "Brunei", "type": "gov.uk Country", "is_eu": False},
                "organisation": "b7175103-d0ae-4b59-9c6a-190a2ed7f5e7",
            }
        ],
    }

    requests_mock.get(url=application_url, json=application)
    url = reverse("applications:location", kwargs={"pk": data_draft_standard_application["id"]})
    response = authorized_client.get(url)

    assert response.status_code == 200


def test_locations_summary_new_locations(data_draft_standard_application, authorized_client, requests_mock):
    application_url = client._build_absolute_uri(f"/applications/{data_draft_standard_application['id']}/")
    application = deepcopy(data_draft_standard_application)
    application["goods_recipients"] = "direct_to_end_user"
    application["goods_starting_point"] = "GB"
    application["export_type"] = "permanent"
    application["is_shipped_waybill_or_lading"] = True

    requests_mock.get(url=application_url, json=application)
    url = reverse("applications:location", kwargs={"pk": data_draft_standard_application["id"]})
    response = authorized_client.get(url)

    assert response.status_code == 302
    summary_url = reverse("applications:locations_summary", kwargs={"pk": data_draft_standard_application["id"]})
    assert response.url == f"{summary_url}?return_to=/applications/{data_draft_standard_application['id']}/task-list/"
