from shared.seed_data.seed_data_classes.seed_class import SeedClass
from shared.seed_data.make_requests import make_request

class SeedOrganisation(SeedClass):
    def setup_org(self):
        organisation = self.find_org_by_name(self.request_data['organisation']['name'])
        if not organisation:
            organisation = self.add_org('organisation')
        org_id = organisation['id']
        self.add_to_context('org_id', org_id)
        self.add_to_context('first_name', self.request_data['organisation']['user']['first_name'])
        self.add_to_context('last_name', self.request_data['organisation']['user']['last_name'])
        self.add_to_context('primary_site_id', self.get_org_primary_site_id(org_id))
        self.add_to_context('org_name', self.request_data['organisation']['name'])

    def setup_org_for_switching_organisations(self):
        organisation = self.find_org_by_name(self.request_data['organisation_for_switching_organisations']['name'])
        if not organisation:
            self.add_org('organisation_for_switching_organisations')
        self.add_to_context('org_name_for_switching_organisations',
                            self.request_data['organisation_for_switching_organisations']['name'])
