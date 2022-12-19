import uuid

from unittest.mock import Mock

from django.urls import reverse

from caseworker.core.helpers import get_organisation_documents


def test_get_organisation_documents():
    document_id = str(uuid.uuid4())
    queue_id = str(uuid.uuid4())

    case = Mock()
    case.id = str(uuid.uuid4())
    case.organisation = {
        "documents": [
            {
                "document_type": "document-type",
                "document": {
                    "id": document_id,
                },
            },
        ],
    }
    assert get_organisation_documents(case, queue_id) == {
        "document_type": {
            "document": {
                "id": document_id,
                "url": reverse(
                    "cases:document",
                    kwargs={
                        "queue_pk": queue_id,
                        "pk": case.id,
                        "file_pk": document_id,
                    },
                ),
            },
            "document_type": "document-type",
        },
    }
