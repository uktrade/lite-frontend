from shared.seed_data.seed_data_classes.seed_class import SeedClass
from shared.seed_data.make_requests import make_request

class SeedGood(SeedClass):
    def post_good(self, key):
        data = self.request_data[key]
        item = make_request('POST', base_url=self.base_url, url='/goods/',
                                     headers=self.export_headers, body=data).json()['good']
        self.add_good_document(item['id'])
        return item

    def add_good(self):
        self.log('Adding good: ...')
        item = self.post_good('good')
        self.add_to_context('good_id', item['id'])

    def add_good_document(self, good_id):
        data = [self.request_data['document']]
        make_request("POST", base_url=self.base_url, url='/goods/' + good_id + '/documents/',
                     headers=self.export_headers, body=data)

    def add_good_end_product(self, item):
        #'good_end_product_false' for add_good_end_product_false
        #'good_end_product_true' for add_good_end_product_true
        self.log('Adding good: ...')
        good = self.find_good_by_name(self.request_data[item]['description'])
        if not good:
            self.post_good(item)
        self.add_to_context('goods_name', self.request_data[item]['description'])
