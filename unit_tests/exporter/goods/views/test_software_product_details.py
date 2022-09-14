import pytest

from pytest_django.asserts import assertTemplateUsed

from django.urls import reverse

from core import client


@pytest.fixture
def software_product_details_url(good_id):
    return reverse(
        "goods:software_detail",
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
        }
    )
    del good["good"]["firearm_details"]
    url = client._build_absolute_uri(f'/goods/{good["good"]["id"]}/')
    return requests_mock.get(url=url, json=good)


def test_software_product_details_template_used(
    authorized_client,
    software_product_details_url,
    mock_good_get,
):
    response = authorized_client.get(software_product_details_url)
    assert response.status_code == 200
    assertTemplateUsed("goods/product-details.html")


def test_software_product_details_context(
    authorized_client,
    software_product_details_url,
    mock_good_get,
):

    response = authorized_client.get(software_product_details_url)
    assert response.status_code == 200
    assert response.context["summary"] == (
        ("product-type", "Yes", "Is it a firearm product?"),
        ("non-firearm-category", "It helps to operate a product", "Select the product category"),
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
        ("security-features", "Yes", "Does the product include security features to protect information?"),
        (
            "security-feature-details",
            "security features",
            "Provide details of the information security features",
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
        ("is-document-sensitive", "No", "Is the document rated above Official-sensitive?"),
        (
            "design-details",
            "some design details",
            "Describe the product and what it is designed to do",
        ),
        (
            "product-document",
            '<a class="govuk-link govuk-link--no-visited-state" href="/goods/8b730c06-ab4e-401c-aeb0-32b3c92e912c/documents/6c48a2cc-1ed9-49a5-8ca7-df8af5fc2335/" target="_blank">data_sheet.pdf</a>',
            "Upload a document that shows what your product is designed to do",
        ),
        ("product-document-description", "product data sheet", "Description (optional)"),
        ("military-use", "No", "Is the product specially designed or modified for military use?"),
    )
