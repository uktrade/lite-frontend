import uuid

from core.constants import (
    FirearmsActDocumentType,
    FirearmsActSections,
    OrganisationDocumentType,
)
from caseworker.cases.helpers.summaries import (
    firearm_summary,
    firearm_on_application_summary,
    material_summary,
    material_product_on_application_summary,
    platform_summary,
    platform_product_on_application_summary,
    technology_summary,
    technology_product_on_application_summary,
    component_accessory_summary,
    component_accessory_product_on_application_summary,
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


def test_firearm_summary_with_section_5_and_rfd_certificates(data_standard_case):
    is_user_rfd = True
    good_on_application = data_standard_case["case"]["data"]["goods"][0]
    good = good_on_application["good"]
    good["firearm_details"].update(
        {
            "firearms_act_section": FirearmsActSections.SECTION_5,
            "section_certificate_missing": False,
            "section_certificate_number": "section-certificate-number",
            "section_certificate_date_of_expiry": "2030-10-09",
        }
    )
    queue_pk = uuid.uuid4()
    application_pk = good_on_application["application"]
    product_summary = firearm_summary(
        good,
        queue_pk,
        application_pk,
        is_user_rfd,
        {
            FirearmsActDocumentType.SECTION_5: {
                "document": {
                    "id": "section-5-id",
                    "name": "Section 5 document",
                    "safe": True,
                },
                "reference_code": "section-certificate-number",
                "expiry_date": "9 October 2030",
            },
            OrganisationDocumentType.RFD_CERTIFICATE: {
                "document": {
                    "id": "rfd-certificate-id",
                    "name": "RFD certificate",
                    "safe": True,
                },
                "reference_code": "REF123",
                "expiry_date": "31 May 2025",
            },
        },
    )

    expected_summary = (
        ("firearm-type", "Firearms", "Select the type of firearm product"),
        ("firearm-category", "Non automatic shotgun, Non automatic rim-fired handgun", "Firearm category"),
        ("name", "p1", "Give the product a descriptive name"),
        ("is-good-controlled", "Yes", "Do you know the product's control list entry?"),
        ("control-list-entries", "ML1a, ML22b", "Enter the control list entry"),
        ("is-pv-graded", "Yes", "Does the product have a government security grading or classification?"),
        ("pv-grading-prefix", "NATO", "Enter a prefix (optional)"),
        ("pv-grading-grading", "Official", "What is the security grading or classification?"),
        ("pv-grading-suffix", "SUFFIX", "Enter a suffix (optional)"),
        ("pv-grading-issuing-authority", "Government entity", "Name and address of the issuing authority"),
        ("pv-grading-details-reference", "GR123", "Reference"),
        ("pv-grading-details-date-of-issue", "20 February 2020", "Date of issue"),
        ("calibre", "0.25", "What is the calibre of the product?"),
        ("is-replica", "No", "Is the product a replica firearm?"),
        ("is-registered-firearms-dealer", "Yes", "Are you a registered firearms dealer?"),
        (
            "rfd-certificate-document",
            f'<a class="govuk-link govuk-link--no-visited-state" href="/queues/{queue_pk}/cases/{application_pk}/documents/rfd-certificate-id/" target="_blank">RFD certificate</a>',
            "Upload a registered firearms dealer certificate",
        ),
        ("rfd-certificate-reference-number", "REF123", "Certificate reference number"),
        ("rfd-certificate-date-of-expiry", "31 May 2025", "Certificate date of expiry"),
        (
            "is-covered-by-firearm-act-section-five",
            "Don't know",
            "Is the product covered by section 5 of the Firearms Act 1968?",
        ),
        (
            "section-5-certificate-document",
            f'<a class="govuk-link govuk-link--no-visited-state" href="/queues/{queue_pk}/cases/{application_pk}/documents/section-5-id/" target="_blank">Section 5 document</a>',
            "Upload your section 5 letter of authority",
        ),
        ("section-5-certificate-reference-number", "section-certificate-number", "Certificate reference number"),
        ("section-5-certificate-date-of-expiry", "9 October 2030", "Certificate date of expiry"),
        (
            "has-product-document",
            "Yes",
            "Do you have a document that shows what your product is and what it’s " "designed to do?",
        ),
        ("is-document-sensitive", "No", "Is the document rated above Official-sensitive?"),
        (
            "product-document",
            f'<a class="govuk-link govuk-link--no-visited-state" href="/queues/{queue_pk}/cases/{application_pk}/documents/6c48a2cc-1ed9-49a5-8ca7-df8af5fc2335/" target="_blank">data_sheet.pdf</a>',
            "Upload a document that shows what your product is designed to do",
        ),
        ("product-document-description", "product data sheet", "Description (optional)"),
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


def test_component_accessory_summary(data_standard_case, standard_component_accessory_expected_product_summary):
    good_on_application = data_standard_case["case"]["data"]["goods"][0]
    queue_pk = uuid.uuid4()
    application_pk = uuid.uuid4()
    product_summary = component_accessory_summary(
        good_on_application["good"],
        queue_pk,
        application_pk,
    )

    expected_summary = merge_summaries(
        standard_component_accessory_expected_product_summary,
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


def test_component_accessory_product_on_application_summary(
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
    product_summary = component_accessory_product_on_application_summary(good_on_application, queue_pk, application_pk)
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


def test_technology_summary(data_standard_case, standard_technology_expected_product_summary):
    good_on_application = data_standard_case["case"]["data"]["goods"][0]
    queue_pk = uuid.uuid4()
    application_pk = uuid.uuid4()
    product_summary = technology_summary(
        good_on_application["good"],
        queue_pk,
        application_pk,
    )

    expected_summary = merge_summaries(
        standard_technology_expected_product_summary,
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


def test_technology_product_on_application_summary(
    data_standard_case, standard_technology_expected_product_on_application_summary
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
    product_summary = technology_product_on_application_summary(good_on_application, queue_pk, application_pk)

    assert product_summary == standard_technology_expected_product_on_application_summary
