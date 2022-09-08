from django.urls import reverse

from core.summaries.formatters import (
    document_formatter,
)
from core.summaries.summaries import (
    firearm_summary as core_firearm_summary,
    firearm_on_application_summary as core_firearm_on_application_summary,
    material_summary as core_material_summary,
    material_product_on_application_summary as core_material_product_on_application_summary,
    platform_summary as core_platform_summary,
    platform_product_on_application_summary as core_platform_product_on_application_summary,
    software_summary as core_software_summary,
    software_product_on_application_summary as core_software_product_on_application_summary,
)


def _get_document_url(queue_pk, application_pk, document):
    return reverse(
        "cases:document",
        kwargs={
            "queue_pk": queue_pk,
            "pk": application_pk,
            "file_pk": document["id"],
        },
    )


def firearm_summary(good, application_pk, is_user_rfd, organisation_documents, queue_pk):
    def organisation_document_formatter(document):
        url = _get_document_url(queue_pk, application_pk, document)
        return document_formatter(document["document"], url)

    def product_document_formatter(document):
        url = _get_document_url(queue_pk, application_pk, document)
        return document_formatter(document, url)

    return core_firearm_summary(
        good,
        is_user_rfd,
        organisation_documents,
        {
            "product-document": product_document_formatter,
            "section-5-certificate-document": organisation_document_formatter,
            "rfd-certificate-document": organisation_document_formatter,
        },
    )


def firearm_on_application_summary(good_on_application, good_on_application_documents, queue_pk):
    def good_on_application_document_formatter(document):
        url = _get_document_url(queue_pk, good_on_application, document)
        return document_formatter(document, url)

    return core_firearm_on_application_summary(
        good_on_application,
        good_on_application_documents,
        {
            "firearm-certificate": good_on_application_document_formatter,
            "shotgun-certificate": good_on_application_document_formatter,
        },
    )


def platform_summary(good, queue_pk, application_pk):
    def product_document_formatter(document):
        url = _get_document_url(queue_pk, application_pk, document)
        return document_formatter(document, url)

    return core_platform_summary(
        good,
        {
            "product-document": product_document_formatter,
        },
    )


def platform_product_on_application_summary(good_on_application, queue_pk, application_pk):
    return core_platform_product_on_application_summary(good_on_application)


def material_summary(good, queue_pk, application_pk):
    def product_document_formatter(document):
        url = _get_document_url(queue_pk, application_pk, document)
        return document_formatter(document, url)

    return core_material_summary(
        good,
        {
            "product-document": product_document_formatter,
        },
    )


def material_product_on_application_summary(good_on_application, queue_pk, application_pk):
    return core_material_product_on_application_summary(good_on_application)


def software_summary(good, queue_pk, application_pk):
    def product_document_formatter(document):
        url = _get_document_url(queue_pk, application_pk, document)
        return document_formatter(document, url)

    return core_software_summary(
        good,
        {
            "product-document": product_document_formatter,
        },
    )


def software_product_on_application_summary(good_on_application, queue_pk, application_pk):
    return core_software_product_on_application_summary(good_on_application)
