from django import template

from exporter.core.constants import DocumentType


register = template.Library()


@register.filter(name="is_system_document")
def is_system_document(document):
    return document.get("document_type") in [DocumentType.RFD_CERTIFICATE]
