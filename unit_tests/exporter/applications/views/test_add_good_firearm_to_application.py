import pytest

from django.urls import reverse

from exporter.applications.views.goods.add_good_firearm.views.constants import AddGoodFirearmToApplicationSteps
from exporter.goods.forms.firearms import FirearmYearOfManufactureForm


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
    return application["goods"][0]["good"]


@pytest.fixture(autouse=True)
def set_feature_flags(settings):
    settings.FEATURE_FLAG_ONLY_ALLOW_FIREARMS_PRODUCTS = True
    settings.FEATURE_FLAG_PRODUCT_2_0 = True


@pytest.fixture
def goto_step(authorized_client, new_firearm_to_application_url):
    def _goto_step(step_name):
        return authorized_client.post(
            new_firearm_to_application_url,
            data={
                "wizard_goto_step": step_name,
            },
        )

    return _goto_step


@pytest.fixture
def post_to_step(authorized_client, new_firearm_to_application_url):
    ADD_GOOD_FIREARM_TO_APPLICATION_VIEW = "add_good_firearm_to_application"

    def _post_to_step(step_name, data):
        return authorized_client.post(
            new_firearm_to_application_url,
            data={
                f"{ADD_GOOD_FIREARM_TO_APPLICATION_VIEW}-current_step": step_name,
                **{f"{step_name}-{key}": value for key, value in data.items()},
            },
        )

    return _post_to_step


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

    assert response.status_code == 302
    expected_good_data["firearm_details"]["is_made_before_1938"] = False
    assert requests_mock.last_request.json() == expected_good_data


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

    assert response.status_code == 302
    expected_good_data["firearm_details"]["is_made_before_1938"] = True
    expected_good_data["firearm_details"]["year_of_manufacture"] = 1937
    assert requests_mock.last_request.json() == expected_good_data
