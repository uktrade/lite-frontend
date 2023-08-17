import pytest
from bs4 import BeautifulSoup
from django.urls import reverse

from core import client
from exporter.applications.views.goods.material.views.constants import AddGoodMaterialToApplicationSteps
from exporter.applications.views.goods.material.views.edit import SummaryTypeMixin
from exporter.goods.forms.common import (
    ProductOnwardAlteredProcessedForm,
    ProductOnwardExportedForm,
    ProductOnwardIncorporatedForm,
    ProductUnitQuantityAndValueForm,
)


@pytest.fixture
def mock_good_on_application_get(requests_mock, good_on_application):
    url = client._build_absolute_uri(f'/applications/good-on-application/{good_on_application["id"]}')
    del good_on_application["firearm_details"]
    return requests_mock.get(url=url, json=good_on_application, status_code=200)


@pytest.fixture(autouse=True)
def setup(mock_application_get, mock_good_get, mock_good_on_application_get):
    yield


@pytest.fixture
def edit_onward_exported_url(application, good_on_application, summary_type):
    url = reverse(
        "applications:material_on_application_summary_edit_onward_exported",
        kwargs={
            "pk": application["id"],
            "good_on_application_pk": good_on_application["id"],
            "summary_type": summary_type,
        },
    )
    return url


@pytest.fixture
def post_to_step_onward_exported(post_to_step_factory, edit_onward_exported_url):
    return post_to_step_factory(edit_onward_exported_url)


@pytest.mark.parametrize(
    "summary_type",
    SummaryTypeMixin.SUMMARY_TYPES,
)
def test_edit_onward_exported_true(
    authorized_client,
    edit_onward_exported_url,
    post_to_step_onward_exported,
    product_on_application_summary_url_factory,
    mock_good_on_application_put,
    summary_type,
):
    response = authorized_client.get(edit_onward_exported_url)
    assert response.status_code == 200
    form = response.context["form"]
    assert isinstance(form, ProductOnwardExportedForm)
    assert form.initial == {
        "is_onward_exported": True,
    }

    response = post_to_step_onward_exported(
        AddGoodMaterialToApplicationSteps.ONWARD_EXPORTED,
        data={"is_onward_exported": True},
    )
    assert response.status_code == 200
    form = response.context["form"]
    assert isinstance(form, ProductOnwardAlteredProcessedForm)
    assert form.initial == {
        "is_onward_altered_processed": True,
        "is_onward_altered_processed_comments": "I will alter it real good",
    }

    response = post_to_step_onward_exported(
        AddGoodMaterialToApplicationSteps.ONWARD_ALTERED_PROCESSED,
        data={
            "is_onward_altered_processed": True,
            "is_onward_altered_processed_comments": "Altering",
        },
    )
    assert response.status_code == 200
    form = response.context["form"]
    assert isinstance(form, ProductOnwardIncorporatedForm)
    assert form.initial == {
        "is_onward_incorporated": True,
        "is_onward_incorporated_comments": "I will onward incorporate",
    }

    response = post_to_step_onward_exported(
        AddGoodMaterialToApplicationSteps.ONWARD_INCORPORATED,
        data={
            "is_onward_incorporated": True,
            "is_onward_incorporated_comments": "Incorporated",
        },
    )
    assert response.status_code == 302
    assert response.url == product_on_application_summary_url_factory(summary_type)

    assert mock_good_on_application_put.called_once
    assert mock_good_on_application_put.last_request.json() == {
        "is_onward_altered_processed": True,
        "is_onward_altered_processed_comments": "Altering",
        "is_onward_exported": True,
        "is_onward_incorporated": True,
        "is_onward_incorporated_comments": "Incorporated",
        "is_good_incorporated": True,
    }


@pytest.mark.parametrize(
    "summary_type",
    SummaryTypeMixin.SUMMARY_TYPES,
)
def test_edit_onward_exported_false(
    authorized_client,
    edit_onward_exported_url,
    post_to_step_onward_exported,
    product_on_application_summary_url_factory,
    mock_good_on_application_put,
    summary_type,
):
    response = authorized_client.get(edit_onward_exported_url)
    assert response.status_code == 200
    form = response.context["form"]
    assert isinstance(form, ProductOnwardExportedForm)
    assert form.initial == {
        "is_onward_exported": True,
    }

    response = post_to_step_onward_exported(
        AddGoodMaterialToApplicationSteps.ONWARD_EXPORTED,
        data={"is_onward_exported": False},
    )
    assert response.status_code == 302
    assert response.url == product_on_application_summary_url_factory(summary_type)

    assert mock_good_on_application_put.called_once
    assert mock_good_on_application_put.last_request.json() == {
        "is_onward_exported": False,
    }


@pytest.fixture
def edit_onward_altered_url(application, good_on_application, summary_type):
    url = reverse(
        "applications:material_on_application_summary_edit_onward_altered",
        kwargs={
            "pk": application["id"],
            "good_on_application_pk": good_on_application["id"],
            "summary_type": summary_type,
        },
    )
    return url


@pytest.mark.parametrize(
    "summary_type",
    SummaryTypeMixin.SUMMARY_TYPES,
)
def test_edit_onward_altered_processed(
    authorized_client,
    edit_onward_altered_url,
    product_on_application_summary_url_factory,
    mock_good_on_application_put,
    summary_type,
):
    response = authorized_client.get(edit_onward_altered_url)
    assert response.status_code == 200
    assert isinstance(response.context["form"], ProductOnwardAlteredProcessedForm)
    assert response.context["form"].initial == {
        "is_onward_altered_processed": True,
        "is_onward_altered_processed_comments": "I will alter it real good",
    }
    soup = BeautifulSoup(response.content, "html.parser")
    assert (
        soup.title.string.strip()
        == "Will the item be altered or processed before it is exported again? - LITE - GOV.UK"
    )

    response = authorized_client.post(
        edit_onward_altered_url,
        data={
            "is_onward_altered_processed": True,
            "is_onward_altered_processed_comments": "Altered",
        },
    )
    assert response.status_code == 302
    assert response.url == product_on_application_summary_url_factory(summary_type)
    assert mock_good_on_application_put.called_once
    assert mock_good_on_application_put.last_request.json() == {
        "is_onward_altered_processed": True,
        "is_onward_altered_processed_comments": "Altered",
    }


@pytest.fixture
def edit_onward_incorporated_url(application, good_on_application, summary_type):
    url = reverse(
        "applications:material_on_application_summary_edit_onward_incorporated",
        kwargs={
            "pk": application["id"],
            "good_on_application_pk": good_on_application["id"],
            "summary_type": summary_type,
        },
    )
    return url


@pytest.mark.parametrize(
    "summary_type",
    SummaryTypeMixin.SUMMARY_TYPES,
)
def test_edit_onward_incorporated(
    authorized_client,
    edit_onward_incorporated_url,
    product_on_application_summary_url_factory,
    mock_good_on_application_put,
    summary_type,
):
    response = authorized_client.get(edit_onward_incorporated_url)
    assert response.status_code == 200
    assert isinstance(response.context["form"], ProductOnwardIncorporatedForm)
    assert response.context["form"].initial == {
        "is_onward_incorporated": True,
        "is_onward_incorporated_comments": "I will onward incorporate",
    }
    soup = BeautifulSoup(response.content, "html.parser")
    assert (
        soup.title.string.strip()
        == "Will the product be incorporated into another item before it is onward exported? - LITE - GOV.UK"
    )

    response = authorized_client.post(
        edit_onward_incorporated_url,
        data={
            "is_onward_incorporated": True,
            "is_onward_incorporated_comments": "Incorporated",
        },
    )
    assert response.status_code == 302
    assert response.url == product_on_application_summary_url_factory(summary_type)
    assert mock_good_on_application_put.called_once
    assert mock_good_on_application_put.last_request.json() == {
        "is_onward_incorporated": True,
        "is_onward_incorporated_comments": "Incorporated",
        "is_good_incorporated": True,
    }


@pytest.fixture
def edit_unit_quantity_value_url(application, good_on_application, summary_type):
    url = reverse(
        "applications:material_on_application_summary_edit_unit_quantity_value",
        kwargs={
            "pk": application["id"],
            "good_on_application_pk": good_on_application["id"],
            "summary_type": summary_type,
        },
    )
    return url


@pytest.mark.parametrize(
    "summary_type",
    SummaryTypeMixin.SUMMARY_TYPES,
)
def test_edit_quantity_value(
    authorized_client,
    edit_unit_quantity_value_url,
    product_on_application_summary_url_factory,
    mock_good_on_application_put,
    summary_type,
    get_units_mock,
):
    response = authorized_client.get(edit_unit_quantity_value_url)
    assert response.status_code == 200
    assert isinstance(response.context["form"], ProductUnitQuantityAndValueForm)
    assert response.context["form"].initial == {
        "unit": "GRM",
        "quantity": 3.0,
        "value": "16.32",
    }
    soup = BeautifulSoup(response.content, "html.parser")
    assert soup.title.string.strip() == "Quantity and value - LITE - GOV.UK"

    response = authorized_client.post(
        edit_unit_quantity_value_url,
        data={
            "unit": "TON",
            "quantity": "20",
            "value": "20.22",
        },
    )
    assert response.status_code == 302
    assert response.url == product_on_application_summary_url_factory(summary_type)
    assert mock_good_on_application_put.called_once
    assert mock_good_on_application_put.last_request.json() == {
        "unit": "TON",
        "quantity": "20",
        "value": "20.22",
    }
