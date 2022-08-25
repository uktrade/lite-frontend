from django.urls import reverse

from core.summaries.formatters import (
    document_formatter,
)
from core.summaries.summaries import (
    platform_summary as core_platform_summary,
    platform_product_on_application_summary as core_platform_product_on_application_summary,
)


PLATFORM_SUMMARY_EDIT_LINKS = {
    "name": "name",
    "is-good-controlled": "control_list_entries",
    "control-list-entries": "control_list_entries",
    "part-number": "part_number",
    "has-part-number": "part_number",
    "no-part-number-comments": "part_number",
    "is-pv-graded": "pv_grading",
    "pv-grading-prefix": "pv_grading_details",
    "pv-grading-grading": "pv_grading_details",
    "pv-grading-suffix": "pv_grading_details",
    "pv-grading-issuing-authority": "pv_grading_details",
    "pv-grading-details-reference": "pv_grading_details",
    "pv-grading-details-date-of-issue": "pv_grading_details",
    "uses-information-security": "uses_information_security",
    "uses-information-security-details": "uses_information_security",
    "has-product-document": "product_document_availability",
    "no-product-document-explanation": "product_document_availability",
    "is-document-sensitive": "product_document_sensitivity",
    "product-document": "product_document",
    "product-document-description": "product_document",
    "military-use": "military_use",
    "military-use-details": "military_use",
}


def get_platform_summary_edit_link_factory(application, good):
    def get_edit_link(name):
        return reverse(
            f"applications:platform_edit_{name}",
            kwargs={
                "pk": application["id"],
                "good_pk": good["id"],
            },
        )

    return get_edit_link


def add_platform_summary_edit_links(summary, edit_links, application, good):
    get_edit_link = get_platform_summary_edit_link_factory(application, good)

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


def platform_summary(good):
    def goods_document_formatter(document):
        url = reverse(
            "goods:document",
            kwargs={
                "pk": good["id"],
                "file_pk": document["id"],
            },
        )

        return document_formatter(document, url)

    return core_platform_summary(
        good,
        {
            "product-document": goods_document_formatter,
        },
    )


def platform_product_on_application_summary(good_on_application):
    return core_platform_product_on_application_summary(good_on_application)


PLATFORM_ON_APPLICATION_SUMMARY_EDIT_LINKS = {
    "is-onward-exported": "onward_exported",
    "is-altered": "onward_altered",
    "is-altered-comments": "onward_altered",
    "number-of-items": "quantity_value",
    "total-value": "quantity_value",
}


def get_platform_on_application_summary_edit_link_factory(application, good_on_application, summary_type):
    def get_edit_link(name):
        return reverse(
            f"applications:platform_on_application_summary_edit_{name}",
            kwargs={
                "pk": application["id"],
                "good_on_application_pk": good_on_application["id"],
                "summary_type": summary_type,
            },
        )

    return get_edit_link


def add_platform_on_application_summary_edit_links(
    summary,
    edit_links,
    application,
    good_on_application,
    summary_type,
):
    get_edit_link = get_platform_on_application_summary_edit_link_factory(
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
