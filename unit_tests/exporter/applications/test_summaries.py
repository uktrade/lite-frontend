import uuid

from core.constants import OrganisationDocumentType

from exporter.applications.summaries.firearm import (
    add_firearm_on_application_summary_edit_links,
    add_firearm_summary_edit_links,
    firearm_summary,
    get_firearm_summary_edit_link_factory,
    get_firearm_on_application_summary_edit_link_factory,
)


def test_get_firearm_summary_edit_link_factory(mocker):
    mock_reverse = mocker.patch("exporter.applications.summaries.firearm.reverse")
    mock_reverse.return_value = "/reversed-url/"

    application = {
        "id": uuid.uuid4(),
    }
    good = {
        "id": uuid.uuid4(),
    }

    get_edit_link = get_firearm_summary_edit_link_factory(application, good)

    assert get_edit_link("test") == "/reversed-url/"
    mock_reverse.assert_called_with(
        "applications:firearm_edit_test",
        kwargs={
            "pk": application["id"],
            "good_pk": good["id"],
        },
    )


def test_add_firearm_summary_edit_links(mocker):
    mock_reverse = mocker.patch("exporter.applications.summaries.firearm.reverse")
    mock_reverse.side_effect = lambda name, kwargs: f"/{kwargs['pk']}/{kwargs['good_pk']}/{name}/"

    application = {
        "id": uuid.uuid4(),
    }
    good = {
        "id": uuid.uuid4(),
    }

    summary = (
        ("no-edit-link", "value"),
        ("has-edit-link", "another-value"),
        ("has-another-edit-link", "a-different-value"),
    )

    edit_links = {
        "has-edit-link": "edit-link-name",
        "has-another-edit-link": "another-edit-link-name",
    }

    summary_with_edit_links = add_firearm_summary_edit_links(summary, edit_links, application, good)
    assert summary_with_edit_links == (
        ("no-edit-link", "value", None),
        (
            "has-edit-link",
            "another-value",
            f"/{application['id']}/{good['id']}/applications:firearm_edit_edit-link-name/",
        ),
        (
            "has-another-edit-link",
            "a-different-value",
            f"/{application['id']}/{good['id']}/applications:firearm_edit_another-edit-link-name/",
        ),
    )


def test_firearm_summary():
    product_document = {
        "description": "Document description",
        "id": uuid.uuid4(),
        "safe": True,
        "name": "product-document.pdf",
    }
    good = {
        "id": uuid.uuid4(),
        "firearm_details": {
            "type": {
                "key": "type",
                "value": "Type",
            },
            "category": [
                {
                    "key": "category",
                    "value": "Category",
                },
            ],
            "calibre": "calibre",
            "is_replica": False,
            "is_covered_by_firearm_act_section_one_two_or_five": False,
            "firearms_act_section": "firearms_act_section5",
            "section_certificate_missing": False,
            "section_certificate_number": "section-certificate-number",
            "section_certificate_date_of_expiry": "2020-10-09",
        },
        "name": "name",
        "is_good_controlled": {
            "key": "True",
            "value": "Yes is controlled",
        },
        "control_list_entries": [
            {"rating": "ML1"},
            {"rating": "ML1a"},
        ],
        "is_pv_graded": {
            "key": "no",
            "value": "No",
        },
        "is_document_available": True,
        "is_document_sensitive": False,
        "no_documents_comments": "No document comments",
        "documents": [product_document],
    }
    is_user_rfd = True
    section_5_document = {
        "id": uuid.uuid4(),
        "document": {
            "id": uuid.uuid4(),
            "safe": True,
            "name": "section5.pdf",
        },
    }
    rfd_document = {
        "id": uuid.uuid4(),
        "document": {
            "id": uuid.uuid4(),
            "safe": True,
            "name": "section5.pdf",
        },
        "reference_code": "12345",
        "expiry_date": "31 May 2025",
    }
    organisation_documents = {
        "section-five-certificate": section_5_document,
        OrganisationDocumentType.RFD_CERTIFICATE: rfd_document,
    }

    assert firearm_summary(good, is_user_rfd, organisation_documents) == (
        (
            "firearm-type",
            "Type",
            "Select the type of firearm product",
        ),
        (
            "firearm-category",
            "Category",
            "Firearm category",
        ),
        (
            "name",
            "name",
            "Give the product a descriptive name",
        ),
        (
            "is-good-controlled",
            "Yes is controlled",
            "Do you know the product's control list entry?",
        ),
        (
            "control-list-entries",
            "ML1, ML1a",
            "Enter the control list entry",
        ),
        (
            "is-pv-graded",
            "No",
            "Does the product have a government security grading or classification?",
        ),
        (
            "calibre",
            "calibre",
            "What is the calibre of the product?",
        ),
        (
            "is-replica",
            "No",
            "Is the product a replica firearm?",
        ),
        (
            "is-registered-firearms-dealer",
            "Yes",
            "Are you a registered firearms dealer?",
        ),
        (
            "rfd-certificate-document",
            '<a class="govuk-link govuk-link--no-visited-state" '
            f'href="/goods/{good["id"]}/documents/{rfd_document["id"]}/" '
            'target="_blank">section5.pdf</a>',
            "Upload a registered firearms dealer certificate",
        ),
        ("rfd-certificate-reference-number", "12345", "Certificate reference number"),
        (
            "rfd-certificate-date-of-expiry",
            "31 May 2025",
            "Certificate date of expiry",
        ),
        (
            "is-covered-by-firearm-act-section-five",
            False,
            "Is the product covered by section 5 of the Firearms Act 1968?",
        ),
        (
            "section-5-certificate-document",
            f'<a class="govuk-link govuk-link--no-visited-state" href="/organisation/document/{section_5_document["id"]}/" target="_blank">section5.pdf</a>',
            "Upload your section 5 letter of authority",
        ),
        (
            "section-5-certificate-reference-number",
            "section-certificate-number",
            "Certificate reference number",
        ),
        (
            "section-5-certificate-date-of-expiry",
            "9 October 2020",
            "Certificate date of expiry",
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
            f'<a class="govuk-link govuk-link--no-visited-state" href="/goods/{good["id"]}/documents/{product_document["id"]}/" target="_blank">product-document.pdf</a>',
            "Upload a document that shows what your product is designed to do",
        ),
        (
            "product-document-description",
            "Document description",
            "Description (optional)",
        ),
    )


def test_get_firearm_on_application_summary_edit_link_factory(mocker):
    mock_reverse = mocker.patch("exporter.applications.summaries.firearm.reverse")
    mock_reverse.return_value = "/reversed-url/"

    application = {
        "id": uuid.uuid4(),
    }
    good_on_application = {
        "id": uuid.uuid4(),
    }
    summary_type = "summary-type"

    get_edit_link = get_firearm_on_application_summary_edit_link_factory(
        application,
        good_on_application,
        summary_type,
    )

    assert get_edit_link("test") == "/reversed-url/"
    mock_reverse.assert_called_with(
        "applications:product_on_application_summary_edit_test",
        kwargs={
            "pk": application["id"],
            "good_on_application_pk": good_on_application["id"],
            "summary_type": summary_type,
        },
    )


def test_add_firearm_on_application_summary_edit_links(mocker):
    mock_reverse = mocker.patch("exporter.applications.summaries.firearm.reverse")
    mock_reverse.side_effect = (
        lambda name, kwargs: f"/{kwargs['pk']}/{kwargs['good_on_application_pk']}/{kwargs['summary_type']}/{name}/"
    )

    application = {
        "id": uuid.uuid4(),
    }
    good_on_application = {
        "id": uuid.uuid4(),
    }
    summary_type = "product-on-application-summary"

    summary = (
        ("no-edit-link", "value"),
        ("has-edit-link", "another-value"),
        ("has-another-edit-link", "a-different-value"),
    )

    edit_links = {
        "has-edit-link": "edit-link-name",
        "has-another-edit-link": "another-edit-link-name",
    }

    summary_with_edit_links = add_firearm_on_application_summary_edit_links(
        summary,
        edit_links,
        application,
        good_on_application,
        summary_type,
    )
    assert summary_with_edit_links == (
        ("no-edit-link", "value", None),
        (
            "has-edit-link",
            "another-value",
            f"/{application['id']}/{good_on_application['id']}/{summary_type}/applications:product_on_application_summary_edit_edit-link-name/",
        ),
        (
            "has-another-edit-link",
            "a-different-value",
            f"/{application['id']}/{good_on_application['id']}/{summary_type}/applications:product_on_application_summary_edit_another-edit-link-name/",
        ),
    )
