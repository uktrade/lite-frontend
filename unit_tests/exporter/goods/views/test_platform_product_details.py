import pytest

from pytest_django.asserts import assertTemplateUsed

from django.urls import reverse

from core import client


@pytest.fixture(autouse=True)
def default_feature_flags(settings):
    settings.FEATURE_FLAG_NON_FIREARMS_PLATFORM_ENABLED = True


@pytest.fixture
def platform_product_details_url(good_id):
    return reverse(
        "goods:platform_detail",
        kwargs={
            "pk": good_id,
        },
    )


@pytest.fixture
def mock_good_get(requests_mock, data_standard_case):
    good = data_standard_case["case"]["data"]["goods"][0]
    good["good"]["item_category"].update({"key": "group1_platform", "value": "Platform, vehicle, system or machine"})

    url = client._build_absolute_uri(f'/goods/{good["good"]["id"]}/')
    return requests_mock.get(url=url, json=good)


def test_platform_product_details_template_used(
    authorized_client,
    platform_product_details_url,
    mock_good_get,
):
    response = authorized_client.get(platform_product_details_url)
    assert response.status_code == 200
    assertTemplateUsed("goods/product-details.html")


def test_platform_product_details_context(
    authorized_client,
    platform_product_details_url,
    mock_good_get,
    platform_summary,
):

    response = authorized_client.get(platform_product_details_url)
    assert response.status_code == 200
    assert response.context["summary"] == platform_summary
