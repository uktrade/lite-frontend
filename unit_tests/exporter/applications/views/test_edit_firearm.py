import pytest
from django.urls import reverse


@pytest.fixture(autouse=True)
def setup(mock_good_get, mock_good_put, settings):
    settings.FEATURE_FLAG_PRODUCT_2_0 = True


@pytest.mark.parametrize(
    "url_name, form_data",
    (
        (
            "firearm_edit_category",
            {
                "category": ["NON_AUTOMATIC_SHOTGUN", "NON_AUTOMATIC_RIM_FIRED_HANDGUN"],
            },
        ),
        (
            "firearm_edit_calibre",
            {
                "calibre": "2",
            },
        ),
    ),
)
def test_edit_firearm(authorized_client, data_standard_case, requests_mock, url_name, form_data):
    application_id = data_standard_case["case"]["data"]["id"]
    good = data_standard_case["case"]["data"]["goods"][0]["good"]
    url = reverse(f"applications:{url_name}", kwargs={"pk": application_id, "good_pk": good["id"]})

    response = authorized_client.post(
        url,
        data=form_data,
    )

    assert response.status_code == 302
    assert requests_mock.last_request.json() == {
        "firearm_details": form_data,
    }
