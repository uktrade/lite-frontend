import pytest
from bs4 import BeautifulSoup
from django.urls import reverse

from exporter.goods.forms.common import ProductQuantityAndValueForm


@pytest.fixture(autouse=True)
def setup(mock_application_get, mock_good_get, mock_good_on_application_get):
    yield


@pytest.fixture
def edit_quantity_value_url(application, good_on_application):
    url = reverse(
        "applications:edit_preexisting_good",
        kwargs={
            "pk": application["id"],
            "good_on_application_pk": good_on_application["id"],
        },
    )
    return url


def test_edit_quantity_value_existing_good(
    authorized_client,
    edit_quantity_value_url,
    application_products_url,
    mock_good_on_application_put,
):
    response = authorized_client.get(edit_quantity_value_url)
    assert response.status_code == 200
    assert isinstance(response.context["form"], ProductQuantityAndValueForm)
    assert response.context["form"].initial == {
        "number_of_items": 3,
        "value": "16.32",
    }
    soup = BeautifulSoup(response.content, "html.parser")
    assert soup.title.string.strip() == "Quantity and value - LITE - GOV.UK"

    response = authorized_client.post(
        edit_quantity_value_url,
        data={
            "number_of_items": 20,
            "value": "20.22",
        },
    )
    assert response.status_code == 302
    assert response.url == application_products_url
    assert mock_good_on_application_put.called_once
    assert mock_good_on_application_put.last_request.json() == {
        "quantity": "20",
        "unit": "NAR",
        "value": "20.22",
    }
