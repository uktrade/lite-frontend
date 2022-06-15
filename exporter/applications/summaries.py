from django.urls import reverse

from core.summaries.formatters import (
    add_labels,
    document_formatter,
    format_values,
    FIREARM_LABELS,
    FIREARM_ON_APPLICATION_FORMATTERS,
    FIREARM_VALUE_FORMATTERS,
    template_formatter,
)
from core.summaries.reducers import (
    firearm_on_application_reducer,
    firearm_reducer,
)
from core.summaries.utils import pick_fields


def get_edit_link_factory(application, good):
    def get_edit_link(name):
        return reverse(
            f"applications:firearm_edit_{name}",
            kwargs={
                "pk": application["id"],
                "good_pk": good["id"],
            },
        )

    return get_edit_link


PRODUCT_SUMMARY_EDIT_LINKS = {
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


def add_edit_links(summary, edit_links, application, good):
    get_edit_link = get_edit_link_factory(application, good)

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


FIREARM_FIELDS = (
    "firearm-type",
    "firearm-category",
    "name",
    "is-good-controlled",
    "control-list-entries",
    "is-pv-graded",
    "pv-grading-prefix",
    "pv-grading-grading",
    "pv-grading-suffix",
    "pv-grading-issuing-authority",
    "pv-grading-details-reference",
    "pv-grading-details-date-of-issue",
    "calibre",
    "is-replica",
    "is-replica-description",
    "is-registered-firearms-dealer",
    "is-covered-by-firearm-act-section-five",
    "firearms-act-1968-section",
    "is-covered-by-firearm-act-section-one-two-or-five-explanation",
    "section-5-certificate-document",
    "section-5-certificate-reference-number",
    "section-5-certificate-date-of-expiry",
    "section-5-certificate-missing",
    "section-5-certificate-missing-reason",
    "has-product-document",
    "no-product-document-explanation",
    "is-document-sensitive",
    "product-document",
    "product-document-description",
)


def firearm_product_summary(good, is_user_rfd, organisation_documents):
    summary = firearm_reducer(good, is_user_rfd, organisation_documents)

    def goods_document_formatter(document):
        url = reverse(
            "goods:document",
            kwargs={
                "pk": good["id"],
                "file_pk": document["id"],
            },
        )

        return document_formatter(document, url)

    formatters = {
        **FIREARM_VALUE_FORMATTERS,
        **{
            "product-document": goods_document_formatter,
        },
    }
    summary = pick_fields(summary, FIREARM_FIELDS)
    summary = format_values(summary, formatters)
    summary = add_labels(summary, FIREARM_LABELS)

    return summary


FIREARM_ON_APPLICATION_FIELDS = (
    "firearm-certificate",
    "firearm-certificate-missing-reason",
    "firearm-certificate-number",
    "firearm-certificate-expiry-date",
    "shotgun-certificate",
    "shotgun-certificate-missing-reason",
    "shotgun-certificate-number",
    "shotgun-certificate-expiry-date",
    "made-before-1938",
    "manufacture-year",
    "is-onward-exported",
    "is-altered",
    "is-altered-comments",
    "is-incorporated",
    "is-incorporated-comments",
    "is-deactivated",
    "deactivated-date",
    "is-proof-standards",
    "is-proof-standards-comments",
    "number-of-items",
    "total-value",
    "has-serial-numbers",
    "no-identification-markings-details",
    "serial-numbers",
)


def firearm_product_on_application_summary(good_on_application, good_on_application_documents):
    summary = firearm_on_application_reducer(good_on_application, good_on_application_documents)

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

    def serial_numbers_formatter(serial_numbers):
        return template_formatter(
            "goods/includes/serial_numbers.html",
            lambda _: good_on_application,
        )(serial_numbers)

    formatters = {
        **FIREARM_ON_APPLICATION_FORMATTERS,
        **{
            "firearm-certificate": good_on_application_document_formatter,
            "shotgun-certificate": good_on_application_document_formatter,
            "serial-numbers": serial_numbers_formatter,
        },
    }

    summary = pick_fields(summary, FIREARM_ON_APPLICATION_FIELDS)
    summary = format_values(summary, formatters)

    return summary
