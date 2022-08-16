from django.urls import reverse

from core.summaries.formatters import (
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
    "security-features": "has_security_features",
    "security-features-details": "has_security_features",
    "declared-at-customs": "has_declared_at_customs",
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


def software_summary(good):
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


def software_product_on_application_summary(good_on_application):
    return core_software_product_on_application_summary(good_on_application)
