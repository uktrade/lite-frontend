import pytest

from django.urls import reverse

from exporter.applications.views.goods.add_good_complete_product.views.constants import CompleteProductSteps

from exporter.goods.forms.firearms import (
    FirearmPvGradingForm,
    FirearmPvGradingDetailsForm,
)


@pytest.fixture(autouse=True)
def setup(no_op_storage):
    pass


@pytest.fixture
def new_good_compete_product_url(data_standard_case):
    application_id = data_standard_case["case"]["data"]["id"]
    return reverse(
        "applications:new_good_complete_product",
        kwargs={
            "pk": application_id,
        },
    )


@pytest.fixture(autouse=True)
def set_feature_flags(settings):
    settings.FEATURE_FLAG_NON_FIREARMS_ENABLED = True


@pytest.fixture
def post_goods_matcher(requests_mock, good_id):
    return requests_mock.post(
        f"/goods/",
        status_code=201,
        json={
            "good": {
                "id": good_id,
                "name": "p1",
            },
        },
    )


@pytest.fixture
def goto_step(goto_step_factory, new_good_compete_product_url):
    return goto_step_factory(new_good_compete_product_url)


@pytest.fixture
def post_to_step(post_to_step_factory, new_good_compete_product_url):
    return post_to_step_factory(new_good_compete_product_url)


def test_add_good_complete_product_access_denied_without_feature_flag(
    settings,
    authorized_client,
    new_good_compete_product_url,
):
    settings.FEATURE_FLAG_NON_FIREARMS_ENABLED = False
    response = authorized_client.get(new_good_compete_product_url)
    assert response.status_code == 404


def test_add_good_complete_product_end_to_end(
    authorized_client,
    data_standard_case,
    good_id,
    new_good_compete_product_url,
    mock_application_get,
    pv_gradings,
    post_to_step,
    post_goods_matcher,
):
    authorized_client.get(new_good_compete_product_url)

    response = post_to_step(
        CompleteProductSteps.NAME,
        {"name": "product_1"},
    )

    assert response.status_code == 200
    assert isinstance(response.context["form"], FirearmPvGradingForm)

    response = post_to_step(
        CompleteProductSteps.PV_GRADING,
        {"is_pv_graded": True},
    )

    assert response.status_code == 200
    assert isinstance(response.context["form"], FirearmPvGradingDetailsForm)
    response = post_to_step(
        CompleteProductSteps.PV_GRADING_DETAILS,
        {
            "prefix": "NATO",
            "grading": "official",
            "issuing_authority": "Government entity",
            "reference": "GR123",
            "date_of_issue_0": "20",
            "date_of_issue_1": "02",
            "date_of_issue_2": "2020",
        },
    )

    assert response.status_code == 302
    assert response.url == reverse(
        "applications:compete_product_summary",
        kwargs={
            "pk": data_standard_case["case"]["id"],
            "good_pk": good_id,
        },
    )

    assert post_goods_matcher.called_once
    last_request = post_goods_matcher.last_request
    assert last_request.json() == {
        "name": "product_1",
        "is_pv_graded": "yes",
        "pv_grading_details": {
            "prefix": "NATO",
            "grading": "official",
            "suffix": "",
            "issuing_authority": "Government entity",
            "reference": "GR123",
            "date_of_issue": "2020-02-20",
        },
        "item_category": "group1_platform",
        "is_good_controlled": None,
    }


def test_add_good_complete_product_no_pv(
    authorized_client,
    data_standard_case,
    good_id,
    new_good_compete_product_url,
    mock_application_get,
    post_to_step,
    post_goods_matcher,
):
    authorized_client.get(new_good_compete_product_url)

    response = post_to_step(
        CompleteProductSteps.NAME,
        {"name": "product_1"},
    )

    assert response.status_code == 200
    assert isinstance(response.context["form"], FirearmPvGradingForm)

    response = post_to_step(
        CompleteProductSteps.PV_GRADING,
        {"is_pv_graded": False},
    )
    assert response.status_code == 302
    assert response.url == reverse(
        "applications:compete_product_summary",
        kwargs={
            "pk": data_standard_case["case"]["id"],
            "good_pk": good_id,
        },
    )

    assert post_goods_matcher.called_once
    last_request = post_goods_matcher.last_request
    assert last_request.json() == {
        "name": "product_1",
        "is_pv_graded": "no",
        "item_category": "group1_platform",
        "is_good_controlled": None,
    }
