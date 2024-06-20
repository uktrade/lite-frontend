import pytest

from pytest_django.asserts import assertTemplateUsed


def test_firearm_summary_response_status_code(
    authorized_client,
    mock_application_get,
    mock_good_get,
    firearm_product_summary_url,
):
    response = authorized_client.get(firearm_product_summary_url)
    assert response.status_code == 200


def test_firearm_summary_template_used(
    authorized_client,
    mock_application_get,
    mock_good_get,
    firearm_product_summary_url,
):
    response = authorized_client.get(firearm_product_summary_url)
    assertTemplateUsed(response, "applications/goods/firearms/product-summary.html")


@pytest.fixture
def product_summary(good_id):
    return (
        (
            "firearm-type",
            "Firearms",
            "Select the type of firearm product",
        ),
        (
            "firearm-category",
            "Non automatic shotgun, Non automatic rim-fired handgun",
            "Firearm category",
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
            "calibre",
            "0.25",
            "What is the calibre of the product?",
        ),
        (
            "is-replica",
            "No",
            "Is the product a replica firearm?",
        ),
        (
            "is-registered-firearms-dealer",
            "No",
            "Are you a registered firearms dealer?",
        ),
        (
            "firearms-act-1968-section",
            "Don't know",
            "Which section of the Firearms Act 1968 is the product covered by?",
        ),
        (
            "is-covered-by-firearm-act-section-one-two-or-five-explanation",
            "No firearm act section",
            "Explain",
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
    )


def test_firearm_summary_context(
    authorized_client,
    mock_application_get,
    mock_good_get,
    firearm_product_summary_url,
    data_standard_case,
    good_id,
    product_summary,
):
    response = authorized_client.get(firearm_product_summary_url)

    def _get_test_url(name):
        if not name:
            return None
        return f'/applications/{data_standard_case["case"]["id"]}/goods/firearm/{good_id}/edit/{name}/'

    url_map = {
        "firearm-category": "category",
        "name": "name",
        "is-good-controlled": "control-list-entries",
        "control-list-entries": "control-list-entries",
        "is-pv-graded": "pv-grading",
        "pv-grading-prefix": "pv-grading-details",
        "pv-grading-grading": "pv-grading-details",
        "pv-grading-suffix": "pv-grading-details",
        "pv-grading-issuing-authority": "pv-grading-details",
        "pv-grading-details-reference": "pv-grading-details",
        "pv-grading-details-date-of-issue": "pv-grading-details",
        "calibre": "calibre",
        "is-replica": "replica",
        "is-registered-firearms-dealer": "registered-firearms-dealer",
        "firearms-act-1968-section": "firearms-act-1968",
        "is-covered-by-firearm-act-section-one-two-or-five-explanation": "firearms-act-1968",
        "has-product-document": "product-document-availability",
        "is-document-sensitive": "product-document-sensitivity",
        "product-document": "product-document",
        "product-document-description": "product-document",
    }

    summary_with_links = tuple(
        (key, value, label, _get_test_url(url_map.get(key, None))) for key, value, label in product_summary
    )
    assert response.context["summary"] == summary_with_links


def test_firearm_on_application_summary_response_status_code(
    authorized_client,
    product_on_application_summary_url,
    mock_application_get,
    mock_good_get,
    mock_good_on_application_get,
    application,
    good_id,
    requests_mock,
):
    requests_mock.get(
        f"/applications/{application['id']}/goods/{good_id}/documents/",
        json={"documents": []},
    )
    requests_mock.get(
        f"/goods/{good_id}/documents/",
        json={},
    )
    response = authorized_client.get(product_on_application_summary_url)
    assert response.status_code == 200


@pytest.fixture
def good(data_standard_case):
    return data_standard_case["case"]["data"]["goods"][0]


@pytest.fixture
def product_on_application_summary():
    return (
        ("made-before-1938", "Yes", "Was the product made before 1938?"),
        ("manufacture-year", 1930, "What year was it made?"),
        ("is-onward-exported", "Yes", "Is the product going to any ultimate end-users?"),
        ("is-altered", "Yes", "Will the item be altered or processed before it is exported again?"),
        ("is-altered-comments", "I will alter it real good", "Explain how the product will be processed or altered"),
        ("is-incorporated", "Yes", "Will the product be incorporated into another item before it is onward exported?"),
        (
            "is-incorporated-comments",
            "I will onward incorporate",
            "Describe what you are incorporating the product into",
        ),
        ("is-deactivated", "Yes", "Has the product been deactivated?"),
        ("deactivated-date", "12 December 2007", "When was the item deactivated?"),
        ("is-proof-standards", "No", "Has the item been deactivated to UK proof house standards?"),
        (
            "is-proof-standards-comments",
            "Not deactivated",
            "Describe who deactivated the product and to what standard it was done",
        ),
        ("number-of-items", 3, "Number of items"),
        ("total-value", "£16.32", "Total value"),
        ("has-serial-numbers", "No", "Will each product have a serial number or other identification marking?"),
        ("no-identification-markings-details", "No markings", "Explain why the product has not been marked"),
    )


def test_firearm_on_application_summary_context(
    authorized_client,
    product_on_application_summary_url,
    mock_application_get,
    mock_good_get,
    mock_good_on_application_get,
    application,
    good,
    good_on_application,
    requests_mock,
    product_summary,
    product_on_application_summary,
):
    requests_mock.get(
        f"/applications/{application['id']}/goods/{good['good']['id']}/documents/",
        json={"documents": []},
    )
    requests_mock.get(
        f"/goods/{good['good']['id']}/documents/",
        json={"documents": []},
    )
    response = authorized_client.get(product_on_application_summary_url)
    context = response.context

    def _get_test_url(name):
        if not name:
            return None
        return f"/applications/{application['id']}/goods/firearm/{good_on_application['id']}/product-on-application-summary/edit/{name}/"

    url_map = {
        "made-before-1938": "made-before-1938",
        "manufacture-year": "year-of-manufacture",
        "is-onward-exported": "onward-exported",
        "is-altered": "onward-altered",
        "is-altered-comments": "onward-altered",
        "is-incorporated": "onward-incorporated",
        "is-incorporated-comments": "onward-incorporated",
        "is-deactivated": "is-deactivated",
        "deactivated-date": "is-deactivated",
        "is-proof-standards": "is-deactivated-to-standard",
        "is-proof-standards-comments": "is-deactivated-to-standard",
        "number-of-items": "quantity-value",
        "total-value": "quantity-value",
        "has-serial-numbers": "serial-identification-markings",
        "no-identification-markings-details": "serial-identification-markings",
    }

    product_on_application_summary_with_links = tuple(
        (key, value, label, _get_test_url(url_map.get(key, None)))
        for key, value, label in product_on_application_summary
    )

    assert context["application"] == application
    assert context["good"] == good["good"]
    assert context["good_on_application"] == good_on_application
    assert context["product_summary"] == product_summary
    assert context["product_on_application_summary"] == product_on_application_summary_with_links


def test_firearm_attach_product_on_application_summary_response_status_code(
    authorized_client,
    attach_product_on_application_summary_url,
    mock_application_get,
    mock_good_get,
    mock_good_on_application_get,
    application,
    good_id,
    requests_mock,
):
    requests_mock.get(
        f"/applications/{application['id']}/goods/{good_id}/documents/",
        json={"documents": []},
    )
    requests_mock.get(
        f"/goods/{good_id}/documents/",
        json={},
    )
    response = authorized_client.get(attach_product_on_application_summary_url)
    assert response.status_code == 200


def test_firearm_attach_product_on_application_summary_context(
    authorized_client,
    attach_product_on_application_summary_url,
    mock_application_get,
    mock_good_get,
    mock_good_on_application_get,
    application,
    good,
    good_on_application,
    requests_mock,
    product_summary,
    product_on_application_summary,
):
    requests_mock.get(
        f"/applications/{application['id']}/goods/{good['good']['id']}/documents/",
        json={"documents": []},
    )
    requests_mock.get(
        f"/goods/{good['good']['id']}/documents/",
        json={"documents": []},
    )
    response = authorized_client.get(attach_product_on_application_summary_url)
    context = response.context

    def _get_test_url(name):
        if not name:
            return None
        return f"/applications/{application['id']}/goods/firearm/{good_on_application['id']}/attach-product-on-application-summary/edit/{name}/"

    url_map = {
        "made-before-1938": "made-before-1938",
        "manufacture-year": "year-of-manufacture",
        "is-onward-exported": "onward-exported",
        "is-altered": "onward-altered",
        "is-altered-comments": "onward-altered",
        "is-incorporated": "onward-incorporated",
        "is-incorporated-comments": "onward-incorporated",
        "is-deactivated": "is-deactivated",
        "deactivated-date": "is-deactivated",
        "is-proof-standards": "is-deactivated-to-standard",
        "is-proof-standards-comments": "is-deactivated-to-standard",
        "number-of-items": "quantity-value",
        "total-value": "quantity-value",
        "has-serial-numbers": "serial-identification-markings",
        "no-identification-markings-details": "serial-identification-markings",
    }

    product_on_application_summary_with_links = tuple(
        (key, value, label, _get_test_url(url_map.get(key, None)))
        for key, value, label in product_on_application_summary
    )

    assert context["application"] == application
    assert context["good"] == good["good"]
    assert context["good_on_application"] == good_on_application
    assert context["product_summary"] == product_summary
    assert context["product_on_application_summary"] == product_on_application_summary_with_links


def test_firearm_attach_product_on_application_summary_context_get_requests(
    authorized_client,
    attach_product_on_application_summary_url,
    mock_application_get,
    mock_good_get,
    mock_good_on_application_get,
    application,
    good,
    good_on_application,
    requests_mock,
    product_summary,
    product_on_application_summary,
):
    requests_mock.get(
        f"/applications/{application['id']}/goods/{good['good']['id']}/documents/",
        json={"documents": []},
    )
    requests_mock.get(
        f"/goods/{good['good']['id']}/documents/",
        json={"documents": []},
    )
    response = authorized_client.get(
        f"{attach_product_on_application_summary_url}?added_firearm_category=1&confirmed_rfd_validity=1",
    )
    context = response.context

    def _get_test_url(name):
        if not name:
            return None
        return f"/applications/{application['id']}/goods/firearm/{good_on_application['id']}/attach-product-on-application-summary/edit/{name}/"

    url_map = {
        "made-before-1938": "made-before-1938",
        "manufacture-year": "year-of-manufacture",
        "is-onward-exported": "onward-exported",
        "is-altered": "onward-altered",
        "is-altered-comments": "onward-altered",
        "is-incorporated": "onward-incorporated",
        "is-incorporated-comments": "onward-incorporated",
        "is-deactivated": "is-deactivated",
        "deactivated-date": "is-deactivated",
        "is-proof-standards": "is-deactivated-to-standard",
        "is-proof-standards-comments": "is-deactivated-to-standard",
        "number-of-items": "quantity-value",
        "total-value": "quantity-value",
        "has-serial-numbers": "serial-identification-markings",
        "no-identification-markings-details": "serial-identification-markings",
    }

    product_on_application_summary_with_links = tuple(
        (key, value, label, _get_test_url(url_map.get(key, None)))
        for key, value, label in product_on_application_summary
    )

    assert (
        context["product_on_application_summary"]
        == (
            (
                "firearm-category",
                "Non automatic shotgun, Non automatic rim-fired handgun",
                "Firearm category",
                None,
            ),
            (
                "confirm-rfd-validity",
                "Yes",
                "Is your registered firearms dealer certificate still valid?",
                None,
            ),
        )
        + product_on_application_summary_with_links
    )

    assert (
        "firearm-category",
        "Non automatic shotgun, Non automatic rim-fired handgun",
        "Firearm category",
    ) not in context["product_summary"]
