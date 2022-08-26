import pytest

from pytest_django.asserts import assertTemplateUsed
from django.urls import reverse


@pytest.fixture(autouse=True)
def default_feature_flags(settings):
    settings.FEATURE_FLAG_NON_FIREARMS_SOFTWARE_ENABLED = True


@pytest.fixture
def software_summary_url(data_standard_case, good_id):
    return reverse(
        "applications:software_product_summary",
        kwargs={
            "pk": data_standard_case["case"]["id"],
            "good_pk": good_id,
        },
    )


@pytest.fixture
def good(data_standard_case):
    return data_standard_case["case"]["data"]["goods"][0]


def test_software_summary_response_status_code(
    authorized_client,
    mock_application_get,
    mock_good_get,
    software_summary_url,
):
    response = authorized_client.get(software_summary_url)
    assert response.status_code == 200


def test_software_summary_template_used(
    authorized_client,
    mock_application_get,
    mock_good_get,
    software_summary_url,
):
    response = authorized_client.get(software_summary_url)
    assertTemplateUsed(response, "applications/goods/software/product-summary.html")


@pytest.fixture
def software_summary(good_id):
    return (
        (
            "product-type",
            "Yes",
            "Is it a firearm product?",
        ),
        (
            "non-firearm-category",
            "It helps to operate a product",
            "Select the product category",
        ),
        (
            "name",
            "p1",
            "Give the product a descriptive name",
        ),
        (
            "is-good-controlled",
            "Yes",
            "Do you know the product's control list entry?",
        ),
        (
            "control-list-entries",
            "ML1a, ML22b",
            "Enter the control list entry",
        ),
        (
            "is-pv-graded",
            "Yes",
            "Does the product have a government security grading or classification?",
        ),
        (
            "pv-grading-prefix",
            "NATO",
            "Enter a prefix (optional)",
        ),
        (
            "pv-grading-grading",
            "Official",
            "What is the security grading or classification?",
        ),
        (
            "pv-grading-suffix",
            "SUFFIX",
            "Enter a suffix (optional)",
        ),
        (
            "pv-grading-issuing-authority",
            "Government entity",
            "Name and address of the issuing authority",
        ),
        (
            "pv-grading-details-reference",
            "GR123",
            "Reference",
        ),
        (
            "pv-grading-details-date-of-issue",
            "20 February 2020",
            "Date of issue",
        ),
        (
            "security-features",
            "Yes",
            "Does the product include security features to protect information?",
        ),
        (
            "security-feature-details",
            "security features",
            "security-feature-details",
        ),
        (
            "declared-at-customs",
            "Yes",
            "Will the product be declared at customs?",
        ),
        (
            "has-product-document",
            "Yes",
            "Do you have a document that shows what your product is and what it’s designed to do?",
        ),
        (
            "is-document-sensitive",
            "No",
            "Is the document rated above Official-sensitive?",
        ),
        (
            "design-details",
            "some design details",
            "Describe the product and what it is designed to do",
        ),
        (
            "product-document",
            f'<a class="govuk-link govuk-link--no-visited-state" href="/goods/{good_id}/documents/6c48a2cc-1ed9-49a5-8ca7-df8af5fc2335/" target="_blank">data_sheet.pdf</a>',
            "Upload a document that shows what your product is designed to do",
        ),
        (
            "product-document-description",
            "product data sheet",
            "Description (optional)",
        ),
        (
            "military-use",
            "Yes",
            "Is the product specially designed or modified for military use?",
        ),
    )


def test_software_product_summary_context(
    authorized_client,
    mock_application_get,
    mock_good_get,
    software_summary_url,
    software_summary,
    data_standard_case,
    good_id,
):
    response = authorized_client.get(software_summary_url)

    def _get_test_url(name):
        if not name:
            return None
        return f'/applications/{data_standard_case["case"]["id"]}/goods/{good_id}/software/edit/{name}/'

    url_map = {
        "name": "name",
        "is-good-controlled": "control-list-entries",
        "control-list-entries": "control-list-entries",
    }

    summary_with_links = tuple(
        (key, value, label, _get_test_url(url_map.get(key, None))) for key, value, label in software_summary
    )
    assert response.context["summary"] == summary_with_links


def test_software_product_on_application_summary_response_status_code(
    authorized_client,
    software_on_application_summary_url,
    mock_application_get,
    mock_good_get,
    mock_good_on_application_get,
    application,
    good_id,
    requests_mock,
):

    response = authorized_client.get(software_on_application_summary_url)
    assert response.status_code == 200


@pytest.fixture
def software_on_application_summary():
    return (
        ("is-onward-exported", "Yes", "Will the product be onward exported to any additional countries?"),
        ("is-altered", "Yes", "Will the item be altered or processed before it is exported again?"),
        ("is-altered-comments", "I will alter it real good", "Explain how the product will be processed or altered"),
        ("is-incorporated", "Yes", "Will the product be incorporated into another item before it is onward exported?"),
        (
            "is-incorporated-comments",
            "I will onward incorporate",
            "Describe what you are incorporating the product into",
        ),
        ("number-of-items", 3, "Number of items"),
        ("total-value", "£16.32", "Total value"),
    )


def test_software_on_application_summary_context(
    authorized_client,
    software_on_application_summary_url,
    mock_application_get,
    mock_good_get,
    mock_good_on_application_get,
    application,
    good,
    good_on_application,
    requests_mock,
    software_summary,
    software_on_application_summary,
):

    response = authorized_client.get(software_on_application_summary_url)
    context = response.context

    assert context["application"] == application
    assert context["good"] == good["good"]
    assert context["good_on_application"] == good_on_application
    assert context["product_summary"] == software_summary
    assert context["product_on_application_summary"] == software_on_application_summary
