import pytest

from pytest_django.asserts import assertTemplateUsed

from django.urls import reverse

from core import client
from core.constants import ProductCategories


@pytest.fixture
def component_product_details_url(good_id):
    return reverse(
        "goods:component_detail",
        kwargs={
            "pk": good_id,
        },
    )


@pytest.fixture
def mock_good_get(requests_mock, data_standard_case):
    good = data_standard_case["case"]["data"]["goods"][0]
    good["good"].update(
        {
            "is_pv_graded": {"key": "yes", "value": "Yes"},
            "is_covered_by_firearm_act_section_one_two_or_five": "Yes",
            "item_category": {
                "key": ProductCategories.PRODUCT_CATEGORY_COMPONENT,
            },
        }
    )
    del good["good"]["firearm_details"]
    url = client._build_absolute_uri(f'/goods/{good["good"]["id"]}/')
    return requests_mock.get(url=url, json=good)


def test_component_product_details_status_code(
    authorized_client,
    component_product_details_url,
    mock_good_get,
):
    response = authorized_client.get(component_product_details_url)
    assert response.status_code == 200


def test_component_product_details_template_used(
    authorized_client,
    component_product_details_url,
    mock_good_get,
):
    response = authorized_client.get(component_product_details_url)
    assertTemplateUsed(response, "goods/product-details.html")


def test_component_product_details_context(
    authorized_client,
    component_product_details_url,
    mock_good_get,
):
    response = authorized_client.get(component_product_details_url)
    assert response.context["summary"] == (
        ("is-firearm-product", "No", "Is it a firearm product?"),
        ("product-category", "Component", "Select the product category"),
        ("name", "p1", "Give the product a descriptive name"),
        ("is-component", "Yes", "Is the product a component?"),
        ("component-type", "Modified for hardware", "What type of component is it?"),
        ("modified-details", "modified details", "Provide details of the modifications and the specific hardware"),
        ("is-good-controlled", "Yes", "Do you know the product's control list entry?"),
        ("control-list-entries", "ML1a, ML22b", "Enter the control list entry"),
        ("part-number", "44", "Part number"),
        ("is-pv-graded", "Yes", "Does the product have a government security grading or classification?"),
        ("pv-grading-prefix", "NATO", "Enter a prefix (optional)"),
        ("pv-grading-grading", "Official", "What is the security grading or classification?"),
        ("pv-grading-suffix", "SUFFIX", "Enter a suffix (optional)"),
        ("pv-grading-issuing-authority", "Government entity", "Name and address of the issuing authority"),
        ("pv-grading-details-reference", "GR123", "Reference"),
        ("pv-grading-details-date-of-issue", "20 February 2020", "Date of issue"),
        ("uses-information-security", "No", "Does the product include security features to protect information?"),
        (
            "has-product-document",
            "Yes",
            "Do you have a document that shows what your product is and what it’s designed to do?",
        ),
        ("is-document-sensitive", "No", "Is the document rated above Official-sensitive?"),
        (
            "product-document",
            '<a class="govuk-link govuk-link--no-visited-state" href="/goods/8b730c06-ab4e-401c-aeb0-32b3c92e912c/documents/6c48a2cc-1ed9-49a5-8ca7-df8af5fc2335/" target="_blank">data_sheet.pdf</a>',
            "Upload a document that shows what your product is designed to do",
        ),
        ("product-document-description", "product data sheet", "Description (optional)"),
        ("military-use", "No", "Is the product specially designed or modified for military use?"),
    )
