from django.urls import reverse


def get_document_url(document):
    return reverse(
        "organisation:document",
        kwargs={
            "pk": document["id"],
        },
    )
