from ...seed_data.seed_data_classes.seed_class import SeedClass
from ...seed_data.make_requests import make_request


class SeedGood(SeedClass):
    def post_good(self, key):
        data = self.request_data[key]
        item = make_request('POST', base_url=self.base_url, url='/goods/',
                            headers=self.export_headers, body=data).json()['good']
        self.add_good_document(item['id'])
        return item

    def add_good_to_draft(self, draft_id, good):
        self.log("Adding good to draft: ...")
        good = self.request_data['add_good'] if good is None else good
        good['good_id'] = self.context['good_id']
        make_request("POST", base_url=self.base_url, url='/applications/' + draft_id + '/goods/',
                     headers=self.export_headers, body=good)

    def add_good(self):
        self.log('Adding good: ...')
        item = self.post_good('good')
        self.add_to_context('good_id', item['id'])

    def add_good_document(self, good_id):
        data = [self.request_data['document']]
        make_request("POST", base_url=self.base_url, url='/goods/' + good_id + '/documents/',
                     headers=self.export_headers, body=data)

    def add_good_end_product(self, item):
        # 'good_end_product_false' for add_good_end_product_false
        # 'good_end_product_true' for add_good_end_product_true
        self.log('Adding good: ...')
        good = self.find_good_by_name(self.request_data[item]['description'])
        if not good:
            self.post_good(item)
        self.add_to_context('goods_name', self.request_data[item]['description'])

    def find_good_by_name(self, good_name):
        goods = make_request('GET', base_url=self.base_url, url='/goods/', headers=self.export_headers).json()['goods']
        good = next((item for item in goods if item['description'] == good_name), None)
        return good

    def add_open_draft_good(self, draft_id):
        self.log("Adding goods_type: ...")
        data = self.request_data['good_type']
        data['application'] = draft_id
        make_request("POST", base_url=self.base_url, url='/goodstype/', headers=self.export_headers, body=data)
