import pytest
from django.urls import reverse


@pytest.fixture(autouse=True)
def setup(mock_good_get, mock_good_put, mock_control_list_entries_get, settings):
    settings.FEATURE_FLAG_PRODUCT_2_0 = True


@pytest.mark.parametrize(
    "url_name, form_data, expected",
    (
        (
            "firearm_edit_name",
            {"name": "new good"},
            {"name": "new good"},
        ),
        (
            "firearm_edit_category",
            {"category": ["NON_AUTOMATIC_SHOTGUN", "NON_AUTOMATIC_RIM_FIRED_HANDGUN"]},
            {"firearm_details": {"category": ["NON_AUTOMATIC_SHOTGUN", "NON_AUTOMATIC_RIM_FIRED_HANDGUN"]}},
        ),
        ("firearm_edit_calibre", {"calibre": "2"}, {"firearm_details": {"calibre": "2"}}),
        (
            "firearm_edit_replica",
            {"is_replica": True, "replica_description": "photocopy of real item"},
            {"firearm_details": {"is_replica": True, "replica_description": "photocopy of real item"}},
        ),
        (
            "firearm_edit_replica",
            {"is_replica": False, "replica_description": "photocopy of real item"},
            {"firearm_details": {"is_replica": False, "replica_description": ""}},
        ),
    ),
)
def test_edit_firearm(authorized_client, data_standard_case, requests_mock, url_name, form_data, expected):
    application_id = data_standard_case["case"]["data"]["id"]
    good = data_standard_case["case"]["data"]["goods"][0]["good"]
    url = reverse(f"applications:{url_name}", kwargs={"pk": application_id, "good_pk": good["id"]})

    response = authorized_client.post(
        url,
        data=form_data,
    )

    assert response.status_code == 302
    assert requests_mock.last_request.json() == expected


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
