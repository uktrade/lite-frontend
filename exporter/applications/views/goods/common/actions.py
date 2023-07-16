from http import HTTPStatus

from core.decorators import expect_status
from core.helpers import get_document_data

from exporter.applications.views.goods.common.constants import PRODUCT_DOCUMENT_UPLOAD
from exporter.goods.services import post_good_documents


class ProductDocumentAction:
    def __init__(self, wizard):
        self.wizard = wizard
        self.request = wizard.request
        self.good = wizard.good

    def has_product_documentation(self):
        return self.wizard.condition_dict[PRODUCT_DOCUMENT_UPLOAD](self.wizard)

    def get_product_document_payload(self):
        data = self.wizard.get_cleaned_data_for_step(PRODUCT_DOCUMENT_UPLOAD)
        document = data["product_document"]
        payload = {
            **get_document_data(document),
            "description": data["description"],
        }
        return payload

    @expect_status(
        HTTPStatus.CREATED,
        "Error adding product document",
        "Unexpected error adding product document",
    )
    def post_product_documentation(self):
        document_payload = self.get_product_document_payload()
        return post_good_documents(
            request=self.request,
            pk=self.good["id"],
            json=document_payload,
        )

    def run(self):
        if not self.has_product_documentation():
            return
        self.post_product_documentation()
