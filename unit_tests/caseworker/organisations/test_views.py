import pytest
from copy import deepcopy
from uuid import UUID

from django.urls import reverse

from core import client
from lite_forms.helpers import flatten_data


@pytest.fixture(scope="function")
def organisation():
    return {
        "form_pk": 1,
        "name": "regional site",
        "type": "commercial",
        "location": "united_kingdom",
        "eori_number": "123456789AA",
        "sic_number": "2345",
        "vat_number": "GB123456789",
        "registration_number": "897654",
        "phone_number": "+441234567890",
        "website": "",
        "site": {
            "name": "Headquarters",
            "address": {
                "address_line_1": "42 Industrial Estate",
                "address_line_2": "Queens Road",
                "region": "Hertfordshire",
                "postcode": "AL1 4GT",
                "city": "St Albans",
            },
        },
        "user": {"email": "john@smith.com"},
    }


@pytest.fixture(scope="function")
def retrieved_organisation():
    return {
        "id": "b985b6d0-7d04-4351-ad6a-c7e51d3a3bad",
        "documents": [],
        "type": {"key": "commercial", "value": "Commercial Organisation"},
        "created_at": "2020-02-20T10:24:47.217470Z",
        "updated_at": "2020-06-03T14:40:47.123401+01:00",
        "name": "Archway Communications",
        "eori_number": "1234567890AAA",
        "sic_number": "2345",
        "vat_number": "GB123456789",
        "registration_number": "09876543",
        "phone_number": "+447234517890",
        "website": "",
        "primary_site": {
            "id": "858b324e-9d59-4571-ac7a-01950b5b2ce7",
            "name": "Headquarters",
            "address": {
                "id": "9a2223b3-1a58-4cf1-a97d-d5a3f5a99b2e",
                "address_line_1": "42 Question Road",
                "address_line_2": "",
                "city": "London",
                "region": "London",
                "postcode": "Islington",
                "country": {"id": "GB", "name": "United Kingdom", "type": "gov.uk Country", "is_eu": "True"},
            },
        },
    }


def test_register_organisation_success(authorized_client, requests_mock, organisation):
    requests_mock.get(client._build_absolute_uri("/static/countries/"), json={"countries": []})
    requests_mock_instance = requests_mock.post(client._build_absolute_uri("/organisations/"), json={})

    url = reverse("organisations:register")
    response = authorized_client.post(url, data=flatten_data(organisation))
    assert response.status_code == 200

    expected = deepcopy(organisation)
    expected.pop("form_pk")
    assert requests_mock_instance.call_count == 1
    assert requests_mock_instance.request_history[0].json() == {**expected}
    assert response.context["errors"] is None


def test_register_organisation_missing_location(authorized_client, requests_mock, organisation):
    requests_mock.get(client._build_absolute_uri("/static/countries/"), json={"countries": []})
    requests_mock_instance = requests_mock.post(client._build_absolute_uri("/organisations/"), json={})

    data = organisation
    data.pop("location")

    url = reverse("organisations:register")
    response = authorized_client.post(url, data=data)
    assert response.status_code == 200
    expected = {"location": ["Select a location"]}
    assert response.context["errors"] == expected
    assert requests_mock_instance.call_count == 0
    assert requests_mock_instance.request_history == []


def test_edit_organisation_success(authorized_client, requests_mock, organisation, retrieved_organisation):
    organisation_id = UUID("b985b6d0-7d04-4351-ad6a-c7e51d3a3bad")
    requests_mock.get(client._build_absolute_uri("/static/countries/"), json={"countries": []})
    requests_mock.get(client._build_absolute_uri(f"/organisations/{organisation_id}/"), json=retrieved_organisation)
    requests_mock.get(client._build_absolute_uri(f"/organisations/{organisation_id}/activity"), json={"activity": {}})
    requests_mock_instance = requests_mock.put(
        client._build_absolute_uri(f"/organisations/{organisation_id}/"), json=retrieved_organisation
    )

    url = reverse("organisations:organisation", kwargs={"pk": organisation_id})
    edit_url = reverse("organisations:edit-address", kwargs={"pk": organisation_id})
    response = authorized_client.get(url)
    assert response.status_code == 200

    response = authorized_client.post(edit_url, data=flatten_data(retrieved_organisation))
    assert response.status_code == 302
    expected = deepcopy(retrieved_organisation)
    expected.pop("documents")
    assert requests_mock_instance.call_count == 1
    assert requests_mock_instance.request_history[0].json() == {**expected}
