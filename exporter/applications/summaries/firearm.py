from django.urls import reverse

from core.summaries.formatters import (
    add_edit_links,
    document_formatter,
)
from core.summaries.summaries import (
    firearm_summary as core_firearm_summary,
    firearm_on_application_summary as core_firearm_on_application_summary,
    firearms_accessory_summary as core_firearms_accessory_summary,
    firearm_ammunition_summary as core_firearm_ammunition_summary,
    components_for_firearms_ammunition_summary as core_components_for_firearms_ammunition_summary,
    components_for_firearms_summary as core_components_for_firearms_summary,
    software_related_to_firearms_summary as core_software_related_to_firearms_summary,
)


FIREARM_SUMMARY_EDIT_LINKS = {
    "firearm-category": "category",
    "name": "name",
    "calibre": "calibre",
    "is-good-controlled": "control_list_entries",
    "control-list-entries": "control_list_entries",
    "is-pv-graded": "pv_grading",
    "pv-grading-prefix": "pv_grading_details",
    "pv-grading-grading": "pv_grading_details",
    "pv-grading-suffix": "pv_grading_details",
    "pv-grading-issuing-authority": "pv_grading_details",
    "pv-grading-details-reference": "pv_grading_details",
    "pv-grading-details-date-of-issue": "pv_grading_details",
    "is-replica": "replica",
    "is-replica-description": "replica",
    "has-product-document": "product_document_availability",
    "no-product-document-explanation": "product_document_availability",
    "product-description": "product_description",
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

    return add_edit_links(summary, edit_links, get_edit_link)


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


def components_for_firearms_summary(good, is_user_rfd, organisation_documents):
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

    return core_components_for_firearms_summary(
        good,
        is_user_rfd,
        organisation_documents,
        {
            "product-document": goods_document_formatter,
            "rfd-certificate-document": rfd_document_formatter,
        },
    )


def firearm_ammunition_summary(good, is_user_rfd, organisation_documents):
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

    return core_firearm_ammunition_summary(
        good,
        is_user_rfd,
        organisation_documents,
        {
            "product-document": goods_document_formatter,
            "rfd-certificate-document": rfd_document_formatter,
        },
    )


def components_for_firearms_ammunition_summary(good, is_user_rfd, organisation_documents):
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

    return core_components_for_firearms_ammunition_summary(
        good,
        is_user_rfd,
        organisation_documents,
        {
            "product-document": goods_document_formatter,
            "rfd-certificate-document": rfd_document_formatter,
        },
    )


def firearms_accessory_summary(good, is_user_rfd, organisation_documents):
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

    return core_firearms_accessory_summary(
        good,
        is_user_rfd,
        organisation_documents,
        {
            "product-document": goods_document_formatter,
            "rfd-certificate-document": rfd_document_formatter,
        },
    )


def software_related_to_firearms_summary(good):
    def goods_document_formatter(document):
        url = reverse(
            "goods:document",
            kwargs={
                "pk": good["id"],
                "file_pk": document["id"],
            },
        )

        return document_formatter(document, url)

    return core_software_related_to_firearms_summary(
        good,
        {
            "product-document": goods_document_formatter,
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

    return add_edit_links(summary, edit_links, get_edit_link)
