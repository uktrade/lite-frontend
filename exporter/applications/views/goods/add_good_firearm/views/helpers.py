from django.urls import reverse


def get_organisation_document_url(document):
    return reverse(
        "organisation:document",
        kwargs={
            "pk": document["id"],
        },
    )


def get_good_on_application_document_url(application, good, document):
    return reverse(
        "applications:good-on-application-document",
        kwargs={
            "pk": application["id"],
            "good_pk": good["id"],
            "doc_pk": document["id"],
        },
    )
