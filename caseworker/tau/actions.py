from http import HTTPStatus
from core.decorators import expect_status
from caseworker.tau.services import (
    post_document_internal_good_on_application,
    delete_good_on_application_document,
    edit_good_on_application_document,
)
from core.helpers import get_document_data


class GoodOnApplicationInternalDocumentAction:
    def __init__(self, request, good, file=None, file_title=None):
        self.request = request
        self.good = good
        self.file = file
        self.file_title = file_title

    def run(self):
        if self.file:
            # We have uploaded a file
            if self.has_existing_evidence_document():
                # Lets delete old document
                self.delete_good_on_application_document()
            # Recreate with new document details
            self.post_good_on_application_document()
        elif self.file_title and self.has_existing_evidence_document():
            # This is an edit
            self.edit_good_on_application_document()

    def get_evidence_document_payload(self):
        payload = {
            **get_document_data(self.file),
            "document_title": self.file_title,
        }
        return payload

    def get_evidence_doc(self):
        return self.good["good_application_internal_documents"][0]

    def has_existing_evidence_document(self):
        return len(self.good["good_application_internal_documents"]) > 0

    @expect_status(
        HTTPStatus.CREATED,
        "Error adding evidence file",
        "Unexpected error evidence file",
    )
    def post_good_on_application_document(self):
        evidence_file_payload = self.get_evidence_document_payload()

        return post_document_internal_good_on_application(
            self.request, goods_on_application_pk=self.good["id"], data=evidence_file_payload
        )

    @expect_status(
        HTTPStatus.OK,
        "Error delete evidence file",
        "Unexpected deleting file",
    )
    def delete_good_on_application_document(self):
        return delete_good_on_application_document(
            self.request,
            doc_pk=self.get_evidence_doc()["id"],
        )

    @expect_status(
        HTTPStatus.OK,
        "Error edit evidence file",
        "Unexpected editing file",
    )
    def edit_good_on_application_document(self):
        payload = {
            "document_title": self.file_title,
        }
        return edit_good_on_application_document(
            self.request,
            doc_pk=self.get_evidence_doc()["id"],
            data=payload,
        )
