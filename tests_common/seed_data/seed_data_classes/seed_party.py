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

    def add_eua_query(self):
        self.log("Adding end user advisory: ...")
        data = self.request_data['end_user_advisory']
        response = make_request("POST", base_url=self.base_url, url='/queries/end-user-advisories/', headers=self.export_headers, body=data)
        id = response.json()['end_user_advisory']['id']
        self.add_to_context('end_user_advisory_id', str(id))
        response = make_request("GET", base_url=self.base_url, url='/queries/end-user-advisories/' + str(id) + '/', headers=self.export_headers)
        self.add_to_context('end_user_advisory_case_id', response.json()['case_id'])

    def add_end_user(self, draft_id, enduser):
        self.log("Adding end user: ...")
        end_user_data = self.request_data['end-user'] if enduser is None else enduser
        end_user = make_request("POST", base_url=self.base_url, url='/drafts/' + draft_id + '/end-user/',
                                     headers=self.export_headers,
                                     body=end_user_data).json()['end_user']
        self.log("Adding end user document: ...")
        self.seed_party.add_end_user_document(draft_id)
        self.add_to_context('end_user', end_user)
