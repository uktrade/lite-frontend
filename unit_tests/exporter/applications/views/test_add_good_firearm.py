import pytest

from django.urls import reverse

from core import client
from exporter.core.constants import AddGoodFormSteps


@pytest.fixture
def new_good_firearm_url(data_standard_case):
    return reverse(
        "applications:new_good_firearm",
        kwargs={
            "pk": data_standard_case["case"]["id"],
        },
    )


def test_firearm_category_redirects_to_new_wizard(
    settings, authorized_client, requests_mock, data_standard_case, new_good_firearm_url
):
    settings.FEATURE_FLAG_ONLY_ALLOW_FIREARMS_PRODUCTS = True
    settings.FEATURE_FLAG_PRODUCT_2_0 = True

    app_url = client._build_absolute_uri(f"/applications/{data_standard_case['case']['id']}/")
    requests_mock.get(url=app_url, json=data_standard_case["case"])

    clc_url = client._build_absolute_uri("/static/control-list-entries/")
    requests_mock.get(url=clc_url, json={"control_list_entries": [{"rating": "ML1"}, {"rating": "ML1a"}]})

    url = reverse("applications:new_good", kwargs={"pk": data_standard_case["case"]["id"]})

    response = authorized_client.post(url, data={"wizard_goto_step": AddGoodFormSteps.GROUP_TWO_PRODUCT_TYPE})
    response = authorized_client.post(
        url,
        data={
            f"add_good-current_step": AddGoodFormSteps.GROUP_TWO_PRODUCT_TYPE,
            f"{AddGoodFormSteps.GROUP_TWO_PRODUCT_TYPE}-type": "firearms",
        },
    )

    assert response.status_code == 302
    assert response.url == new_good_firearm_url


def test_new_good_firearm_view(authorized_client, new_good_firearm_url):
    response = authorized_client.get(new_good_firearm_url)
    assert response.status_code == 200
