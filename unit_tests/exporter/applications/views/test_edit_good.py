import pytest
from django.urls import reverse


@pytest.fixture(autouse=True)
def setup(mock_good_get, mock_good_put, mock_control_list_entries_get, settings):
    settings.FEATURE_FLAG_PRODUCT_2_0 = True


def test_edit_good_name(authorized_client, data_standard_case, requests_mock):
    application_id = data_standard_case["case"]["data"]["id"]
    good = data_standard_case["case"]["data"]["goods"][0]["good"]
    url = reverse("applications:firearm_edit_name", kwargs={"pk": application_id, "good_pk": good["id"]})

    response = authorized_client.post(
        url,
        data={"name": "new good"},
    )

    assert response.status_code == 302
    assert requests_mock.last_request.json() == {"name": "new good"}


@pytest.mark.parametrize(
    "data, expected",
    (
        (
            {
                "is_good_controlled": False,
            },
            {"is_good_controlled": False, "control_list_entries": []},
        ),
        (
            {"is_good_controlled": True, "control_list_entries": ["ML1a", "ML22b"]},
            {"is_good_controlled": True, "control_list_entries": ["ML1a", "ML22b"]},
        ),
    ),
)
def test_edit_good_control_list_entry_options(authorized_client, data_standard_case, requests_mock, data, expected):
    application_id = data_standard_case["case"]["data"]["id"]
    good = data_standard_case["case"]["data"]["goods"][0]["good"]
    url = reverse(
        "applications:firearm_edit_control_list_entries", kwargs={"pk": application_id, "good_pk": good["id"]}
    )

    response = authorized_client.post(url, data=data)

    assert response.status_code == 302
    assert requests_mock.last_request.json() == expected
