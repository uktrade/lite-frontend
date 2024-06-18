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
def archive_product_url(good_id):
    return reverse(
        "goods:good_archive_restore",
        kwargs={
            "pk": good_id,
            "action": "archive",
        },
    )


@pytest.fixture
def restore_product_url(good_id):
    return reverse(
        "goods:good_archive_restore",
        kwargs={
            "pk": good_id,
            "action": "restore",
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


@pytest.fixture
def put_good_api_url(good_id):
    return client._build_absolute_uri(f"/goods/{good_id}/")


@pytest.fixture
def mock_put_good(requests_mock, put_good_api_url):
    return requests_mock.put(
        put_good_api_url,
        json={"is_archived": True},
        status_code=200,
    )


@pytest.fixture
def mock_archived_good_with_history_get(requests_mock, data_standard_case):
    good = data_standard_case["case"]["data"]["goods"][0]
    good["good"].update(
        {
            "status": {"key": GoodStatus.VERIFIED, "value": GoodStatus.VERIFIED.title()},
            "is_archived": True,
            "archive_history": [
                {
                    "is_archived": True,
                    "actioned_on": "2024-06-18T20:47:39.047Z",
                    "user": {
                        "first_name": "Exporter",
                        "last_name": "User1",
                        "email": "exporter1@example.com",
                    },
                },
                {
                    "is_archived": False,
                    "actioned_on": "2024-05-24T13:02:22.544Z",
                    "user": {
                        "first_name": "Exporter",
                        "last_name": "User2",
                        "email": "exporter1@example.com",
                    },
                },
                {
                    "is_archived": True,
                    "actioned_on": "2024-04-10T12:46:57.161Z",
                    "user": {
                        "first_name": "Exporter",
                        "last_name": "User1",
                        "email": "exporter1@example.com",
                    },
                },
            ],
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


def test_archive_product_asks_for_confirmation(
    authorized_client,
    firearm_product_details_url,
    archive_product_url,
    mock_verified_good_get,
):
    response = authorized_client.get(firearm_product_details_url)
    assert response.status_code == 200
    soup = BeautifulSoup(response.content, "html.parser")
    assert "Archive product" in soup.find("a", {"id": "archive-good"}).text

    response = authorized_client.get(archive_product_url)
    assert response.status_code == 200

    soup = BeautifulSoup(response.content, "html.parser")
    assert soup.find("h1").text == "Are you sure you want to archive this product?"
    info_paragraphs = [p.text for p in soup.find_all("p", class_="govuk-body")]
    assert info_paragraphs == [
        "If you move this product to the archive you will not be able to use it on any applications and it will be hidden from your default product list.",
        "You can remove it from the archive and restore it to your product list at any time.",
    ]
    assert soup.find("input", {"id": "submit-id-submit"})["value"] == "Archive product"
    assert soup.find("a", {"id": "cancel-id-cancel"})["href"] == firearm_product_details_url


def test_restore_product_asks_for_confirmation(
    authorized_client,
    firearm_product_details_url,
    restore_product_url,
    mock_archived_good_with_history_get,
):
    response = authorized_client.get(firearm_product_details_url)
    assert response.status_code == 200
    soup = BeautifulSoup(response.content, "html.parser")
    assert "Restore product" in soup.find("a", {"id": "restore-good"}).text

    response = authorized_client.get(restore_product_url)
    assert response.status_code == 200

    soup = BeautifulSoup(response.content, "html.parser")
    assert soup.find("h1").text == "Are you sure you want to restore this product?"
    info_paragraphs = [p.text for p in soup.find_all("p", class_="govuk-body")]
    assert info_paragraphs == [
        "This product will show in your product list and you will be able to add it to applications.",
    ]
    assert soup.find("input", {"id": "submit-id-submit"})["value"] == "Restore product"
    assert soup.find("a", {"id": "cancel-id-cancel"})["href"] == firearm_product_details_url


def test_archived_product_details_context(
    authorized_client,
    firearm_product_details_url,
    mock_archived_good_with_history_get,
):

    response = authorized_client.get(firearm_product_details_url)
    assert response.status_code == 200
    soup = BeautifulSoup(response.content, "html.parser")

    assert "Restore product" in soup.find("a", {"id": "restore-good"}).text
    assert soup.find("a", {"id": "archive-good"}) is None
    assert soup.find("a", {"id": "delete-good"}) is None

    archive_history = [item.strip() for item in soup.find("div", {"id": "archive_history"}).text.split("\n") if item]
    assert archive_history == [
        "Archived by Exporter User1 at 20:47 on 18 June 2024",
        "Restored by Exporter User2 at 13:02 on 24 May 2024",
        "Archived by Exporter User1 at 12:46 on 10 April 2024",
    ]


def test_post_archive_product(
    authorized_client,
    firearm_product_details_url,
    archive_product_url,
    mock_verified_good_get,
    mock_put_good,
):
    response = authorized_client.post(archive_product_url)
    assert response.status_code == 302
    assert response.url == firearm_product_details_url
    assert mock_put_good.called_once
    assert mock_put_good.last_request.json() == {"is_archived": True}


def test_post_restore_product(
    authorized_client,
    firearm_product_details_url,
    restore_product_url,
    mock_verified_good_get,
    mock_put_good,
):
    response = authorized_client.post(restore_product_url)
    assert response.status_code == 302
    assert response.url == firearm_product_details_url
    assert mock_put_good.called_once
    assert mock_put_good.last_request.json() == {"is_archived": False}
