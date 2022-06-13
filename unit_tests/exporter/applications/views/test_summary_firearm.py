import pytest

from pytest_django.asserts import assertTemplateUsed


@pytest.fixture(autouse=True)
def default_feature_flags(settings):
    settings.FEATURE_FLAG_PRODUCT_2_0 = True


def test_firearm_product_summary_response_status_code(
    authorized_client,
    mock_application_get,
    mock_good_get,
    product_summary_url,
):
    response = authorized_client.get(product_summary_url)
    assert response.status_code == 200


def test_firearm_product_summary_template_used(
    authorized_client,
    mock_application_get,
    mock_good_get,
    product_summary_url,
):
    response = authorized_client.get(product_summary_url)
    assertTemplateUsed(response, "applications/goods/firearms/product-summary.html")


def test_firearm_product_summary_context(
    authorized_client,
    mock_application_get,
    mock_good_get,
    product_summary_url,
    data_standard_case,
    good_id,
):
    response = authorized_client.get(product_summary_url)

    def _get_test_url(name):
        return f'/applications/{data_standard_case["case"]["id"]}/goods/{good_id}/firearm/edit/{name}/'

    assert response.context["summary"] == (
        (
            "firearm-type",
            "Firearms",
            "Select the type of firearm product",
            None,
        ),
        (
            "firearm-category",
            "Non automatic shotgun, Non automatic rim-fired handgun",
            "Firearm category",
            _get_test_url("category"),
        ),
        (
            "name",
            "p1",
            "Give the product a descriptive name",
            _get_test_url("name"),
        ),
        (
            "is-good-controlled",
            "Yes",
            "Do you know the product's control list entry?",
            _get_test_url("control-list-entries"),
        ),
        (
            "control-list-entries",
            "ML1a, ML22b",
            "Enter the control list entry",
            _get_test_url("control-list-entries"),
        ),
        (
            "is-pv-graded",
            "Yes",
            "Does the product have a government security grading or classification?",
            _get_test_url("pv-grading"),
        ),
        (
            "pv-grading-prefix",
            "NATO",
            "Enter a prefix (optional)",
            _get_test_url("pv-grading"),
        ),
        (
            "pv-grading-grading",
            "Official",
            "What is the security grading or classification?",
            _get_test_url("pv-grading"),
        ),
        (
            "pv-grading-suffix",
            "SUFFIX",
            "Enter a suffix (optional)",
            _get_test_url("pv-grading"),
        ),
        (
            "pv-grading-issuing-authority",
            "Government entity",
            "Name and address of the issuing authority",
            _get_test_url("pv-grading"),
        ),
        (
            "pv-grading-details-reference",
            "GR123",
            "Reference",
            _get_test_url("pv-grading"),
        ),
        (
            "pv-grading-details-date-of-issue",
            "20 February 2020",
            "Date of issue",
            _get_test_url("pv-grading"),
        ),
        (
            "calibre",
            "0.25",
            "What is the calibre of the product?",
            _get_test_url("calibre"),
        ),
        (
            "is-replica",
            "No",
            "Is the product a replica firearm?",
            _get_test_url("replica"),
        ),
        (
            "is-registered-firearms-dealer",
            "No",
            "Are you a registered firearms dealer?",
            _get_test_url("registered-firearms-dealer"),
        ),
        (
            "is-covered-by-firearm-act-section-one-two-or-five-explanation",
            "No firearm act section",
            "Explain",
            _get_test_url("firearms-act-1968"),
        ),
        (
            "has-product-document",
            "Yes",
            "Do you have a document that shows what your product is and what it’s designed to do?",
            _get_test_url("product-document-availability"),
        ),
        (
            "is-document-sensitive",
            "No",
            "Is the document rated above Official-sensitive?",
            _get_test_url("product-document-sensitivity"),
        ),
        (
            "product-document",
            f'<a class="govuk-link govuk-link--no-visited-state" href="/goods/{good_id}/documents/6c48a2cc-1ed9-49a5-8ca7-df8af5fc2335/" target="_blank">data_sheet.pdf</a>',
            "Upload a document that shows what your product is designed to do",
            _get_test_url("product-document"),
        ),
        (
            "product-document-description",
            "product data sheet",
            "Description (optional)",
            _get_test_url("product-document"),
        ),
    )
