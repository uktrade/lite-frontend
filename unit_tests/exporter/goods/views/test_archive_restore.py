import pytest

from bs4 import BeautifulSoup
from pytest_django.asserts import assertTemplateUsed

from django.urls import reverse

from core import client
from exporter.goods.constants import GoodStatus


@pytest.fixture
def firearm_product_details_url(good_id):
    return reverse(
        "goods:firearm_detail",
        kwargs={
            "pk": good_id,
        },
    )


@pytest.fixture
def mock_draft_good_get(requests_mock, data_standard_case):
    good = data_standard_case["case"]["data"]["goods"][0]
    good["good"].update(
        {
            "status": {"key": GoodStatus.DRAFT, "value": GoodStatus.DRAFT.title()},
        }
    )

    url = client._build_absolute_uri(f'/goods/{good["good"]["id"]}/')
    return requests_mock.get(url=url, json=good)


@pytest.fixture
def mock_submitted_good_get(requests_mock, data_standard_case):
    good = data_standard_case["case"]["data"]["goods"][0]
    good["good"].update(
        {
            "status": {"key": GoodStatus.SUBMITTED, "value": GoodStatus.SUBMITTED.title()},
        }
    )

    url = client._build_absolute_uri(f'/goods/{good["good"]["id"]}/')
    return requests_mock.get(url=url, json=good)


@pytest.fixture
def mock_verified_good_get(requests_mock, data_standard_case):
    good = data_standard_case["case"]["data"]["goods"][0]
    good["good"].update(
        {
            "status": {"key": GoodStatus.VERIFIED, "value": GoodStatus.VERIFIED.title()},
        }
    )

    url = client._build_absolute_uri(f'/goods/{good["good"]["id"]}/')
    return requests_mock.get(url=url, json=good)


def test_draft_product_details_context(
    authorized_client,
    firearm_product_details_url,
    mock_draft_good_get,
):

    response = authorized_client.get(firearm_product_details_url)
    assert response.status_code == 200
    soup = BeautifulSoup(response.content, "html.parser")

    assert "Delete product" in soup.find("a", {"id": "delete-good"}).text
    assert soup.find("a", {"id": "archive-good"}) is None
    assert soup.find("a", {"id": "restore-good"}) is None


def test_submitted_product_details_context(
    authorized_client,
    firearm_product_details_url,
    mock_submitted_good_get,
):

    response = authorized_client.get(firearm_product_details_url)
    assert response.status_code == 200
    soup = BeautifulSoup(response.content, "html.parser")

    assert "Archive product" in soup.find("a", {"id": "archive-good"}).text
    assert soup.find("a", {"id": "restore-good"}) is None
    assert soup.find("a", {"id": "delete-good"}) is None


def test_verified_product_details_context(
    authorized_client,
    firearm_product_details_url,
    mock_verified_good_get,
):

    response = authorized_client.get(firearm_product_details_url)
    assert response.status_code == 200
    soup = BeautifulSoup(response.content, "html.parser")

    assert "Archive product" in soup.find("a", {"id": "archive-good"}).text
    assert soup.find("a", {"id": "restore-good"}) is None
    assert soup.find("a", {"id": "delete-good"}) is None
