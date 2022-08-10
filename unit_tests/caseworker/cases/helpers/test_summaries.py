import uuid

from caseworker.cases.helpers.summaries import (
    firearm_summary,
    firearm_on_application_summary,
)

from unit_tests.helpers import merge_summaries


def test_firearm_summary(data_standard_case, standard_firearm_expected_product_summary):
    is_user_rfd = False
    good_on_application = data_standard_case["case"]["data"]["goods"][0]
    queue_pk = uuid.uuid4()
    product_summary = firearm_summary(good_on_application, is_user_rfd, {}, queue_pk)

    expected_summary = merge_summaries(
        standard_firearm_expected_product_summary,
        (
            (
                "product-document",
                '<a class="govuk-link govuk-link--no-visited-state" '
                f'href="/queues/{queue_pk}/cases/8fb76bed-fd45-4293-95b8-eda9468aa254/documents/6c48a2cc-1ed9-49a5-8ca7-df8af5fc2335/" '
                'target="_blank">data_sheet.pdf</a>',
                "Upload a document that shows what your product is designed to do",
            ),
        ),
    )
    assert product_summary == expected_summary


def test_firearm_on_application_summary(data_standard_case, standard_firearm_expected_product_on_application_summary):
    good_on_application = data_standard_case["case"]["data"]["goods"][0]
    queue_pk = uuid.uuid4()
    product_summary = firearm_on_application_summary(good_on_application, {}, queue_pk)

    assert product_summary == standard_firearm_expected_product_on_application_summary
