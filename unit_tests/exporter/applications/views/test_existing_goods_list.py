import pytest
import uuid

from pytest_django.asserts import assertTemplateUsed

from django.urls import reverse


@pytest.fixture
def application(data_standard_case):
    return data_standard_case["case"]["data"]


@pytest.fixture
def existing_goods_list_url(application):
    return reverse(
        "applications:preexisting_good",
        kwargs={
            "pk": application["id"],
        },
    )


@pytest.fixture
def mock_goods_get(requests_mock):
    return requests_mock.get("/goods/", json={"results": [{"id": str(uuid.uuid4())}]})


def test_existing_goods_list_response_status(
    authorized_client,
    existing_goods_list_url,
    mock_application_get,
    mock_goods_get,
):
    response = authorized_client.get(existing_goods_list_url)
    assert response.status_code == 200


def test_existing_goods_list_templates_used(
    authorized_client,
    existing_goods_list_url,
    mock_application_get,
    mock_goods_get,
):
    response = authorized_client.get(existing_goods_list_url)
    assertTemplateUsed(response, "applications/goods/preexisting.html")
    assertTemplateUsed(response, "includes/verified-control-list-entries.html")
