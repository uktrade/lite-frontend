from . import seed_class
from .. import make_requests


class SeedEcju(seed_class.SeedClass):
    def add_ecju_response(self, question, response):
        self.log("adding response to ecju: ...")
        case_id = self.context['case_id']
        ecju_queries = make_requests.make_request("GET", base_url=self.base_url, url='/cases/' + case_id + '/ecju-queries/',
                                                  headers=self.gov_headers).json()['ecju_queries']
        ecju_query_id = None
        for ecju_query in ecju_queries:
            if ecju_query['question'] == question:
                ecju_query_id = ecju_query['id']
                break
        make_requests.make_request("PUT", base_url=self.base_url, url='/cases/' + case_id + '/ecju-queries/' + ecju_query_id + '/',
                                   headers=self.export_headers, body={'response': response})

    def add_ecju_query(self, case_id):
        self.log("Creating ecju query: ...")
        make_requests.make_request("POST", base_url=self.base_url, url='/cases/' + case_id + '/ecju-queries/',
                                   headers=self.gov_headers, body=self.request_data['ecju_query'])
