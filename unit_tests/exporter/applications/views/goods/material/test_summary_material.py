import pytest

from pytest_django.asserts import assertTemplateUsed


@pytest.fixture
def good(data_standard_case):
    return data_standard_case["case"]["data"]["goods"][0]


def test_material_summary_response_status_code(
    authorized_client,
    mock_application_get,
    mock_good_get,
    material_product_summary_url,
):
    response = authorized_client.get(material_product_summary_url)
    assert response.status_code == 200


def test_material_summary_template_used(
    authorized_client,
    mock_application_get,
    mock_good_get,
    material_product_summary_url,
):
    response = authorized_client.get(material_product_summary_url)
    assertTemplateUsed(response, "applications/goods/material/product-summary.html")


@pytest.fixture
def material_summary(good_id):
    return (
        ("is-firearm-product", "No", "Is it a firearm product?"),
        ("product-category", "It forms part of a product", "Select the product category"),
        ("is-material-substance", "Yes", "Is it a material or substance?"),
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
            "part-number",
            "44",
            "Part number",
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
            "product-document",
            f'<a class="govuk-link govuk-link--no-visited-state" href="/product-list/{good_id}/documents/6c48a2cc-1ed9-49a5-8ca7-df8af5fc2335/" target="_blank">data_sheet.pdf</a>',
            "Upload a document that shows what your product is designed to do",
        ),
        (
            "product-document-description",
            "product data sheet",
            "Description (optional)",
        ),
        (
            "military-use",
            "No",
            "Is the product specially designed or modified for military use?",
        ),
    )


def test_material_product_summary_context(
    authorized_client,
    mock_application_get,
    mock_good_get,
    material_product_summary_url,
    material_summary,
    data_standard_case,
    good_id,
):
    response = authorized_client.get(material_product_summary_url)

    def _get_test_url(name):
        if not name:
            return None
        return f'/applications/{data_standard_case["case"]["id"]}/goods/material/{good_id}/edit/{name}/'

    url_map = {
        "name": "name",
        "is-good-controlled": "control-list-entries",
        "control-list-entries": "control-list-entries",
        "part-number": "part-number",
        "is-pv-graded": "pv-grading",
        "pv-grading-prefix": "pv-grading-details",
        "pv-grading-grading": "pv-grading-details",
        "pv-grading-suffix": "pv-grading-details",
        "pv-grading-issuing-authority": "pv-grading-details",
        "pv-grading-details-reference": "pv-grading-details",
        "pv-grading-details-date-of-issue": "pv-grading-details",
        "has-product-document": "product-document-availability",
        "is-document-sensitive": "product-document-sensitivity",
        "product-document": "product-document",
        "product-document-description": "product-document",
        "military-use": "military-use",
    }

    summary_with_links = tuple(
        (key, value, label, _get_test_url(url_map.get(key, None))) for key, value, label in material_summary
    )
    assert response.context["summary"] == summary_with_links


def test_material_product_on_application_summary_response_status_code(
    authorized_client,
    mock_application_get,
    material_on_application_summary_url,
    mock_good_get,
    mock_good_on_application_get,
    application,
    good_id,
    requests_mock,
):
    response = authorized_client.get(material_on_application_summary_url)
    assert response.status_code == 200


@pytest.fixture
def material_on_application_summary():
    return (
        ("is-onward-exported", "Yes", "Is the product going to any ultimate end-users?"),
        ("is-altered", "Yes", "Will the item be altered or processed before it is exported again?"),
        ("is-altered-comments", "I will alter it real good", "Explain how the product will be processed or altered"),
        ("is-incorporated", "Yes", "Will the product be incorporated into another item before it is onward exported?"),
        (
            "is-incorporated-comments",
            "I will onward incorporate",
            "Describe what you are incorporating the product into",
        ),
        ("unit", "Gram(s)", "Unit of measurement"),
        ("quantity", 3.0, "Quantity"),
        ("total-value", "£16.32", "Total value"),
    )


def test_material_on_application_summary_context(
    authorized_client,
    material_on_application_summary_url,
    mock_application_get,
    mock_good_get,
    mock_good_on_application_get,
    application,
    good,
    good_on_application,
    requests_mock,
    material_summary,
    material_on_application_summary,
):

    response = authorized_client.get(material_on_application_summary_url)
    context = response.context

    def _get_test_url(name):
        if not name:
            return None
        return f"/applications/{application['id']}/goods/material/{good_on_application['id']}/material-on-application-summary/edit/{name}/"

    url_map = {
        "is-onward-exported": "onward-exported",
        "is-altered": "onward-altered",
        "is-altered-comments": "onward-altered",
        "is-incorporated": "onward-incorporated",
        "is-incorporated-comments": "onward-incorporated",
        "unit": "unit-quantity-value",
        "quantity": "unit-quantity-value",
        "total-value": "unit-quantity-value",
    }

    material_on_application_summary_with_links = tuple(
        (key, value, label, _get_test_url(url_map.get(key, None)))
        for key, value, label in material_on_application_summary
    )

    assert context["application"] == application
    assert context["good"] == good["good"]
    assert context["good_on_application"] == good_on_application
    assert context["product_summary"] == material_summary
    assert context["product_on_application_summary"] == material_on_application_summary_with_links
