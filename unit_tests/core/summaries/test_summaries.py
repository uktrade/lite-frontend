import pytest
from core.constants import FirearmsProductType, ProductCategories

from core.summaries.summaries import (
    NoSummaryForType,
    SummaryTypes,
    firearm_summary,
    firearm_on_application_summary,
    get_summary_type_for_good,
    get_summary_type_for_good_on_application,
)


def test_firearm_summary(data_standard_case, standard_firearm_expected_product_summary):
    is_user_rfd = False
    good_on_application = data_standard_case["case"]["data"]["goods"][0]
    product_summary = firearm_summary(good_on_application["good"], is_user_rfd, [])

    assert product_summary == standard_firearm_expected_product_summary


def test_firearm_on_application_summary(data_standard_case, standard_firearm_expected_product_on_application_summary):
    good_on_application = data_standard_case["case"]["data"]["goods"][0]
    product_summary = firearm_on_application_summary(good_on_application, [])

    assert product_summary == standard_firearm_expected_product_on_application_summary


@pytest.mark.parametrize(
    "good, summary_type",
    (
        (
            {"firearm_details": {"type": {"key": FirearmsProductType.FIREARMS}}},
            SummaryTypes.FIREARM,
        ),
        (
            {"item_category": {"key": ProductCategories.PRODUCT_CATEGORY_COMPLETE_ITEM}},
            SummaryTypes.COMPLETE_ITEM,
        ),
        (
            {"item_category": {"key": ProductCategories.PRODUCT_CATEGORY_MATERIAL}},
            SummaryTypes.MATERIAL,
        ),
        (
            {"item_category": {"key": ProductCategories.PRODUCT_CATEGORY_SOFTWARE}},
            SummaryTypes.TECHNOLOGY,
        ),
        (
            {"item_category": {"key": ProductCategories.PRODUCT_CATEGORY_COMPONENT_ACCESSORY}},
            SummaryTypes.COMPONENT_ACCESSORY,
        ),
    ),
)
def test_get_summary_type_for_good(good, summary_type):
    assert get_summary_type_for_good(good) == summary_type


@pytest.mark.parametrize(
    "good",
    (
        {},
        {"firearm_details": {}},
        {"firearm_details": {"type": {"key": "madeup"}}},
        {"item_category": None},
        {"item_category": {}},
        {"item_category": {"key": "madeup"}},
    ),
)
def test_get_summary_type_for_good_no_summary_type(good):
    with pytest.raises(NoSummaryForType):
        get_summary_type_for_good(good)


@pytest.mark.parametrize(
    "good_on_application, summary_type",
    (
        (
            {"firearm_details": {"type": {"key": FirearmsProductType.FIREARMS}}},
            SummaryTypes.FIREARM,
        ),
        (
            {"good": {"item_category": {"key": ProductCategories.PRODUCT_CATEGORY_COMPLETE_ITEM}}},
            SummaryTypes.COMPLETE_ITEM,
        ),
        (
            {"good": {"item_category": {"key": ProductCategories.PRODUCT_CATEGORY_MATERIAL}}},
            SummaryTypes.MATERIAL,
        ),
        (
            {"good": {"item_category": {"key": ProductCategories.PRODUCT_CATEGORY_SOFTWARE}}},
            SummaryTypes.TECHNOLOGY,
        ),
        (
            {"good": {"item_category": {"key": ProductCategories.PRODUCT_CATEGORY_COMPONENT_ACCESSORY}}},
            SummaryTypes.COMPONENT_ACCESSORY,
        ),
    ),
)
def test_get_summary_type_for_good_on_application(good_on_application, summary_type):
    assert get_summary_type_for_good_on_application(good_on_application) == summary_type


@pytest.mark.parametrize(
    "good_on_application",
    (
        {},
        {"firearm_details": {}},
        {"firearm_details": {"type": {"key": "madeup"}}},
        {"good": {}},
        {"good": {"item_category": None}},
        {"good": {"item_category": {}}},
        {"good": {"item_category": {"key": "madeup"}}},
    ),
)
def test_get_summary_type_for_good_on_application_no_summary_type(good_on_application):
    with pytest.raises(NoSummaryForType):
        get_summary_type_for_good_on_application(good_on_application)
