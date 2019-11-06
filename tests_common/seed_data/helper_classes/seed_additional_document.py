from seed_data.helper_classes import seed_class
from seed_data import make_requests


class SeedAdditionalDocument(seed_class.SeedClass):
    def add_additional_document(self, draft_id, additional_documents):
        self.log("Adding additional document: ...")
        additional_documents_data = \
            self.request_data['additional_document'] if additional_documents is None else additional_documents
        additional_document = make_requests.make_request('POST', base_url=self.base_url,
                                                         url='/applications/' + draft_id + '/documents/',
                                                         headers=self.export_headers,
                                                         body=additional_documents_data).json()['document']
        self.add_to_context('additional_document', additional_document)
        return self.context['additional_document']['id']
