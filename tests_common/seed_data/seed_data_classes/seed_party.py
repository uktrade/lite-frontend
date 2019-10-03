from shared.seed_data.seed_data_classes.seed_class import SeedClass
from shared.seed_data.make_requests import make_request


class SeedParty(SeedClass):
    def add_document(self, url):
        data = self.request_data['document']
        make_request("POST", base_url=self.base_url, url=url, headers=self.export_headers, body=data)

    def add_end_user_document(self, draft_id):
        self.add_document('/drafts/' + draft_id + '/end-user/document/')

    def add_ultimate_end_user_document(self, draft_id, ultimate_end_user_id):
        self.add_document('/drafts/' + draft_id + '/ultimate-end-user/' + ultimate_end_user_id + '/document/')

    def add_third_party_document(self, draft_id, third_party_id):
        self.add_document('/drafts/' + draft_id + '/third-parties/' + third_party_id + '/document/')

    def add_consignee_document(self, draft_id):
        self.add_document('/drafts/' + draft_id + '/consignee/document/')
