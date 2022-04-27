import pytest

from django.urls import reverse

from exporter.applications.views.goods.add_good_firearm.views.constants import AddGoodFirearmToApplicationSteps
from exporter.goods.forms.firearms import (
    FirearmOnwardExportedForm,
    FirearmOnwardAlteredProcessedForm,
    FirearmOnwardIncorporatedForm,
    FirearmQuantityAndValueForm,
    FirearmSummaryForm,
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


@pytest.fixture(autouse=True)
def mock_get_document(requests_mock, expected_good_data):
    return requests_mock.get(
        f"/goods/{expected_good_data['id']}/documents/",
        json={},
    )


@pytest.fixture
def steps_data():
    return [
        (AddGoodFirearmToApplicationSteps.MADE_BEFORE_1938, {"is_made_before_1938": True}),
        (AddGoodFirearmToApplicationSteps.YEAR_OF_MANUFACTURE, {"year_of_manufacture": 1937}),
        (AddGoodFirearmToApplicationSteps.ONWARD_EXPORTED, {"is_onward_exported": True}),
        (
            AddGoodFirearmToApplicationSteps.ONWARD_ALTERED_PROCESSED,
            {"is_onward_altered_processed": True, "is_onward_altered_processed_comments": "processed comments"},
        ),
        (
            AddGoodFirearmToApplicationSteps.ONWARD_INCORPORATED,
            {"is_onward_incorporated": True, "is_onward_incorporated_comments": "incorporated comments"},
        ),
        (AddGoodFirearmToApplicationSteps.QUANTITY_AND_VALUE, {"number_of_items": "2", "value": "16.32"}),
        (AddGoodFirearmToApplicationSteps.SERIAL_IDENTIFICATION_MARKING, {"serial_numbers_available": "AVAILABLE"}),
    ]


@pytest.fixture
def advance_to_step(post_to_step, steps_data):
    def advance(step_name):
        for step in steps_data:
            if step_name == step[0]:
                return
            else:
                post_to_step(
                    step[0],
                    step[1],
                )

    return advance


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


def test_add_firearm_to_application_year_of_manufacture_step(goto_step, post_to_step):
    goto_step(AddGoodFirearmToApplicationSteps.MADE_BEFORE_1938)
    post_to_step(
        AddGoodFirearmToApplicationSteps.MADE_BEFORE_1938,
        {"is_made_before_1938": True},
    )
    response = post_to_step(
        AddGoodFirearmToApplicationSteps.YEAR_OF_MANUFACTURE,
        {"year_of_manufacture": 1937},
    )

    assert response.status_code == 200
    assert isinstance(response.context["form"], FirearmOnwardExportedForm)


def test_add_firearm_to_application_onward_exported_step_not_onward_export(goto_step, post_to_step):
    goto_step(AddGoodFirearmToApplicationSteps.ONWARD_EXPORTED)
    response = post_to_step(
        AddGoodFirearmToApplicationSteps.ONWARD_EXPORTED,
        {"is_onward_exported": False},
    )

    assert response.status_code == 200
    assert isinstance(response.context["form"], FirearmQuantityAndValueForm)


def test_add_firearm_to_application_serial_numbers_later(post_to_step, advance_to_step):

    advance_to_step(AddGoodFirearmToApplicationSteps.SERIAL_IDENTIFICATION_MARKING)
    response = post_to_step(
        AddGoodFirearmToApplicationSteps.SERIAL_IDENTIFICATION_MARKING,
        {"serial_numbers_available": "LATER"},
    )

    assert response.status_code == 200
    assert isinstance(response.context["form"], FirearmSummaryForm)


def test_add_firearm_to_application_serial_numbers_not_available(post_to_step, advance_to_step):

    advance_to_step(AddGoodFirearmToApplicationSteps.SERIAL_IDENTIFICATION_MARKING)
    response = post_to_step(
        AddGoodFirearmToApplicationSteps.SERIAL_IDENTIFICATION_MARKING,
        {"serial_numbers_available": "NOT_AVAILABLE"},
    )

    assert response.status_code == 200
    assert response.context["form"].errors == {
        "no_identification_markings_details": ["Enter why products will not have serial numbers"]
    }

    response = post_to_step(
        AddGoodFirearmToApplicationSteps.SERIAL_IDENTIFICATION_MARKING,
        {"serial_numbers_available": "NOT_AVAILABLE", "no_identification_markings_details": "lost"},
    )

    assert response.status_code == 200
    assert isinstance(response.context["form"], FirearmSummaryForm)


def test_add_firearm_to_application_end_to_end(requests_mock, expected_good_data, application, goto_step, post_to_step):

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

    assert response.status_code == 200
    assert isinstance(response.context["form"], FirearmSummaryForm)

    response = post_to_step(
        AddGoodFirearmToApplicationSteps.SUMMARY,
        {},
    )

    assert response.status_code == 302

    assert response.url == reverse("applications:goods", kwargs={"pk": application["id"]})

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
