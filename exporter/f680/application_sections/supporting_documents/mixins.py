from http import HTTPStatus

from exporter.applications.services import get_application_supporting_document
from core.decorators import expect_status
from exporter.f680.services import get_f680_application, patch_f680_application


class F680SupportingDocumentsMixin:

    @expect_status(
        HTTPStatus.OK,
        "Error getting F680 documents",
        "Unexpected error getting F680 documents",
        reraise_404=True,
    )
    def get_f680_supporting_documents(self, application_id):
        return get_application_supporting_document(self.request, application_id)

    @expect_status(
        HTTPStatus.OK,
        "Error retrieving F680 application",
        "Unexpected error retrieving F680 application",
        reraise_404=True,
    )
    def get_f680_application(self, pk):
        return get_f680_application(self.request, pk)

    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)
        self.application_id = str(kwargs["pk"])
        self.application, _ = self.get_f680_application(kwargs["pk"])
        self.supporting_documents, _ = self.get_f680_supporting_documents(self.application_id)

    @expect_status(
        HTTPStatus.OK,
        "Error updating F680 application",
        "Unexpected error updating F680 application",
    )
    def patch_f680_application(self, data):
        return patch_f680_application(self.request, self.application["id"], data)
