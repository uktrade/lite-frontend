from shared.seed_data.make_requests import make_request
from shared.tools.wait import wait_for_ultimate_end_user_document, wait_for_third_party_document, wait_for_additional_document, wait_for_document


def check_documents(self, draft_id, ultimate_end_user_id, third_party_id, additional_document_id):
    end_user_document_is_processed = wait_for_document(
        func=self.check_end_user_document_is_processed, draft_id=draft_id)
    assert end_user_document_is_processed, "End user document wasn't successfully processed"
    consignee_document_is_processed = wait_for_document(
        func=self.check_consignee_document_is_processed, draft_id=draft_id)
    assert consignee_document_is_processed, "Consignee document wasn't successfully processed"
    ultimate_end_user_document_is_processed = wait_for_ultimate_end_user_document(
        func=self.check_ultimate_end_user_document_is_processed, draft_id=draft_id,
        ultimate_end_user_id=ultimate_end_user_id)
    assert ultimate_end_user_document_is_processed, "Ultimate end user document wasn't successfully processed"
    third_party_document_is_processed = wait_for_third_party_document(
        func=self.check_third_party_document_is_processed, draft_id=draft_id,
        third_party_id=third_party_id)
    assert third_party_document_is_processed, "Third party document wasn't successfully processed"
    additional_document_is_processed = wait_for_additional_document(
        func=self.check_additional_document_is_processed, draft_id=draft_id,
        document_id=additional_document_id)
    assert additional_document_is_processed, "Additional document wasn't successfully processed"

def check_document(self, url):
    response = make_request("GET", base_url=self.base_url, url=url, headers=self.export_headers)
    return response.json()['document']['safe']

def check_end_user_document_is_processed(self, draft_id):
    return self.check_document('/drafts/' + draft_id + '/end-user/document/')

def check_consignee_document_is_processed(self, draft_id):
    return self.check_document('/drafts/' + draft_id + '/consignee/document/')

def check_ultimate_end_user_document_is_processed(self, draft_id, ultimate_end_user_id):
    return self.check_document('/drafts/' + draft_id + '/ultimate-end-user/' + ultimate_end_user_id + '/document/')

def check_third_party_document_is_processed(self, draft_id, third_party_id):
    return self.check_document('/drafts/' + draft_id + '/third-parties/' + third_party_id + '/document/')

def check_additional_document_is_processed(self, draft_id, document_id):
    return self.check_document('/drafts/' + draft_id + '/documents/' + document_id + '/')
