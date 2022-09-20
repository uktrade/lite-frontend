from django.urls import reverse

from core.summaries.formatters import (
    add_edit_links,
    document_formatter,
)
from core.summaries.summaries import (
    software_summary as core_software_summary,
    software_product_on_application_summary as core_software_product_on_application_summary,
)


SOFTWARE_SUMMARY_EDIT_LINKS = {
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
    "security-features": "security_features",
    "security-feature-details": "security_features",
    "declared-at-customs": "declared_at_customs",
    "has-product-document": "product_document_availability",
    "no-product-document-explanation": "product_document_availability",
    "is-document-sensitive": "product_document_sensitivity",
    "product-document": "product_document",
    "product-document-description": "product_document",
    "product-description": "product_description",
    "military-use": "military_use",
    "military-use-details": "military_use",
}


def get_software_summary_edit_link_factory(application, good):
    def get_edit_link(name):
        return reverse(
            f"applications:software_edit_{name}",
            kwargs={
                "pk": application["id"],
                "good_pk": good["id"],
            },
        )

    return get_edit_link


def add_software_summary_edit_links(summary, edit_links, application, good):
    get_edit_link = get_software_summary_edit_link_factory(application, good)

    return add_edit_links(summary, edit_links, get_edit_link)


def software_summary(good, *args, **kwargs):
    def goods_document_formatter(document):
        url = reverse(
            "goods:document",
            kwargs={
                "pk": good["id"],
                "file_pk": document["id"],
            },
        )

        return document_formatter(document, url)

    return core_software_summary(
        good,
        {
            "product-document": goods_document_formatter,
        },
    )


def software_product_on_application_summary(good_on_application, *args, **kwargs):
    return core_software_product_on_application_summary(good_on_application)


SOFTWARE_ON_APPLICATION_SUMMARY_EDIT_LINKS = {
    "is-onward-exported": "onward_exported",
    "is-altered": "onward_altered",
    "is-altered-comments": "onward_altered",
    "is-incorporated": "onward_incorporated",
    "is-incorporated-comments": "onward_incorporated",
    "number-of-items": "quantity_value",
    "total-value": "quantity_value",
}


def get_software_on_application_summary_edit_link_factory(application, good_on_application, summary_type):
    def get_edit_link(name):
        return reverse(
            f"applications:software_on_application_summary_edit_{name}",
            kwargs={
                "pk": application["id"],
                "good_on_application_pk": good_on_application["id"],
                "summary_type": summary_type,
            },
        )

    return get_edit_link


def add_software_on_application_summary_edit_links(
    summary,
    edit_links,
    application,
    good_on_application,
    summary_type,
):
    get_edit_link = get_software_on_application_summary_edit_link_factory(
        application,
        good_on_application,
        summary_type,
    )

    return add_edit_links(summary, edit_links, get_edit_link)
