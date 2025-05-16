import logging
import pytest

from django.urls import reverse

from core import client

from exporter.applications.views.goods.component.views.constants import AddGoodComponentToApplicationSteps
from exporter.goods.forms.common import (
    ProductOnwardAlteredProcessedForm,
    ProductOnwardIncorporatedForm,
    ProductQuantityAndValueForm,
)


@pytest.fixture(autouse=True)
def setup(mock_application_get, mock_good_get, no_op_storage):
    yield


@pytest.fixture
def new_component_accessory_to_application_url(application):
    good = application["goods"][0]["good"]
    return reverse(
        "applications:new_good_component_accessory_to_application",
        kwargs={
            "pk": application["id"],
            "good_pk": good["id"],
        },
    )


@pytest.fixture
def expected_good_data(application):
    good = application["goods"][0]["good"]
    return good


@pytest.fixture
def goto_step(goto_step_factory, new_component_accessory_to_application_url):
    return goto_step_factory(new_component_accessory_to_application_url)


@pytest.fixture
def post_to_step(post_to_step_factory, new_component_accessory_to_application_url):
    return post_to_step_factory(new_component_accessory_to_application_url)


@pytest.fixture(autouse=True)
def mock_get_document(requests_mock, expected_good_data):
    return requests_mock.get(
        f"/goods/{expected_good_data['id']}/documents/",
        json={},
    )


def test_add_component_accessory_to_application_onward_exported_step_not_onward_export(goto_step, post_to_step):
    goto_step(AddGoodComponentToApplicationSteps.ONWARD_EXPORTED)
    response = post_to_step(
        AddGoodComponentToApplicationSteps.ONWARD_EXPORTED,
        {"is_onward_exported": False},
    )

    assert response.status_code == 200
    assert isinstance(response.context["form"], ProductQuantityAndValueForm)


def test_add_component_accessory_to_application_end_to_end(
    requests_mock,
    expected_good_data,
    mock_good_on_application_post,
    application,
    good_on_application,
    goto_step,
    post_to_step,
):

    response = post_to_step(
        AddGoodComponentToApplicationSteps.ONWARD_EXPORTED,
        {"is_onward_exported": True},
    )
    assert response.status_code == 200
    assert not response.context["form"].errors
    assert isinstance(response.context["form"], ProductOnwardAlteredProcessedForm)

    response = post_to_step(
        AddGoodComponentToApplicationSteps.ONWARD_ALTERED_PROCESSED,
        {"is_onward_altered_processed": True, "is_onward_altered_processed_comments": "processed comments"},
    )
    assert response.status_code == 200
    assert not response.context["form"].errors
    assert isinstance(response.context["form"], ProductOnwardIncorporatedForm)

    response = post_to_step(
        AddGoodComponentToApplicationSteps.ONWARD_INCORPORATED,
        {"is_onward_incorporated": True, "is_onward_incorporated_comments": "incorporated comments"},
    )
    assert response.status_code == 200
    assert not response.context["form"].errors
    assert isinstance(response.context["form"], ProductQuantityAndValueForm)

    response = post_to_step(
        AddGoodComponentToApplicationSteps.QUANTITY_AND_VALUE,
        {"number_of_items": "2", "value": "16.32"},
    )

    assert response.status_code == 302
    assert response.url == reverse(
        "applications:component_accessory_on_application_summary",
        kwargs={
            "pk": application["id"],
            "good_on_application_pk": good_on_application["good"]["id"],
        },
    )

    assert mock_good_on_application_post.last_request.json() == {
        "is_onward_exported": True,
        "is_onward_altered_processed": True,
        "is_onward_altered_processed_comments": "processed comments",
        "is_onward_incorporated": True,
        "is_onward_incorporated_comments": "incorporated comments",
        "good_id": expected_good_data["id"],
        "is_good_incorporated": False,
        "quantity": "2",
        "unit": "NAR",
        "value": "16.32",
    }


def test_add_component_accessory_to_application_end_to_end_no_set_quantities_or_values(
    requests_mock,
    expected_good_data,
    mock_good_on_application_post,
    application,
    good_on_application,
    goto_step,
    post_to_step,
    settings,
):
    settings.FEATURE_FLAG_INDETERMINATE_EXPORT_LICENCE_TYPE_ALLOWED_ORGANISATIONS = ["*"]

    response = post_to_step(
        AddGoodComponentToApplicationSteps.ONWARD_EXPORTED,
        {"is_onward_exported": True},
    )
    assert response.status_code == 200
    assert not response.context["form"].errors
    assert isinstance(response.context["form"], ProductOnwardAlteredProcessedForm)

    response = post_to_step(
        AddGoodComponentToApplicationSteps.ONWARD_ALTERED_PROCESSED,
        {"is_onward_altered_processed": True, "is_onward_altered_processed_comments": "processed comments"},
    )
    assert response.status_code == 200
    assert not response.context["form"].errors
    assert isinstance(response.context["form"], ProductOnwardIncorporatedForm)

    response = post_to_step(
        AddGoodComponentToApplicationSteps.ONWARD_INCORPORATED,
        {"is_onward_incorporated": True, "is_onward_incorporated_comments": "incorporated comments"},
    )
    assert response.status_code == 200
    assert not response.context["form"].errors
    assert isinstance(response.context["form"], ProductQuantityAndValueForm)

    response = post_to_step(
        AddGoodComponentToApplicationSteps.QUANTITY_AND_VALUE,
        {"no_set_quantities_or_value": True},
    )

    assert response.status_code == 302
    assert response.url == reverse(
        "applications:component_accessory_on_application_summary",
        kwargs={
            "pk": application["id"],
            "good_on_application_pk": good_on_application["good"]["id"],
        },
    )

    assert mock_good_on_application_post.last_request.json() == {
        "is_onward_exported": True,
        "is_onward_altered_processed": True,
        "is_onward_altered_processed_comments": "processed comments",
        "is_onward_incorporated": True,
        "is_onward_incorporated_comments": "incorporated comments",
        "good_id": expected_good_data["id"],
        "is_good_incorporated": False,
        "quantity": None,
        "unit": None,
        "value": None,
    }


def test_add_component_accessory_to_application_end_to_end_handles_service_error(
    requests_mock,
    expected_good_data,
    application,
    good_on_application,
    goto_step,
    post_to_step,
    data_standard_case,
    caplog,
):
    application = data_standard_case["case"]["data"]
    url = client._build_absolute_uri(f'/applications/{application["id"]}/goods/')
    requests_mock.post(url=url, json={"errors": ["Failed to post"]}, status_code=400)

    response = post_to_step(
        AddGoodComponentToApplicationSteps.ONWARD_EXPORTED,
        {"is_onward_exported": True},
    )
    assert response.status_code == 200
    assert not response.context["form"].errors
    assert isinstance(response.context["form"], ProductOnwardAlteredProcessedForm)

    response = post_to_step(
        AddGoodComponentToApplicationSteps.ONWARD_ALTERED_PROCESSED,
        {"is_onward_altered_processed": True, "is_onward_altered_processed_comments": "processed comments"},
    )
    assert response.status_code == 200
    assert not response.context["form"].errors
    assert isinstance(response.context["form"], ProductOnwardIncorporatedForm)

    response = post_to_step(
        AddGoodComponentToApplicationSteps.ONWARD_INCORPORATED,
        {"is_onward_incorporated": True, "is_onward_incorporated_comments": "incorporated comments"},
    )
    assert response.status_code == 200
    assert not response.context["form"].errors
    assert isinstance(response.context["form"], ProductQuantityAndValueForm)

    response = post_to_step(
        AddGoodComponentToApplicationSteps.QUANTITY_AND_VALUE,
        {"number_of_items": "2", "value": "16.32"},
    )

    assert response.status_code == 200
    assert "Unexpected error adding component accessory to application" in str(response.content)
    assert len(caplog.records) == 1
    log = caplog.records[0]
    assert (
        log.message
        == "Error adding component accessory to application - response was: 400 - {'errors': ['Failed to post']}"
    )
    assert log.levelno == logging.ERROR
