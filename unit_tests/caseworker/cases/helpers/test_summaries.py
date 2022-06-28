import uuid

from caseworker.cases.helpers.summaries import (
    firearm_product_summary,
    firearm_product_on_application_summary,
)


def test_firearm_product_summary(data_standard_case):
    is_user_rfd = False
    good_on_application = data_standard_case["case"]["data"]["goods"][0]
    queue_pk = uuid.uuid4()
    product_summary = firearm_product_summary(good_on_application, is_user_rfd, [], queue_pk)

    assert product_summary == (
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
        ("is-registered-firearms-dealer", "No", "Are you a registered firearms dealer?"),
        (
            "is-covered-by-firearm-act-section-one-two-or-five-explanation",
            "Not covered by firearm act sections",
            "Explain",
        ),
        (
            "has-product-document",
            "Yes",
            "Do you have a document that shows what your product is and what it’s " "designed to do?",
        ),
        ("is-document-sensitive", "No", "Is the document rated above Official-sensitive?"),
        (
            "product-document",
            '<a class="govuk-link govuk-link--no-visited-state" '
            f'href="/queues/{queue_pk}/cases/8fb76bed-fd45-4293-95b8-eda9468aa254/documents/6c48a2cc-1ed9-49a5-8ca7-df8af5fc2335/" '
            'target="_blank">data_sheet.pdf</a>',
            "Upload a document that shows what your product is designed to do",
        ),
        ("product-document-description", "product data sheet", "Description (optional)"),
    )


def test_firearm_product_on_application_summary(data_standard_case):
    good_on_application = data_standard_case["case"]["data"]["goods"][0]
    queue_pk = uuid.uuid4()
    product_summary = firearm_product_on_application_summary(good_on_application, [], queue_pk)

    assert product_summary == (
        ("manufacture-year", "1990", "What year was it made?"),
        ("is-onward-exported", "No", "Will the product be onward exported to any additional countries?"),
        ("is-deactivated", "No", "Has the product been deactivated?"),
        ("number-of-items", 2, "Number of items"),
        ("total-value", "£444.00", "Total value"),
        (
            "has-serial-numbers",
            "Yes, I can add serial numbers now",
            "Will each product have a serial number or other identification marking?",
        ),
        (
            "serial-numbers",
            "\n"
            "\n"
            "\n"
            '    <details class="govuk-details govuk-!-margin-bottom-0" '
            'data-module="govuk-details">\n'
            '        <summary class="govuk-details__summary">\n'
            '            <span class="govuk-details__summary-text">\n'
            "                View serial numbers\n"
            "            </span>\n"
            "        </summary>\n"
            '        <div class="govuk-details__text">\n'
            "            \n"
            "                1. 12345  <br> \n"
            "            \n"
            "                2. ABC-123 \n"
            "            \n"
            "        </div>\n"
            "    </details>\n"
            "\n",
            "Enter serial numbers or other identification markings",
        ),
    )
