from shared.seed_data.seed_data_classes.seed_class import SeedClass
from shared.seed_data.make_requests import make_request

class SeedClc(SeedClass):
    def add_clc_query(self, seed_good):
        self.log("Adding clc query: ...")
        item = seed_good.post_good('clc_good')
        data = {
            'not_sure_details_details': 'something',
            'not_sure_details_control_code': 'ML1a',
            'good_id': item['id']
        }
        case_id = make_request("POST", base_url=self.base_url, url='/queries/control-list-classifications/',
                               headers=self.export_headers, body=data).json()['case_id']
        self.add_to_context('case_id', case_id)

    def add_clc_good(self, seed_good):
        self.log('Adding clc good: ...')
        data = self.request_data['clc_good']
        response = make_request('POST', base_url=self.base_url, url='/goods/', headers=self.export_headers, body=data)
        item = response.json()['good']
        self.add_to_context('clc_good_id', item['id'])
        seed_good.add_good_document(item['id'])
        data = {'good_id': self.context['clc_good_id'],
                'not_sure_details_control_code': 'ML1a',
                'not_sure_details_details': 'b'}
        response = make_request('POST', base_url=self.base_url, url='/queries/control-list-classifications/', headers=self.export_headers,
                                     body=data)
        response_data = response.json()
        self.add_ecju_query(response_data['case_id'])
