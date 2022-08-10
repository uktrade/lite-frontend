from django.urls import reverse

from core.summaries.formatters import (
    document_formatter,
)
from core.summaries.summaries import (
    platform_summary as core_platform_summary,
    platform_product_on_application_summary as core_platform_product_on_application_summary,
)


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
