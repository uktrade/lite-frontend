import pytest
from django.urls import reverse


@pytest.fixture(autouse=True)
def setup(mock_good_get, mock_good_put, settings):
    settings.FEATURE_FLAG_PRODUCT_2_0 = True


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
        "firearm_details": {"category": ["NON_AUTOMATIC_SHOTGUN", "NON_AUTOMATIC_RIM_FIRED_HANDGUN"]},
    }
