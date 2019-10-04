from shared.seed_data.seed_data_classes.seed_class import SeedClass
from shared.seed_data.make_requests import make_request


class SeedAdditionalDocument(SeedClass):
    def add_additional_document(self, draft_id, additional_documents):
        self.log("Adding additional document: ...")
        additional_documents_data = \
            self.request_data['additional_document'] if additional_documents is None else additional_documents
        additional_document = make_request('POST', base_url=self.base_url, url='/drafts/' + draft_id + '/documents/',
                                                     headers=self.export_headers, body=additional_documents_data).json()['document']
        self.add_to_context('additional_document', additional_document)
        return self.context['additional_document']['id']
