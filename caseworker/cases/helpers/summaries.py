from django.urls import reverse

from core.summaries.formatters import (
    add_labels,
    document_formatter,
    format_values,
    FIREARM_LABELS,
    FIREARM_ON_APPLICATION_FORMATTERS,
    FIREARM_ON_APPLICATION_LABELS,
    FIREARM_VALUE_FORMATTERS,
    template_formatter,
)
from core.summaries.reducers import (
    firearm_on_application_reducer,
    firearm_reducer,
)
from core.summaries.utils import pick_fields


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


def firearm_product_summary(good_on_application, is_user_rfd, organisation_documents, queue_pk):
    summary = firearm_reducer(good_on_application["good"], is_user_rfd, organisation_documents)

    def goods_document_formatter(document):
        url = reverse(
            "cases:document",
            kwargs={
                "queue_pk": queue_pk,
                "pk": good_on_application["application"],
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
    "firearm-certificate-missing",
    "firearm-certificate-missing-reason",
    "firearm-certificate-number",
    "firearm-certificate-expiry-date",
    "shotgun-certificate",
    "shotgun-certificate-missing",
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


def firearm_product_on_application_summary(good_on_application, good_on_application_documents, queue_pk):
    summary = firearm_on_application_reducer(good_on_application, good_on_application_documents)

    def good_on_application_document_formatter(document):
        url = reverse(
            "cases:document",
            kwargs={
                "queue_pk": queue_pk,
                "pk": good_on_application["application"],
                "file_pk": document["id"],
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
    summary = add_labels(summary, FIREARM_ON_APPLICATION_LABELS)

    return summary
