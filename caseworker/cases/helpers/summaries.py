from django.urls import reverse

from core.summaries.formatters import (
    document_formatter,
)
from core.summaries.summaries import (
    firearm_summary as core_firearm_summary,
    firearm_on_application_summary as core_firearm_on_application_summary,
    get_summary_type_for_good_on_application,
    material_summary as core_material_summary,
    material_product_on_application_summary as core_material_product_on_application_summary,
    NoSummaryForType,
    platform_summary as core_platform_summary,
    platform_product_on_application_summary as core_platform_product_on_application_summary,
    technology_summary as core_technology_summary,
    technology_product_on_application_summary as core_technology_product_on_application_summary,
    component_summary as core_component_summary,
    component_product_on_application_summary as core_component_summary_on_application_summary,
    SummaryTypes,
)

from caseworker.cases.services import get_good_on_application_documents


def _get_document_url(queue_pk, application_pk, document):
    return reverse(
        "cases:document",
        kwargs={
            "queue_pk": queue_pk,
            "pk": application_pk,
            "file_pk": document["id"],
        },
    )


def organisation_document_formatter_factory(queue_pk, application_pk):
    def organisation_document_formatter(document):
        url = _get_document_url(queue_pk, application_pk, document["document"])
        return document_formatter(document["document"], url)

    return organisation_document_formatter


def product_document_formatter_factory(queue_pk, application_pk):
    def product_document_formatter(document):
        url = _get_document_url(queue_pk, application_pk, document)
        return document_formatter(document, url)

    return product_document_formatter


def good_on_application_document_formatter_factory(queue_pk, application_pk):
    def good_on_application_document_formatter(document):
        url = _get_document_url(queue_pk, application_pk, document)
        return document_formatter(document, url)

    return good_on_application_document_formatter


def firearm_summary(good, queue_pk, application_pk, is_user_rfd, organisation_documents):
    product_document_formatter = product_document_formatter_factory(
        queue_pk,
        application_pk,
    )
    organisation_document_formatter = organisation_document_formatter_factory(queue_pk, application_pk)

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


def firearm_on_application_summary(good_on_application, queue_pk, application_pk, good_on_application_documents):
    good_on_application_document_formatter = good_on_application_document_formatter_factory(queue_pk, application_pk)
    return core_firearm_on_application_summary(
        good_on_application,
        good_on_application_documents,
        {
            "firearm-certificate": good_on_application_document_formatter,
            "shotgun-certificate": good_on_application_document_formatter,
        },
    )


def platform_summary(good, queue_pk, application_pk, *args, **kwargs):
    product_document_formatter = product_document_formatter_factory(queue_pk, application_pk)
    return core_platform_summary(
        good,
        {
            "product-document": product_document_formatter,
        },
    )


def platform_product_on_application_summary(good_on_application, *args, **kwargs):
    return core_platform_product_on_application_summary(good_on_application)


def material_summary(good, queue_pk, application_pk, *args, **kwargs):
    product_document_formatter = product_document_formatter_factory(queue_pk, application_pk)
    return core_material_summary(
        good,
        {
            "product-document": product_document_formatter,
        },
    )


def material_product_on_application_summary(good_on_application, *args, **kwargs):
    return core_material_product_on_application_summary(good_on_application)


def technology_summary(good, queue_pk, application_pk, *args, **kwargs):
    product_document_formatter = product_document_formatter_factory(queue_pk, application_pk)
    return core_technology_summary(
        good,
        {
            "product-document": product_document_formatter,
        },
    )


def component_product_on_application_summary(good_on_application, *args, **kwargs):
    return core_component_summary_on_application_summary(good_on_application)


def component_summary(good, queue_pk, application_pk, *args, **kwargs):
    def product_document_formatter(document):
        url = _get_document_url(queue_pk, application_pk, document)
        return document_formatter(document, url)

    return core_component_summary(
        good,
        {
            "product-document": product_document_formatter,
        },
    )


def technology_product_on_application_summary(good_on_application, *args, **kwargs):
    return core_technology_product_on_application_summary(good_on_application)


def get_good_on_application_summary(
    request,
    good_on_application,
    queue_pk,
    application_pk,
    is_user_rfd,
    organisation_documents,
):
    try:
        summary_type = get_summary_type_for_good_on_application(good_on_application)
    except NoSummaryForType:
        return None

    summary_type_map = {
        SummaryTypes.FIREARM: (
            firearm_summary,
            firearm_on_application_summary,
        ),
        SummaryTypes.PLATFORM: (
            platform_summary,
            platform_product_on_application_summary,
        ),
        SummaryTypes.MATERIAL: (
            material_summary,
            material_product_on_application_summary,
        ),
        SummaryTypes.TECHNOLOGY: (
            technology_summary,
            technology_product_on_application_summary,
        ),
        SummaryTypes.COMPONENT: (
            component_summary,
            component_product_on_application_summary,
        ),
    }

    _product_summary, _product_on_application_summary = summary_type_map[summary_type]

    organisation_documents = {document["document_type"]: document for document in organisation_documents.values()}
    good_on_application_documents = get_good_on_application_documents(
        request,
        application_pk,
        good_on_application["good"]["id"],
    )
    good_on_application_documents = {
        item["document_type"]: item for item in good_on_application_documents["documents"] if item.get("document_type")
    }

    product_summary = _product_summary(
        good_on_application["good"],
        queue_pk,
        application_pk,
        is_user_rfd,
        organisation_documents,
    )
    product_on_application_summary = _product_on_application_summary(
        good_on_application,
        queue_pk,
        application_pk,
        good_on_application_documents,
    )

    return product_summary + product_on_application_summary
