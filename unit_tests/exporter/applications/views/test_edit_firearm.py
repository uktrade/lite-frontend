import pytest

from django.urls import reverse

from core import client


@pytest.fixture
def mock_good_get(requests_mock, data_standard_case):
    good = data_standard_case["case"]["data"]["goods"][0]
    url = client._build_absolute_uri(f'/goods/{good["good"]["id"]}/')
    yield requests_mock.get(url=url, json=good)


@pytest.fixture
def mock_good_put(requests_mock, data_standard_case):
    good = data_standard_case["case"]["data"]["goods"][0]["good"]
    url = client._build_absolute_uri(f'/goods/{good["id"]}/')
    yield requests_mock.put(url=url, json={})


@pytest.fixture(autouse=True)
def setup(mock_good_get, mock_good_put):
    pass


def test_edit_firearm_category(authorized_client, data_standard_case, requests_mock):
    application_id = data_standard_case["case"]["data"]["id"]
    good = data_standard_case["case"]["data"]["goods"][0]["good"]
    url = reverse("applications:firearm_edit_category", kwargs={"pk": application_id, "good_pk": good["id"]})

    response = authorized_client.post(
        url,
        data={
            "category": ["NON_AUTOMATIC_SHOTGUN", "NON_AUTOMATIC_RIM_FIRED_HANDGUN"],
        },
    )

    assert response.status_code == 302
    assert requests_mock.last_request.json() == {
        "item_category": "group2_firearms",
        "firearm_details": {"category": ["NON_AUTOMATIC_SHOTGUN", "NON_AUTOMATIC_RIM_FIRED_HANDGUN"]},
    }
