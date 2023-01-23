import pytest
from bs4 import BeautifulSoup
from django.urls import reverse

from core import client


@pytest.fixture(autouse=True)
def setup(
    mock_queue,
    mock_denial_reasons,
    mock_application_good_documents,
):
    yield


@pytest.fixture
def url(data_standard_case):
    return reverse(
        "cases:advice_view",
        kwargs={"queue_pk": "566fd526-bd6d-40c1-94bd-60d10c967cf7", "pk": data_standard_case["case"]["id"]},
    )


def setup_mock_api(requests_mock, data):
    application_id = data["case"]["id"]
    requests_mock.get(client._build_absolute_uri(f"/cases/{application_id}"), json=data)


def test_advice_view_shows_no_assessed_trigger_list_goods_if_some_are_not_assessed(
    authorized_client,
    requests_mock,
    url,
    data_standard_case_with_potential_trigger_list_product,
    mock_gov_beis_nuclear_user,
):
    setup_mock_api(requests_mock, data_standard_case_with_potential_trigger_list_product)

    response = authorized_client.get(url)

    assert response.status_code == 200

    soup = BeautifulSoup(response.content, "html.parser")
    product_table = soup.find(id="assessed-products")
    assert product_table is None


def test_advice_view_shows_assessed_trigger_list_goods_if_all_are_assessed(
    authorized_client,
    requests_mock,
    url,
    data_standard_case_with_all_trigger_list_products_assessed,
    mock_gov_beis_nuclear_user,
):
    data = data_standard_case_with_all_trigger_list_products_assessed
    setup_mock_api(requests_mock, data)

    response = authorized_client.get(url)

    assert response.status_code == 200

    soup = BeautifulSoup(response.content, "html.parser")
    product_table = soup.find(id="assessed-products")
    assert product_table is not None

    rows = product_table.tbody.find_all("tr")
    assert len(rows) == len(data["case"]["data"]["goods"])
