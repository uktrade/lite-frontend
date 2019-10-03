from shared.seed_data.seed_data_classes.seed_class import SeedClass
from shared.seed_data.make_requests import make_request

class SeedEcju(SeedClass):
    def add_ecju_response(self, question, response):
        self.log("adding response to ecju: ...")
        case_id = self.context['case_id']
        ecju_queries = make_request("GET", base_url=self.base_url, url='/cases/' + case_id + '/ecju-queries/', headers=self.gov_headers)
        ecju_query_id = None
        for ecju_query in ecju_queries.json()['ecju_queries']:
            if ecju_query['question'] == question:
                ecju_query_id = ecju_query['id']
                break
        data = {'response': response}
        make_request("PUT", base_url=self.base_url, url='/cases/' + case_id + '/ecju-queries/' + ecju_query_id + '/',
                          headers=self.export_headers, body=data)

    def add_ecju_query(self, case_id):
        self.log("Creating ecju query: ...")
        data = self.request_data['ecju_query']
        make_request("POST", base_url=self.base_url, url='/cases/' + case_id + '/ecju-queries/',
                     headers=self.gov_headers, body=data)  # noqa
