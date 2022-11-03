from django import template

from core.constants import (
    FirearmsActDocumentType,
    OrganisationDocumentType,
)


register = template.Library()


@register.filter(name="is_system_document")
def is_system_document(document):
    return document.get("document_type") in [
        OrganisationDocumentType.RFD_CERTIFICATE,
        FirearmsActDocumentType.SECTION_1,
        FirearmsActDocumentType.SECTION_2,
        FirearmsActDocumentType.SECTION_5,
    ]
