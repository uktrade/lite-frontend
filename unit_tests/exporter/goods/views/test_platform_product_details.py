import pytest

from pytest_django.asserts import assertTemplateUsed

from django.urls import reverse

from core import client
from core.constants import ProductCategories


@pytest.fixture(autouse=True)
def default_feature_flags(settings):
    settings.FEATURE_FLAG_NON_FIREARMS_PLATFORM_ENABLED = True
    settings.FEATURE_C7_NCSC_ENABLED = True


@pytest.fixture
def complete_item_product_details_url(good_id):
    return reverse(
        "goods:complete_item_detail",
        kwargs={
            "pk": good_id,
        },
    )


@pytest.fixture
def mock_good_get(requests_mock, data_standard_case):
    good = data_standard_case["case"]["data"]["goods"][0]
    good["good"].update(
        {
            "item_category": {
                "key": ProductCategories.PRODUCT_CATEGORY_COMPLETE_ITEM,
            },
        },
    )
    del good["good"]["firearm_details"]

    url = client._build_absolute_uri(f'/goods/{good["good"]["id"]}/')
    return requests_mock.get(url=url, json=good)


def test_complete_item_product_details_status_code(
    authorized_client,
    complete_item_product_details_url,
    mock_good_get,
):
    response = authorized_client.get(complete_item_product_details_url)
    assert response.status_code == 200


def test_complete_item_product_details_template_used(
    authorized_client,
    complete_item_product_details_url,
    mock_good_get,
):
    response = authorized_client.get(complete_item_product_details_url)
    assertTemplateUsed(response, "goods/product-details.html")


def test_complete_item_product_details_context(
    authorized_client,
    complete_item_product_details_url,
    mock_good_get,
    complete_item_summary,
):

    response = authorized_client.get(complete_item_product_details_url)
    assert response.status_code == 200
    assert response.context["summary"] == complete_item_summary
