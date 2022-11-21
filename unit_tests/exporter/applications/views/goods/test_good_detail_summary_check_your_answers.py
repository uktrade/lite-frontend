import pytest
import uuid

from pytest_django.asserts import assertTemplateUsed

from django.urls import reverse

from core.constants import (
    FirearmsProductType,
    ProductCategories,
)


@pytest.fixture
def application(data_standard_case):
    return data_standard_case["case"]["data"]


@pytest.fixture
def good(data_standard_case):
    return data_standard_case["case"]["data"]["goods"][0]


@pytest.fixture
def good_detail_summary_check_your_answers_url(application):
    return reverse(
        "applications:good_detail_summary",
        kwargs={
            "pk": application["id"],
        },
    )


def test_good_detail_summary_check_your_answers_view_status_code(
    authorized_client,
    requests_mock,
    mock_application_get,
    good_detail_summary_check_your_answers_url,
    application,
    good,
):
    requests_mock.get(
        f"/applications/{application['id']}/goods/{good['good']['id']}/documents/",
        json={"documents": []},
    )

    response = authorized_client.get(good_detail_summary_check_your_answers_url)
    assert response.status_code == 200


def test_good_detail_summary_check_your_answers_view_template_used(
    authorized_client,
    requests_mock,
    mock_application_get,
    good_detail_summary_check_your_answers_url,
    application,
    good,
):
    requests_mock.get(
        f"/applications/{application['id']}/goods/{good['good']['id']}/documents/",
        json={"documents": []},
    )

    response = authorized_client.get(good_detail_summary_check_your_answers_url)
    assertTemplateUsed(response, "applications/goods/goods-detail-summary.html")


@pytest.mark.parametrize(
    "good_on_application, summary",
    (
        (
            {
                "firearm_details": {
                    "type": {
                        "key": FirearmsProductType.FIREARMS,
                    },
                },
                "good": {"id": str(uuid.uuid4())},
            },
            (
                ("id-summary", "summary", "firearm_summary"),
                ("id-application-summary", "application-summary", "firearm_on_application_summary"),
            ),
        ),
        (
            {
                "firearm_details": {
                    "type": {
                        "key": "not-firearms",
                    },
                },
                "good": {"id": str(uuid.uuid4())},
            },
            None,
        ),
        (
            {
                "good": {
                    "id": str(uuid.uuid4()),
                    "item_category": {
                        "key": ProductCategories.PRODUCT_CATEGORY_COMPLETE_ITEM,
                    },
                },
            },
            (
                ("id-summary", "summary", "complete_item_summary"),
                ("id-application-summary", "application-summary", "complete_item_product_on_application_summary"),
            ),
        ),
        (
            {
                "good": {
                    "id": str(uuid.uuid4()),
                    "item_category": {
                        "key": ProductCategories.PRODUCT_CATEGORY_MATERIAL,
                    },
                },
            },
            (
                ("id-summary", "summary", "material_summary"),
                ("id-application-summary", "application-summary", "material_product_on_application_summary"),
            ),
        ),
        (
            {
                "good": {
                    "id": str(uuid.uuid4()),
                    "item_category": {
                        "key": ProductCategories.PRODUCT_CATEGORY_TECHNOLOGY,
                    },
                },
            },
            (
                ("id-summary", "summary", "technology_summary"),
                ("id-application-summary", "application-summary", "technology_product_on_application_summary"),
            ),
        ),
        (
            {
                "good": {
                    "id": str(uuid.uuid4()),
                    "item_category": {
                        "key": "madeupkey",
                    },
                },
            },
            None,
        ),
    ),
)
def test_good_detail_summary_check_your_answers_context(
    authorized_client,
    requests_mock,
    good_detail_summary_check_your_answers_url,
    application,
    good_on_application,
    summary,
    mocker,
):
    requests_mock.get(
        f"/applications/{application['id']}/goods/{good_on_application['good']['id']}/documents/",
        json={"documents": []},
    )
    application["goods"] = [good_on_application]
    requests_mock.get(
        f'/applications/{application["id"]}/',
        json=application,
    )

    mocker.patch(
        "exporter.applications.views.goods.goods.firearm_summary",
        return_value=(("id-summary", "summary", "firearm_summary"),),
    )
    mocker.patch(
        "exporter.applications.views.goods.goods.firearm_on_application_summary",
        return_value=(("id-application-summary", "application-summary", "firearm_on_application_summary"),),
    )

    mocker.patch(
        "exporter.applications.views.goods.goods.complete_item_summary",
        return_value=(("id-summary", "summary", "complete_item_summary"),),
    )
    mocker.patch(
        "exporter.applications.views.goods.goods.complete_item_product_on_application_summary",
        return_value=(
            ("id-application-summary", "application-summary", "complete_item_product_on_application_summary"),
        ),
    )

    mocker.patch(
        "exporter.applications.views.goods.goods.material_summary",
        return_value=(("id-summary", "summary", "material_summary"),),
    )
    mocker.patch(
        "exporter.applications.views.goods.goods.material_product_on_application_summary",
        return_value=(("id-application-summary", "application-summary", "material_product_on_application_summary"),),
    )

    mocker.patch(
        "exporter.applications.views.goods.goods.technology_summary",
        return_value=(("id-summary", "summary", "technology_summary"),),
    )
    mocker.patch(
        "exporter.applications.views.goods.goods.technology_product_on_application_summary",
        return_value=(("id-application-summary", "application-summary", "technology_product_on_application_summary"),),
    )

    response = authorized_client.get(good_detail_summary_check_your_answers_url)
    context = response.context

    assert context["application_id"] == application["id"]
    assert [good for good, _ in context["goods"]] == application["goods"]
    assert [summary for _, summary in context["goods"]] == [summary]
    assert not context["is_user_rfd"]
    assert not context["application_status_draft"]
    assert context["organisation_documents"] == {}


def test_good_detail_summary_check_your_answers_non_firearm_product_type(
    authorized_client,
    requests_mock,
    mock_application_get,
    good_detail_summary_check_your_answers_url,
    application,
    good,
):
    requests_mock.get(
        f"/applications/{application['id']}/goods/{good['good']['id']}/documents/",
        json={"documents": []},
    )
    application["goods"][0]["firearm_details"] = None

    response = authorized_client.get(good_detail_summary_check_your_answers_url)
    context = response.context

    assert context["application_id"] == application["id"]
    assert [good for good, _ in context["goods"]] == application["goods"]
    assert [summary for _, summary in context["goods"]] == [None, None]
    assert not context["is_user_rfd"]
    assert not context["application_status_draft"]
    assert context["organisation_documents"] == {}
