from core.summaries.formatters import (
    add_labels,
    format_values,
    FIREARM_LABELS,
    FIREARM_ON_APPLICATION_FORMATTERS,
    FIREARM_ON_APPLICATION_LABELS,
    FIREARM_VALUE_FORMATTERS,
    template_formatter,
    PLATFORM_VALUE_FORMATTERS,
    PLATFORM_LABELS,
)
from core.summaries.reducers import (
    firearm_on_application_reducer,
    firearm_reducer,
    platform_reducer,
)
from core.summaries.utils import pick_fields


FIREARM_FIELDS = (
    "firearm-type",
    "firearm-category",
    "name",
    "is-good-controlled",
    "control-list-entries",
    "assessed-control-list-entries",
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
    "rfd-certificate-document",
    "rfd-certificate-reference-number",
    "rfd-certificate-date-of-expiry",
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

PLATFORM_FIELDS = (
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
    "has-product-document",
    "no-product-document-explanation",
    "is-document-sensitive",
    "product-document",
    "product-document-description",
)


def firearm_product_summary(good, is_user_rfd, organisation_documents, additional_formatters=None):
    if not additional_formatters:
        additional_formatters = {}

    summary = firearm_reducer(good, is_user_rfd, organisation_documents)
    formatters = {
        **FIREARM_VALUE_FORMATTERS,
        **additional_formatters,
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


def firearm_product_on_application_summary(
    good_on_application, good_on_application_documents, additional_formatters=None
):
    if not additional_formatters:
        additional_formatters = {}

    summary = firearm_on_application_reducer(good_on_application, good_on_application_documents)

    def serial_numbers_formatter(serial_numbers):
        return template_formatter(
            "goods/includes/serial_numbers.html",
            lambda _: good_on_application,
        )(serial_numbers)

    formatters = {
        **FIREARM_ON_APPLICATION_FORMATTERS,
        **{
            "serial-numbers": serial_numbers_formatter,
        },
        **additional_formatters,
    }

    summary = pick_fields(summary, FIREARM_ON_APPLICATION_FIELDS)
    summary = format_values(summary, formatters)
    summary = add_labels(summary, FIREARM_ON_APPLICATION_LABELS)

    return summary


def platform_summary(good, additional_formatters=None):
    if not additional_formatters:
        additional_formatters = {}

    summary = platform_reducer(good)
    formatters = {
        **PLATFORM_VALUE_FORMATTERS,
        **additional_formatters,
    }
    summary = pick_fields(summary, PLATFORM_FIELDS)
    summary = format_values(summary, formatters)
    summary = add_labels(summary, PLATFORM_LABELS)

    return summary
