import pytest

from django.urls import reverse

from exporter.applications.views.goods.add_good_firearm.views.constants import AddGoodFirearmToApplicationSteps
from exporter.goods.forms.firearms import (
    FirearmOnwardExportedForm,
    FirearmOnwardAlteredProcessedForm,
    FirearmOnwardIncorporatedForm,
    FirearmQuantityAndValueForm,
    FirearmYearOfManufactureForm,
    FirearmSerialIdentificationMarkingsForm,
    FirearmSerialNumbersForm,
)


@pytest.fixture(autouse=True)
def setup(mock_application_get, mock_good_get, mock_good_on_application_post, no_op_storage):
    pass


@pytest.fixture(autouse=True)
def application(data_standard_case):
    return data_standard_case["case"]["data"]


@pytest.fixture
def new_firearm_to_application_url(application):
    good = application["goods"][0]["good"]
    return reverse(
        "applications:new_good_firearm_to_application",
        kwargs={
            "pk": application["id"],
            "good_pk": good["id"],
        },
    )


@pytest.fixture
def expected_good_data(application):
    good = application["goods"][0]["good"]
    return good


@pytest.fixture(autouse=True)
def set_feature_flags(settings):
    settings.FEATURE_FLAG_ONLY_ALLOW_FIREARMS_PRODUCTS = True
    settings.FEATURE_FLAG_PRODUCT_2_0 = True


@pytest.fixture
def goto_step(goto_step_factory, new_firearm_to_application_url):
    return goto_step_factory(new_firearm_to_application_url)


@pytest.fixture
def post_to_step(post_to_step_factory, new_firearm_to_application_url):
    return post_to_step_factory(new_firearm_to_application_url)


def test_add_firearm_to_application_product_made_before_1938_step(goto_step, post_to_step):
    goto_step(AddGoodFirearmToApplicationSteps.MADE_BEFORE_1938)
    response = post_to_step(
        AddGoodFirearmToApplicationSteps.MADE_BEFORE_1938,
        {"is_made_before_1938": True},
    )

    assert response.status_code == 200
    assert isinstance(response.context["form"], FirearmYearOfManufactureForm)


def test_add_firearm_to_application_product_not_made_before_1938_step(
    requests_mock, expected_good_data, goto_step, post_to_step
):
    goto_step(AddGoodFirearmToApplicationSteps.MADE_BEFORE_1938)
    response = post_to_step(
        AddGoodFirearmToApplicationSteps.MADE_BEFORE_1938,
        {"is_made_before_1938": False},
    )

    assert response.status_code == 200
    assert isinstance(response.context["form"], FirearmOnwardExportedForm)


def test_add_firearm_to_application_year_of_manufacture_step(
    requests_mock, expected_good_data, goto_step, post_to_step
):
    goto_step(AddGoodFirearmToApplicationSteps.MADE_BEFORE_1938)
    response = post_to_step(
        AddGoodFirearmToApplicationSteps.MADE_BEFORE_1938,
        {"is_made_before_1938": True},
    )
    response = post_to_step(
        AddGoodFirearmToApplicationSteps.YEAR_OF_MANUFACTURE,
        {"year_of_manufacture": 1937},
    )

    assert response.status_code == 200
    assert isinstance(response.context["form"], FirearmOnwardExportedForm)


def test_add_firearm_to_application_onward_exported_step_not_onward_export(
    requests_mock, expected_good_data, goto_step, post_to_step
):
    goto_step(AddGoodFirearmToApplicationSteps.ONWARD_EXPORTED)
    response = post_to_step(
        AddGoodFirearmToApplicationSteps.ONWARD_EXPORTED,
        {"is_onward_exported": False},
    )

    assert response.status_code == 200
    assert isinstance(response.context["form"], FirearmQuantityAndValueForm)


def test_add_firearm_to_application_end_to_end(
    requests_mock, expected_good_data, application, good_on_application, goto_step, post_to_step
):
    goto_step(AddGoodFirearmToApplicationSteps.MADE_BEFORE_1938)
    response = post_to_step(
        AddGoodFirearmToApplicationSteps.MADE_BEFORE_1938,
        {"is_made_before_1938": True},
    )
    assert isinstance(response.context["form"], FirearmYearOfManufactureForm)
    assert not response.context["form"].errors

    response = post_to_step(
        AddGoodFirearmToApplicationSteps.YEAR_OF_MANUFACTURE,
        {"year_of_manufacture": 1937},
    )

    assert isinstance(response.context["form"], FirearmOnwardExportedForm)
    assert not response.context["form"].errors

    response = post_to_step(
        AddGoodFirearmToApplicationSteps.ONWARD_EXPORTED,
        {"is_onward_exported": True},
    )
    assert isinstance(response.context["form"], FirearmOnwardAlteredProcessedForm)
    assert not response.context["form"].errors

    response = post_to_step(
        AddGoodFirearmToApplicationSteps.ONWARD_ALTERED_PROCESSED,
        {"is_onward_altered_processed": True, "is_onward_altered_processed_comments": "processed comments"},
    )
    assert isinstance(response.context["form"], FirearmOnwardIncorporatedForm)
    assert not response.context["form"].errors
    response = post_to_step(
        AddGoodFirearmToApplicationSteps.ONWARD_INCORPORATED,
        {"is_onward_incorporated": True, "is_onward_incorporated_comments": "incorporated comments"},
    )

    assert response.status_code == 200
    assert isinstance(response.context["form"], FirearmQuantityAndValueForm)

    response = post_to_step(
        AddGoodFirearmToApplicationSteps.QUANTITY_AND_VALUE,
        {"number_of_items": "2", "value": "16.32"},
    )

    assert isinstance(response.context["form"], FirearmSerialIdentificationMarkingsForm)

    response = post_to_step(
        AddGoodFirearmToApplicationSteps.SERIAL_IDENTIFICATION_MARKING,
        {"serial_numbers_available": "AVAILABLE"},
    )

    assert isinstance(response.context["form"], FirearmSerialNumbersForm)

    response = post_to_step(
        AddGoodFirearmToApplicationSteps.SERIAL_NUMBERS,
        {
            "serial_numbers_0": "s111",
            "serial_numbers_1": "s222",
        },
    )

    assert response.status_code == 302

    assert response.url == reverse(
        "applications:product_on_application_summary",
        kwargs={
            "pk": application["id"],
            "good_on_application_pk": good_on_application["good"]["id"],
        },
    )

    assert requests_mock.last_request.json() == {
        "firearm_details": {
            "is_made_before_1938": True,
            "year_of_manufacture": 1937,
            "is_onward_exported": True,
            "is_onward_altered_processed": True,
            "is_onward_altered_processed_comments": "processed comments",
            "is_onward_incorporated": True,
            "is_onward_incorporated_comments": "incorporated comments",
            "number_of_items": 2,
            "serial_numbers_available": "AVAILABLE",
            "no_identification_markings_details": "",
            "serial_numbers": ["s111", "s222"],
        },
        "good_id": expected_good_data["id"],
        "is_good_incorporated": True,
        "quantity": 2,
        "unit": "NAR",
        "value": "16.32",
    }
