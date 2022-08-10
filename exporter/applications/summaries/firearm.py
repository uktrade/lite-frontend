from django.urls import reverse

from core.summaries.formatters import (
    document_formatter,
)
from core.summaries.summaries import (
    firearm_summary as core_firearm_summary,
    firearm_on_application_summary as core_firearm_on_application_summary,
)


FIREARM_SUMMARY_EDIT_LINKS = {
    "firearm-category": "category",
    "name": "name",
    "calibre": "calibre",
    "is-good-controlled": "control_list_entries",
    "control-list-entries": "control_list_entries",
    "is-pv-graded": "pv_grading",
    "pv-grading-prefix": "pv_grading",
    "pv-grading-grading": "pv_grading",
    "pv-grading-suffix": "pv_grading",
    "pv-grading-issuing-authority": "pv_grading",
    "pv-grading-details-reference": "pv_grading",
    "pv-grading-details-date-of-issue": "pv_grading",
    "is-replica": "replica",
    "is-replica-description": "replica",
    "has-product-document": "product_document_availability",
    "no-product-document-explanation": "product_document_availability",
    "is-document-sensitive": "product_document_sensitivity",
    "product-document": "product_document",
    "product-document-description": "product_document",
    "section-5-certificate-missing": "letter_of_authority",
    "section-5-certificate-missing-reason": "letter_of_authority",
    "is-registered-firearms-dealer": "registered_firearms_dealer",
    "firearms-act-1968-section": "firearms_act_1968",
    "is-covered-by-firearm-act-section-one-two-or-five-explanation": "firearms_act_1968",
    "is-covered-by-firearm-act-section-five": "section_5_firearms_act_1968",
    "section-5-certificate-document": "letter_of_authority",
    "section-5-certificate-reference-number": "letter_of_authority",
    "section-5-certificate-date-of-expiry": "letter_of_authority",
}


def get_firearm_summary_edit_link_factory(application, good):
    def get_edit_link(name):
        return reverse(
            f"applications:firearm_edit_{name}",
            kwargs={
                "pk": application["id"],
                "good_pk": good["id"],
            },
        )

    return get_edit_link


def add_firearm_summary_edit_links(summary, edit_links, application, good):
    get_edit_link = get_firearm_summary_edit_link_factory(application, good)

    summary_with_edit_links = ()
    for key, value, *rest in summary:
        try:
            edit_link_key = edit_links[key]
        except KeyError:
            edit_link = None
        else:
            edit_link = get_edit_link(edit_link_key)

        summary_with_edit_links += ((key, value, *rest, edit_link),)

    return summary_with_edit_links


def firearm_summary(good, is_user_rfd, organisation_documents):
    def goods_document_formatter(document):
        url = reverse(
            "goods:document",
            kwargs={
                "pk": good["id"],
                "file_pk": document["id"],
            },
        )

        return document_formatter(document, url)

    def rfd_document_formatter(document):
        url = reverse(
            "goods:document",
            kwargs={
                "pk": good["id"],
                "file_pk": document["id"],
            },
        )

        return document_formatter(document["document"], url)

    return core_firearm_summary(
        good,
        is_user_rfd,
        organisation_documents,
        {
            "product-document": goods_document_formatter,
            "rfd-certificate-document": rfd_document_formatter,
        },
    )


def firearm_on_application_summary(good_on_application, good_on_application_documents):
    def good_on_application_document_formatter(document):
        url = reverse(
            "applications:good-on-application-document",
            kwargs={
                "pk": good_on_application["application"],
                "good_pk": good_on_application["good"]["id"],
                "doc_pk": document["id"],
            },
        )

        return document_formatter(document, url)

    return core_firearm_on_application_summary(
        good_on_application,
        good_on_application_documents,
        {
            "firearm-certificate": good_on_application_document_formatter,
            "shotgun-certificate": good_on_application_document_formatter,
        },
    )


FIREARM_ON_APPLICATION_SUMMARY_EDIT_LINKS = {
    "firearm-certificate": "firearm_certificate",
    "firearm-certificate-number": "firearm_certificate",
    "firearm-certificate-expiry-date": "firearm_certificate",
    "shotgun-certificate": "shotgun_certificate",
    "shotgun-certificate-number": "shotgun_certificate",
    "shotgun-certificate-expiry-date": "shotgun_certificate",
    "made-before-1938": "made_before_1938",
    "manufacture-year": "year_of_manufacture",
    "is-onward-exported": "onward_exported",
    "is-altered": "onward_altered",
    "is-altered-comments": "onward_altered",
    "is-incorporated": "onward_incorporated",
    "is-incorporated-comments": "onward_incorporated",
    "is-deactivated": "is_deactivated",
    "deactivated-date": "is_deactivated",
    "is-proof-standards": "is_deactivated_to_standard",
    "is-proof-standards-comments": "is_deactivated_to_standard",
    "number-of-items": "quantity_value",
    "total-value": "quantity_value",
    "has-serial-numbers": "serial_identification_markings",
    "no-identification-markings-details": "serial_identification_markings",
    "serial-numbers": "serial_numbers",
}


def get_firearm_on_application_summary_edit_link_factory(application, good_on_application, summary_type):
    def get_edit_link(name):
        return reverse(
            f"applications:product_on_application_summary_edit_{name}",
            kwargs={
                "pk": application["id"],
                "good_on_application_pk": good_on_application["id"],
                "summary_type": summary_type,
            },
        )

    return get_edit_link


def add_firearm_on_application_summary_edit_links(
    summary,
    edit_links,
    application,
    good_on_application,
    summary_type,
):
    get_edit_link = get_firearm_on_application_summary_edit_link_factory(
        application,
        good_on_application,
        summary_type,
    )

    summary_with_edit_links = ()
    for key, value, *rest in summary:
        try:
            edit_link_key = edit_links[key]
        except KeyError:
            edit_link = None
        else:
            edit_link = get_edit_link(edit_link_key)

        summary_with_edit_links += ((key, value, *rest, edit_link),)

    return summary_with_edit_links
