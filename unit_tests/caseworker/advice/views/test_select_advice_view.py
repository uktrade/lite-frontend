import pytest
from bs4 import BeautifulSoup

from django.urls import reverse

from unit_tests.caseworker.conftest import standard_case_pk


@pytest.fixture(autouse=True)
def setup(mock_queue, mock_case):
    yield


@pytest.fixture
def url(data_queue, data_standard_case):
    return reverse("cases:select_advice", kwargs={"queue_pk": data_queue["id"], "pk": data_standard_case["case"]["id"]})


def test_select_advice_get(authorized_client, url):
    response = authorized_client.get(url)
    assert response.status_code == 200


@pytest.mark.parametrize("recommendation, redirect", [("approve_all", "approve"), ("refuse_all", "refuse")])
def test_select_advice_post(authorized_client, url, recommendation, redirect):
    response = authorized_client.post(url, data={"recommendation": recommendation})
    assert response.status_code == 302
    assert redirect in response.url


def test_view_serial_numbers_for_firearm_product_in_select_advice_view(authorized_client, data_standard_case, url):
    good = data_standard_case["case"]["data"]["goods"][0]
    assert good["good"]["firearm_details"]["serial_numbers"][0] == "12345"
    assert good["good"]["firearm_details"]["serial_numbers"][1] == "ABC-123"

    response = authorized_client.get(url)
    soup = BeautifulSoup(response.content, "html.parser")

    product_details = [d for d in soup.find_all("details") if "Products" in str(d.summary.span)][0]

    assert "1. 12345" in str(product_details)
    assert "2. ABC-123" in str(product_details)
    assert "Not added yet" not in str(product_details)


def test_serial_numbers_not_added_for_firearm_product_in_select_advice_view(authorized_client, data_standard_case, url):
    data_standard_case["case"]["data"]["goods"][0]["firearm_details"]["serial_numbers"] = []
    data_standard_case["case"]["data"]["goods"][0]["firearm_details"]["serial_numbers_available"] = "LATER"

    response = authorized_client.get(url)
    soup = BeautifulSoup(response.content, "html.parser")

    product_details = [d for d in soup.find_all("details") if "Products" in str(d.summary.span)][0]

    assert "1. 12345" not in str(product_details)
    assert "2. ABC-123" not in str(product_details)
    assert "Not added yet" in str(product_details)
