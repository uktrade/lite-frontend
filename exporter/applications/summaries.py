from django.urls import reverse

from core.summaries.formatters import (
    add_labels,
    document_formatter,
    format_values,
    FIREARM_LABELS,
    FIREARM_VALUE_FORMATTERS,
)
from core.summaries.reducers import firearm_reducer
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


def add_edit_links(application, good, summary):
    edit_links = {
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

    get_edit_link = get_edit_link_factory(application, good)

    summary_with_edit_links = ()
    for key, value, *rest in summary:
        try:
            edit_link = get_edit_link(edit_links[key])
        except KeyError:
            edit_link = None

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
    "has-product-document",
    "is-document-sensitive",
    "product-document",
    "product-document-description",
)


def firearm_product_summary(application, good, is_user_rfd, organisation_documents):
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
    summary = add_edit_links(application, good, summary)

    return summary
