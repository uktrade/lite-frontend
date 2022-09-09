import uuid

from caseworker.cases.helpers.summaries import (
    firearm_summary,
    firearm_on_application_summary,
    material_summary,
    material_product_on_application_summary,
    platform_summary,
    platform_product_on_application_summary,
    software_summary,
    software_product_on_application_summary,
    component_summary,
    component_product_on_application_summary,
)

from unit_tests.helpers import merge_summaries


def test_firearm_summary(data_standard_case, standard_firearm_expected_product_summary):
    is_user_rfd = False
    good_on_application = data_standard_case["case"]["data"]["goods"][0]
    queue_pk = uuid.uuid4()
    application_pk = good_on_application["application"]
    product_summary = firearm_summary(
        good_on_application["good"],
        queue_pk,
        application_pk,
        is_user_rfd,
        {},
    )

    expected_summary = merge_summaries(
        standard_firearm_expected_product_summary,
        (
            (
                "product-document",
                '<a class="govuk-link govuk-link--no-visited-state" '
                f'href="/queues/{queue_pk}/cases/{application_pk}/documents/6c48a2cc-1ed9-49a5-8ca7-df8af5fc2335/" '
                'target="_blank">data_sheet.pdf</a>',
                "Upload a document that shows what your product is designed to do",
            ),
        ),
    )
    assert product_summary == expected_summary


def test_firearm_on_application_summary(data_standard_case, standard_firearm_expected_product_on_application_summary):
    good_on_application = data_standard_case["case"]["data"]["goods"][0]
    queue_pk = uuid.uuid4()
    application_pk = good_on_application["application"]
    product_summary = firearm_on_application_summary(
        good_on_application,
        queue_pk,
        application_pk,
        {},
    )

    assert product_summary == standard_firearm_expected_product_on_application_summary


def test_platform_summary(data_standard_case, standard_platform_expected_product_summary):
    good_on_application = data_standard_case["case"]["data"]["goods"][0]
    queue_pk = uuid.uuid4()
    application_pk = uuid.uuid4()
    product_summary = platform_summary(
        good_on_application["good"],
        queue_pk,
        application_pk,
    )

    expected_summary = merge_summaries(
        standard_platform_expected_product_summary,
        (
            (
                "product-document",
                '<a class="govuk-link govuk-link--no-visited-state" '
                f'href="/queues/{queue_pk}/cases/{application_pk}/documents/6c48a2cc-1ed9-49a5-8ca7-df8af5fc2335/" '
                'target="_blank">data_sheet.pdf</a>',
                "Upload a document that shows what your product is designed to do",
            ),
        ),
    )
    assert product_summary == expected_summary


def test_platform_product_on_application_summary(
    data_standard_case, standard_platform_expected_product_on_application_summary
):
    good_on_application = data_standard_case["case"]["data"]["goods"][0]
    del good_on_application["firearm_details"]
    good_on_application.update(
        {
            "is_onward_exported": True,
            "is_onward_altered_processed": True,
            "is_onward_altered_processed_comments": "Will be altered",
            "is_onward_incorporated": True,
            "is_onward_incorporated_comments": "Will be incorporated",
        }
    )
    queue_pk = uuid.uuid4()
    application_pk = uuid.uuid4()
    product_summary = platform_product_on_application_summary(good_on_application, queue_pk, application_pk)

    assert product_summary == standard_platform_expected_product_on_application_summary


def test_component_summary(data_standard_case, standard_component_expected_product_summary):
    good_on_application = data_standard_case["case"]["data"]["goods"][0]
    queue_pk = uuid.uuid4()
    application_pk = uuid.uuid4()
    product_summary = component_summary(
        good_on_application["good"],
        queue_pk,
        application_pk,
    )

    expected_summary = merge_summaries(
        standard_component_expected_product_summary,
        (
            (
                "product-document",
                '<a class="govuk-link govuk-link--no-visited-state" '
                f'href="/queues/{queue_pk}/cases/{application_pk}/documents/6c48a2cc-1ed9-49a5-8ca7-df8af5fc2335/" '
                'target="_blank">data_sheet.pdf</a>',
                "Upload a document that shows what your product is designed to do",
            ),
        ),
    )
    assert product_summary == expected_summary


def test_component_product_on_application_summary(
    data_standard_case, standard_platform_expected_product_on_application_summary
):
    good_on_application = data_standard_case["case"]["data"]["goods"][0]
    del good_on_application["firearm_details"]
    good_on_application.update(
        {
            "is_onward_exported": True,
            "is_onward_altered_processed": True,
            "is_onward_altered_processed_comments": "Will be altered",
            "is_onward_incorporated": True,
            "is_onward_incorporated_comments": "Will be incorporated",
        }
    )
    queue_pk = uuid.uuid4()
    application_pk = uuid.uuid4()
    product_summary = component_product_on_application_summary(good_on_application, queue_pk, application_pk)
    assert product_summary == standard_platform_expected_product_on_application_summary


def test_material_summary(data_standard_case, standard_material_expected_product_summary):
    good_on_application = data_standard_case["case"]["data"]["goods"][0]
    queue_pk = uuid.uuid4()
    application_pk = uuid.uuid4()
    product_summary = material_summary(
        good_on_application["good"],
        queue_pk,
        application_pk,
    )

    expected_summary = merge_summaries(
        standard_material_expected_product_summary,
        (
            (
                "product-document",
                '<a class="govuk-link govuk-link--no-visited-state" '
                f'href="/queues/{queue_pk}/cases/{application_pk}/documents/6c48a2cc-1ed9-49a5-8ca7-df8af5fc2335/" '
                'target="_blank">data_sheet.pdf</a>',
                "Upload a document that shows what your product is designed to do",
            ),
        ),
    )
    assert product_summary == expected_summary


def test_material_product_on_application_summary(
    data_standard_case, standard_material_expected_product_on_application_summary
):
    good_on_application = data_standard_case["case"]["data"]["goods"][0]
    del good_on_application["firearm_details"]
    good_on_application.update(
        {
            "is_onward_exported": True,
            "is_onward_altered_processed": True,
            "is_onward_altered_processed_comments": "Will be altered",
            "is_onward_incorporated": True,
            "is_onward_incorporated_comments": "Will be incorporated",
        }
    )
    queue_pk = uuid.uuid4()
    application_pk = uuid.uuid4()
    product_summary = material_product_on_application_summary(good_on_application, queue_pk, application_pk)

    assert product_summary == standard_material_expected_product_on_application_summary


def test_software_summary(data_standard_case, standard_software_expected_product_summary):
    good_on_application = data_standard_case["case"]["data"]["goods"][0]
    queue_pk = uuid.uuid4()
    application_pk = uuid.uuid4()
    product_summary = software_summary(
        good_on_application["good"],
        queue_pk,
        application_pk,
    )

    expected_summary = merge_summaries(
        standard_software_expected_product_summary,
        (
            (
                "product-document",
                '<a class="govuk-link govuk-link--no-visited-state" '
                f'href="/queues/{queue_pk}/cases/{application_pk}/documents/6c48a2cc-1ed9-49a5-8ca7-df8af5fc2335/" '
                'target="_blank">data_sheet.pdf</a>',
                "Upload a document that shows what your product is designed to do",
            ),
        ),
    )
    assert product_summary == expected_summary


def test_software_product_on_application_summary(
    data_standard_case, standard_software_expected_product_on_application_summary
):
    good_on_application = data_standard_case["case"]["data"]["goods"][0]
    del good_on_application["firearm_details"]
    good_on_application.update(
        {
            "is_onward_exported": True,
            "is_onward_altered_processed": True,
            "is_onward_altered_processed_comments": "Will be altered",
            "is_onward_incorporated": True,
            "is_onward_incorporated_comments": "Will be incorporated",
        }
    )
    queue_pk = uuid.uuid4()
    application_pk = uuid.uuid4()
    product_summary = software_product_on_application_summary(good_on_application, queue_pk, application_pk)

    assert product_summary == standard_software_expected_product_on_application_summary
