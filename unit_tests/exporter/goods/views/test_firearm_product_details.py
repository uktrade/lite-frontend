import pytest

from pytest_django.asserts import assertTemplateUsed

from django.urls import reverse

from core import client


@pytest.fixture(autouse=True)
def default_feature_flags(settings):
    settings.FEATURE_FLAG_PRODUCT_2_0 = True


@pytest.fixture
def firearm_product_details_url(good_id):
    return reverse(
        "goods:firearm_detail",
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
    good["good"]["firearm_details"].update(
        {
            "is_covered_by_firearm_act_section_one_two_or_five": "Yes",
            "firearms_act_section": "firearms_act_section5",
            "section_certificate_missing": True,
            "section_certificate_missing_reason": "No section 5 certificate",
        }
    )
    url = client._build_absolute_uri(f'/goods/{good["good"]["id"]}/')
    return requests_mock.get(url=url, json=good)


def test_firearm_product_details_template_used(
    authorized_client,
    firearm_product_details_url,
    mock_good_get,
):
    response = authorized_client.get(firearm_product_details_url)
    assert response.status_code == 200
    assertTemplateUsed("goods/product-details.html")


def test_firearm_product_details_context(
    authorized_client,
    firearm_product_details_url,
    mock_good_get,
):

    response = authorized_client.get(firearm_product_details_url)
    assert response.status_code == 200
    assert response.context["summary"] == (
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
            "firearms-act-1968-section",
            "Section 5",
            "Which section of the Firearms Act 1968 is the product covered by?",
        ),
        (
            "section-5-certificate-missing",
            "I do not have a section 5 letter of authority",
            "Upload your section 5 letter of authority",
        ),
        (
            "section-5-certificate-missing-reason",
            "No section 5 certificate",
            "Explain why you do not have a section 5 letter of authority",
        ),
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
    )
