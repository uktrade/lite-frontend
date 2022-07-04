import uuid

from core.summaries.summaries import (
    firearm_product_summary,
    firearm_product_on_application_summary,
)


def test_firearm_product_summary(data_standard_case, standard_firearm_expected_product_summary):
    is_user_rfd = False
    good_on_application = data_standard_case["case"]["data"]["goods"][0]
    product_summary = firearm_product_summary(good_on_application["good"], is_user_rfd, [])

    assert product_summary == standard_firearm_expected_product_summary


def test_firearm_product_on_application_summary(
    data_standard_case, standard_firearm_expected_product_on_application_summary
):
    good_on_application = data_standard_case["case"]["data"]["goods"][0]
    product_summary = firearm_product_on_application_summary(good_on_application, [])

    assert product_summary == standard_firearm_expected_product_on_application_summary
