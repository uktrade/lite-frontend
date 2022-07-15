import pytest

from pytest_django.asserts import assertTemplateUsed

from django.urls import reverse


@pytest.fixture(autouse=True)
def default_feature_flag(settings):
    settings.FEATURE_FLAG_PRODUCT_SEARCH = True


@pytest.fixture
def product_search_url():
    return reverse("search:products")


def test_product_search_disabled_feature_flag(
    authorized_client,
    product_search_url,
    settings,
):
    settings.FEATURE_FLAG_PRODUCT_SEARCH = False
    response = authorized_client.get(product_search_url)
    assert response.status_code == 404


def test_product_search_enabled_feature_flag(authorized_client, product_search_url):
    response = authorized_client.get(product_search_url)
    assert response.status_code == 200


def test_product_search_renders_template(authorized_client, product_search_url):
    response = authorized_client.get(product_search_url)
    assertTemplateUsed(response, "search/products.html")
    assertTemplateUsed(response, "layouts/base.html")
