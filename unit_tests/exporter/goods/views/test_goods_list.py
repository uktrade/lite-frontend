import pytest
import re

from bs4 import BeautifulSoup

from django.urls import reverse

from core import client


@pytest.fixture
def products_list_url():
    return reverse("goods:goods")


@pytest.fixture
def archived_products_list_url():
    return reverse("goods:archived_goods")


@pytest.fixture
def mock_products_list_get(requests_mock, data_standard_case):
    products_list = {"count": 0, "results": []}
    goods_on_application = data_standard_case["case"]["data"]["goods"]
    for good_on_application in goods_on_application:
        products_list["results"].append(good_on_application["good"])

    products_list["count"] = len(goods_on_application)

    url = client._build_absolute_uri("/goods/")
    return requests_mock.get(url=url, json=products_list)


@pytest.fixture
def mock_archived_products_list_get(requests_mock, data_standard_case):
    products_list = {"count": 0, "results": []}
    goods_on_application = data_standard_case["case"]["data"]["goods"]
    for good_on_application in goods_on_application:
        good_on_application["good"]["is_archived"] = True
        products_list["results"].append(good_on_application["good"])

    products_list["count"] = len(goods_on_application)

    url = client._build_absolute_uri("/goods/archived-goods/")
    return requests_mock.get(url=url, json=products_list)


def get_products_list_data(soup, products_table, headers):
    products_data = []

    body = products_table.find("tbody")
    rows = body.find_all("tr")

    for row in rows:
        product_line = row.text.replace("\t", "").strip()
        # replace consecutive special characters with one character
        product_line = re.sub(r"([\W_])\1+", r"\1", product_line)
        columns = {}
        for header in headers[1:]:
            start = product_line.find(header)
            column = product_line[:start].rstrip("\n")
            tokens = column.split("\n", 1)
            columns[tokens[0]] = tokens[1]
            product_line = product_line[start:]

        products_data.append(columns)

    return products_data


def test_products_list_get(
    authorized_client,
    products_list_url,
    mock_products_list_get,
):

    response = authorized_client.get(products_list_url)
    assert response.status_code == 200
    soup = BeautifulSoup(response.content, "html.parser")

    assert "Product list" in soup.find("h1").text

    products_table = soup.find("table", attrs={"class": "govuk-table"})
    headers = ["Name", "Part number", "Control list entries", "Status", "View"]
    products_data = get_products_list_data(soup, products_table, headers)

    assert products_data == [
        {
            "Name": "p1",
            "Part number": "44",
            "Control list entries": "ML1a, \nML22b",
            "Status": "Verified",
        },
        {
            "Name": "p2",
            "Part number": "44",
            "Control list entries": "N/A",
            "Status": "Verified",
        },
    ]


def test_archived_products_list_get(
    authorized_client,
    archived_products_list_url,
    mock_archived_products_list_get,
):

    response = authorized_client.get(archived_products_list_url)
    assert response.status_code == 200
    soup = BeautifulSoup(response.content, "html.parser")

    assert "Archived products" in soup.find("h1").text

    headers = ["Name", "Part number", "Control list entries", "View"]
    products_table = soup.find("table", attrs={"class": "govuk-table"})
    products_data = get_products_list_data(soup, products_table, headers)

    assert products_data == [
        {
            "Name": "p1",
            "Part number": "44",
            "Control list entries": "ML1a, \nML22b",
        },
        {
            "Name": "p2",
            "Part number": "44",
            "Control list entries": "N/A",
        },
    ]
