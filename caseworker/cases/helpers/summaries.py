from django.urls import reverse

from core.summaries.formatters import (
    document_formatter,
)
from core.summaries.summaries import firearm_product_summary as core_firearm_product_summary
from core.summaries.summaries import (
    firearm_product_on_application_summary as core_firearm_product_on_application_summary,
)


def _get_document_url(queue_pk, good_on_application, document):
    return reverse(
        "cases:document",
        kwargs={
            "queue_pk": queue_pk,
            "pk": good_on_application["application"],
            "file_pk": document["id"],
        },
    )


def firearm_product_summary(good_on_application, is_user_rfd, organisation_documents, queue_pk):
    def organisation_document_formatter(document):
        url = _get_document_url(queue_pk, good_on_application, document)
        return document_formatter(document["document"], url)

    def product_document_formatter(document):
        url = _get_document_url(queue_pk, good_on_application, document)
        return document_formatter(document, url)

    return core_firearm_product_summary(
        good_on_application["good"],
        is_user_rfd,
        organisation_documents,
        {
            "product-document": product_document_formatter,
            "section-5-certificate-document": organisation_document_formatter,
            "rfd-certificate-document": organisation_document_formatter,
        },
    )


def firearm_product_on_application_summary(good_on_application, good_on_application_documents, queue_pk):
    def good_on_application_document_formatter(document):
        url = _get_document_url(queue_pk, good_on_application, document)
        return document_formatter(document, url)

    return core_firearm_product_on_application_summary(
        good_on_application,
        good_on_application_documents,
        {
            "firearm-certificate": good_on_application_document_formatter,
            "shotgun-certificate": good_on_application_document_formatter,
        },
    )
