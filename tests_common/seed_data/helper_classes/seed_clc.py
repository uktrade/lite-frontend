from . import seed_class
from .. import make_requests


class SeedClc(seed_class.SeedClass):
    def submit_to_control_list_classification(self, good_id):
        data = self.request_data['not_sure_details']
        data['good_id'] = good_id
        return make_requests.make_request('POST', base_url=self.base_url, url='/queries/control-list-classifications/',
                                          headers=self.export_headers, body=data).json()['case_id']

    def add_clc_query(self, seed_good):
        self.log("Adding clc query: ...")
        good = seed_good.post_good(self.request_data['clc_good'])
        case_id = self.submit_to_control_list_classification(good['id'])
        self.add_to_context('case_id', case_id)

    def add_clc_good(self, seed_good, seed_ecju):
        self.log('Adding clc good: ...')
        good = seed_good.post_good(self.request_data['clc_good'])
        case_id = self.submit_to_control_list_classification(good['id'])
        self.add_to_context('clc_good_id', good['id'])
        seed_ecju.add_ecju_query(case_id)
