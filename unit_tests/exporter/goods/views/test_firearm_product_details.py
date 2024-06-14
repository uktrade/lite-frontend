import datetime
import pytest

from pytest_django.asserts import assertTemplateUsed

from django.urls import reverse

from core import client
from core.constants import OrganisationDocumentType


@pytest.fixture
def firearm_product_details_url(good_id):
    return reverse(
        "goods:firearm_detail",
        kwargs={
            "pk": good_id,
        },
    )


@pytest.fixture
def firearm_ammunition_product_details_url(good_id):
    return reverse(
        "goods:firearm_ammunition_detail",
        kwargs={
            "pk": good_id,
        },
    )


@pytest.fixture
def components_for_firearm_product_details_url(good_id):
    return reverse(
        "goods:components_for_firearms_detail",
        kwargs={
            "pk": good_id,
        },
    )


@pytest.fixture
def components_for_ammunition_product_details_url(good_id):
    return reverse(
        "goods:components_for_firearms_ammunition_detail",
        kwargs={
            "pk": good_id,
        },
    )


@pytest.fixture
def firearm_accessory_product_details_url(good_id):
    return reverse(
        "goods:firearms_accessory_detail",
        kwargs={
            "pk": good_id,
        },
    )


@pytest.fixture
def software_related_to_firearm_product_details_url(good_id):
    return reverse(
        "goods:software_related_to_firearms_detail",
        kwargs={
            "pk": good_id,
        },
    )


@pytest.fixture
def technology_related_to_firearm_product_details_url(good_id):
    return reverse(
        "goods:technology_related_to_firearms_detail",
        kwargs={
            "pk": good_id,
        },
    )


@pytest.fixture
def mock_get_organisation_with_rfd(requests_mock, mock_exporter_user_me, data_standard_case):
    organisation = data_standard_case["case"]["data"]["organisation"]
    expiry_date = datetime.date.today() + datetime.timedelta(days=100)
    organisation["id"] = mock_exporter_user_me["organisations"][0]["id"]
    organisation["name"] = mock_exporter_user_me["organisations"][0]["name"]
    organisation["documents"].extend(
        [
            {
                "id": "b4a2da59-c0bc-4b6d-8ed9-4ca28ffbf65a",
                "document_type": OrganisationDocumentType.RFD_CERTIFICATE,
                "expiry_date": expiry_date.strftime("%d %B %Y"),
                "reference_code": "RFD123",
                "is_expired": False,
                "document": {
                    "id": "9c2222db-98e5-47e8-9e01-653354e95322",
                    "name": "rfd_certificate.txt",
                    "s3_key": "rfd_certificate.txt.s3_key",
                    "size": 0,
                    "safe": True,
                },
            }
        ]
    )

    url = client._build_absolute_uri(f"/organisations/{organisation['id']}")
    requests_mock.get(url=url, json=organisation)
    yield organisation


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


@pytest.fixture
def mock_firearm_ammunition_good_get(requests_mock, data_standard_case):
    good = data_standard_case["case"]["data"]["goods"][0]
    good["good"].update(
        {
            "is_pv_graded": {"key": "yes", "value": "Yes"},
            "is_covered_by_firearm_act_section_one_two_or_five": "Yes",
        }
    )
    good["good"]["firearm_details"].update(
        {
            "type": {"key": "ammunition", "value": "Ammunition"},
            "is_covered_by_firearm_act_section_one_two_or_five": "Yes",
            "firearms_act_section": "firearms_act_section5",
            "section_certificate_missing": True,
            "section_certificate_missing_reason": "No section 5 certificate",
        }
    )
    del good["good"]["firearm_details"]["category"]
    url = client._build_absolute_uri(f'/goods/{good["good"]["id"]}/')
    return requests_mock.get(url=url, json=good)


@pytest.fixture
def mock_components_for_firearm_good_get(requests_mock, data_standard_case):
    good = data_standard_case["case"]["data"]["goods"][0]
    good["good"].update(
        {
            "is_pv_graded": {"key": "yes", "value": "Yes"},
            "is_covered_by_firearm_act_section_one_two_or_five": "Yes",
        }
    )
    good["good"]["firearm_details"].update(
        {
            "type": {"key": "components_for_firearms", "value": "Components for firearms"},
            "is_covered_by_firearm_act_section_one_two_or_five": "Yes",
            "firearms_act_section": "firearms_act_section5",
            "section_certificate_missing": True,
            "section_certificate_missing_reason": "No section 5 certificate",
        }
    )
    del good["good"]["firearm_details"]["category"]
    url = client._build_absolute_uri(f'/goods/{good["good"]["id"]}/')
    return requests_mock.get(url=url, json=good)


@pytest.fixture
def mock_components_for_ammunition_good_get(requests_mock, data_standard_case):
    good = data_standard_case["case"]["data"]["goods"][0]
    good["good"].update(
        {
            "is_pv_graded": {"key": "yes", "value": "Yes"},
            "is_covered_by_firearm_act_section_one_two_or_five": "Yes",
        }
    )
    good["good"]["firearm_details"].update(
        {
            "type": {"key": "components_for_ammunition", "value": "Components for ammunition"},
            "is_covered_by_firearm_act_section_one_two_or_five": "Yes",
            "firearms_act_section": "firearms_act_section5",
            "section_certificate_missing": True,
            "section_certificate_missing_reason": "No section 5 certificate",
        }
    )
    del good["good"]["firearm_details"]["category"]
    url = client._build_absolute_uri(f'/goods/{good["good"]["id"]}/')
    return requests_mock.get(url=url, json=good)


@pytest.fixture
def mock_firearm_accessory_good_get(requests_mock, data_standard_case):
    good = data_standard_case["case"]["data"]["goods"][0]
    good["good"].update(
        {
            "is_pv_graded": {"key": "yes", "value": "Yes"},
        }
    )
    good["good"]["firearm_details"].update(
        {
            "type": {"key": "firearms_accessory", "value": "Accessory of a firearm"},
        }
    )
    del good["good"]["firearm_details"]["category"]
    url = client._build_absolute_uri(f'/goods/{good["good"]["id"]}/')
    return requests_mock.get(url=url, json=good)


@pytest.fixture
def mock_software_related_to_firearm_good_get(requests_mock, data_standard_case):
    good = data_standard_case["case"]["data"]["goods"][0]
    good["good"].update(
        {
            "is_pv_graded": {"key": "yes", "value": "Yes"},
        }
    )
    good["good"]["firearm_details"].update(
        {
            "type": {"key": "software_related_to_firearms", "value": "Software relating to a firearm"},
        }
    )
    del good["good"]["firearm_details"]["category"]
    url = client._build_absolute_uri(f'/goods/{good["good"]["id"]}/')
    return requests_mock.get(url=url, json=good)


@pytest.fixture
def mock_technology_related_to_firearm_good_get(requests_mock, data_standard_case):
    good = data_standard_case["case"]["data"]["goods"][0]
    good["good"].update(
        {
            "is_pv_graded": {"key": "yes", "value": "Yes"},
        }
    )
    good["good"]["firearm_details"].update(
        {
            "type": {"key": "technology_related_to_firearms", "value": "Technology relating to a firearm"},
        }
    )
    del good["good"]["firearm_details"]["category"]
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
    mock_get_organisation_with_rfd,
    mock_good_get,
):

    response = authorized_client.get(firearm_product_details_url)
    assert response.status_code == 200

    expiry_date = datetime.date.today() + datetime.timedelta(days=100)
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
        ("is-registered-firearms-dealer", "Yes", "Are you a registered firearms dealer?"),
        (
            "rfd-certificate-document",
            '<a class="govuk-link govuk-link--no-visited-state" '
            'href="/product-list/8b730c06-ab4e-401c-aeb0-32b3c92e912c/documents/b4a2da59-c0bc-4b6d-8ed9-4ca28ffbf65a/" '
            'target="_blank">rfd_certificate.txt</a>',
            "Upload a registered firearms dealer certificate",
        ),
        ("rfd-certificate-reference-number", "RFD123", "Certificate reference number"),
        ("rfd-certificate-date-of-expiry", expiry_date.strftime("%d %B %Y"), "Certificate date of expiry"),
        (
            "is-covered-by-firearm-act-section-five",
            "Yes",
            "Is the product covered by section 5 of the Firearms Act 1968?",
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
            '<a class="govuk-link govuk-link--no-visited-state" href="/product-list/8b730c06-ab4e-401c-aeb0-32b3c92e912c/documents/6c48a2cc-1ed9-49a5-8ca7-df8af5fc2335/" target="_blank">data_sheet.pdf</a>',
            "Upload a document that shows what your product is designed to do",
        ),
        ("product-document-description", "product data sheet", "Description (optional)"),
    )


def test_firearm_ammunition_product_details_context(
    authorized_client,
    firearm_ammunition_product_details_url,
    mock_get_organisation_with_rfd,
    mock_firearm_ammunition_good_get,
):

    response = authorized_client.get(firearm_ammunition_product_details_url)
    assert response.status_code == 200

    expiry_date = datetime.date.today() + datetime.timedelta(days=100)
    assert response.context["summary"] == (
        ("firearm-type", "Ammunition", "Select the type of firearm product"),
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
            '<a class="govuk-link govuk-link--no-visited-state" '
            'href="/product-list/8b730c06-ab4e-401c-aeb0-32b3c92e912c/documents/b4a2da59-c0bc-4b6d-8ed9-4ca28ffbf65a/" '
            'target="_blank">rfd_certificate.txt</a>',
            "Upload a registered firearms dealer certificate",
        ),
        ("rfd-certificate-reference-number", "RFD123", "Certificate reference number"),
        ("rfd-certificate-date-of-expiry", expiry_date.strftime("%d %B %Y"), "Certificate date of expiry"),
        (
            "is-covered-by-firearm-act-section-five",
            "Yes",
            "Is the product covered by section 5 of the Firearms Act 1968?",
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
            '<a class="govuk-link govuk-link--no-visited-state" href="/product-list/8b730c06-ab4e-401c-aeb0-32b3c92e912c/documents/6c48a2cc-1ed9-49a5-8ca7-df8af5fc2335/" target="_blank">data_sheet.pdf</a>',
            "Upload a document that shows what your product is designed to do",
        ),
        ("product-document-description", "product data sheet", "Description (optional)"),
    )


def test_components_for_firearm_product_details_context(
    authorized_client,
    components_for_firearm_product_details_url,
    mock_get_organisation_with_rfd,
    mock_components_for_firearm_good_get,
):

    response = authorized_client.get(components_for_firearm_product_details_url)
    assert response.status_code == 200

    expiry_date = datetime.date.today() + datetime.timedelta(days=100)
    assert response.context["summary"] == (
        ("firearm-type", "Components for firearms", "Select the type of firearm product"),
        ("name", "p1", "Give the product a descriptive name"),
        ("part-number", "44", "Part number"),
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
            '<a class="govuk-link govuk-link--no-visited-state" '
            'href="/product-list/8b730c06-ab4e-401c-aeb0-32b3c92e912c/documents/b4a2da59-c0bc-4b6d-8ed9-4ca28ffbf65a/" '
            'target="_blank">rfd_certificate.txt</a>',
            "Upload a registered firearms dealer certificate",
        ),
        ("rfd-certificate-reference-number", "RFD123", "Certificate reference number"),
        ("rfd-certificate-date-of-expiry", expiry_date.strftime("%d %B %Y"), "Certificate date of expiry"),
        (
            "is-covered-by-firearm-act-section-five",
            "Yes",
            "Is the product covered by section 5 of the Firearms Act 1968?",
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
            '<a class="govuk-link govuk-link--no-visited-state" href="/product-list/8b730c06-ab4e-401c-aeb0-32b3c92e912c/documents/6c48a2cc-1ed9-49a5-8ca7-df8af5fc2335/" target="_blank">data_sheet.pdf</a>',
            "Upload a document that shows what your product is designed to do",
        ),
        ("product-document-description", "product data sheet", "Description (optional)"),
    )


def test_components_for_ammunition_product_details_context(
    authorized_client,
    components_for_ammunition_product_details_url,
    mock_get_organisation_with_rfd,
    mock_components_for_ammunition_good_get,
):

    response = authorized_client.get(components_for_ammunition_product_details_url)
    assert response.status_code == 200

    expiry_date = datetime.date.today() + datetime.timedelta(days=100)
    assert response.context["summary"] == (
        ("firearm-type", "Components for ammunition", "Select the type of firearm product"),
        ("name", "p1", "Give the product a descriptive name"),
        ("part-number", "44", "Part number"),
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
            '<a class="govuk-link govuk-link--no-visited-state" '
            'href="/product-list/8b730c06-ab4e-401c-aeb0-32b3c92e912c/documents/b4a2da59-c0bc-4b6d-8ed9-4ca28ffbf65a/" '
            'target="_blank">rfd_certificate.txt</a>',
            "Upload a registered firearms dealer certificate",
        ),
        ("rfd-certificate-reference-number", "RFD123", "Certificate reference number"),
        ("rfd-certificate-date-of-expiry", expiry_date.strftime("%d %B %Y"), "Certificate date of expiry"),
        (
            "is-covered-by-firearm-act-section-five",
            "Yes",
            "Is the product covered by section 5 of the Firearms Act 1968?",
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
            '<a class="govuk-link govuk-link--no-visited-state" href="/product-list/8b730c06-ab4e-401c-aeb0-32b3c92e912c/documents/6c48a2cc-1ed9-49a5-8ca7-df8af5fc2335/" target="_blank">data_sheet.pdf</a>',
            "Upload a document that shows what your product is designed to do",
        ),
        ("product-document-description", "product data sheet", "Description (optional)"),
    )


def test_firearm_accessory_product_details_context(
    authorized_client,
    firearm_accessory_product_details_url,
    mock_firearm_accessory_good_get,
):

    response = authorized_client.get(firearm_accessory_product_details_url)
    assert response.status_code == 200
    assert response.context["summary"] == (
        ("firearm-type", "Accessory of a firearm", "Select the type of firearm product"),
        ("name", "p1", "Give the product a descriptive name"),
        ("part-number", "44", "Part number"),
        ("is-good-controlled", "Yes", "Do you know the product's control list entry?"),
        ("control-list-entries", "ML1a, ML22b", "Enter the control list entry"),
        ("is-pv-graded", "Yes", "Does the product have a government security grading or classification?"),
        ("pv-grading-prefix", "NATO", "Enter a prefix (optional)"),
        ("pv-grading-grading", "Official", "What is the security grading or classification?"),
        ("pv-grading-suffix", "SUFFIX", "Enter a suffix (optional)"),
        ("pv-grading-issuing-authority", "Government entity", "Name and address of the issuing authority"),
        ("pv-grading-details-reference", "GR123", "Reference"),
        ("pv-grading-details-date-of-issue", "20 February 2020", "Date of issue"),
        (
            "has-product-document",
            "Yes",
            "Do you have a document that shows what your product is and what it’s designed to do?",
        ),
        ("is-document-sensitive", "No", "Is the document rated above Official-sensitive?"),
        (
            "product-document",
            '<a class="govuk-link govuk-link--no-visited-state" href="/product-list/8b730c06-ab4e-401c-aeb0-32b3c92e912c/documents/6c48a2cc-1ed9-49a5-8ca7-df8af5fc2335/" target="_blank">data_sheet.pdf</a>',
            "Upload a document that shows what your product is designed to do",
        ),
        ("product-document-description", "product data sheet", "Description (optional)"),
        ("product-component", "This has been modified", "Is the product a component?"),
        (
            "uses-information-security",
            "No",
            "Does the product include cryptography or other information security " "features?",
        ),
        ("military-use", "No", "Is the product specially designed or modified for military use?"),
    )


def test_software_relating_to_a_firearm_product_details_context(
    authorized_client,
    software_related_to_firearm_product_details_url,
    mock_software_related_to_firearm_good_get,
):

    response = authorized_client.get(software_related_to_firearm_product_details_url)
    assert response.status_code == 200
    assert response.context["summary"] == (
        ("firearm-type", "Software relating to a firearm", "Select the type of firearm product"),
        ("name", "p1", "Give the product a descriptive name"),
        ("part-number", "44", "Part number"),
        ("is-good-controlled", "Yes", "Do you know the product's control list entry?"),
        ("control-list-entries", "ML1a, ML22b", "Enter the control list entry"),
        ("is-pv-graded", "Yes", "Does the product have a government security grading or classification?"),
        ("pv-grading-prefix", "NATO", "Enter a prefix (optional)"),
        ("pv-grading-grading", "Official", "What is the security grading or classification?"),
        ("pv-grading-suffix", "SUFFIX", "Enter a suffix (optional)"),
        ("pv-grading-issuing-authority", "Government entity", "Name and address of the issuing authority"),
        ("pv-grading-details-reference", "GR123", "Reference"),
        ("pv-grading-details-date-of-issue", "20 February 2020", "Date of issue"),
        (
            "has-product-document",
            "Yes",
            "Do you have a document that shows what your product is and what it’s designed to do?",
        ),
        ("is-document-sensitive", "No", "Is the document rated above Official-sensitive?"),
        (
            "product-document",
            '<a class="govuk-link govuk-link--no-visited-state" href="/product-list/8b730c06-ab4e-401c-aeb0-32b3c92e912c/documents/6c48a2cc-1ed9-49a5-8ca7-df8af5fc2335/" target="_blank">data_sheet.pdf</a>',
            "Upload a document that shows what your product is designed to do",
        ),
        ("product-document-description", "product data sheet", "Description (optional)"),
        (
            "uses-information-security",
            "No",
            "Does the product include cryptography or other information security " "features?",
        ),
        ("military-use", "No", "Is the product specially designed or modified for military use?"),
    )


def test_technology_relating_to_a_firearm_product_details_context(
    authorized_client,
    technology_related_to_firearm_product_details_url,
    mock_technology_related_to_firearm_good_get,
):

    response = authorized_client.get(technology_related_to_firearm_product_details_url)
    assert response.status_code == 200
    assert response.context["summary"] == (
        ("firearm-type", "Technology relating to a firearm", "Select the type of firearm product"),
        ("name", "p1", "Give the product a descriptive name"),
        ("part-number", "44", "Part number"),
        ("is-good-controlled", "Yes", "Do you know the product's control list entry?"),
        ("control-list-entries", "ML1a, ML22b", "Enter the control list entry"),
        ("is-pv-graded", "Yes", "Does the product have a government security grading or classification?"),
        ("pv-grading-prefix", "NATO", "Enter a prefix (optional)"),
        ("pv-grading-grading", "Official", "What is the security grading or classification?"),
        ("pv-grading-suffix", "SUFFIX", "Enter a suffix (optional)"),
        ("pv-grading-issuing-authority", "Government entity", "Name and address of the issuing authority"),
        ("pv-grading-details-reference", "GR123", "Reference"),
        ("pv-grading-details-date-of-issue", "20 February 2020", "Date of issue"),
        (
            "has-product-document",
            "Yes",
            "Do you have a document that shows what your product is and what it’s designed to do?",
        ),
        ("is-document-sensitive", "No", "Is the document rated above Official-sensitive?"),
        (
            "product-document",
            '<a class="govuk-link govuk-link--no-visited-state" href="/product-list/8b730c06-ab4e-401c-aeb0-32b3c92e912c/documents/6c48a2cc-1ed9-49a5-8ca7-df8af5fc2335/" target="_blank">data_sheet.pdf</a>',
            "Upload a document that shows what your product is designed to do",
        ),
        ("product-document-description", "product data sheet", "Description (optional)"),
        (
            "uses-information-security",
            "No",
            "Does the product include cryptography or other information security " "features?",
        ),
        ("military-use", "No", "Is the product specially designed or modified for military use?"),
    )
