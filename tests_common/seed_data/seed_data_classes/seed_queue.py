from shared.seed_data.seed_data_classes.seed_class import SeedClass
from shared.seed_data.make_requests import make_request


class SeedQueue(SeedClass):
    def add_queue(self, queue_name):
        self.log("adding queue: ...")
        self.context['queue_name'] = queue_name
        data = self.request_data['queue']
        data['name'] = queue_name
        queue = make_request("POST", base_url=self.base_url, url='/queues/',
                             headers=self.gov_headers, body=data).json()['queue']
        self.add_to_context('queue_id', queue['id'])

    def get_queues(self):
        self.log("getting queues: ...")
        return make_request("GET", base_url=self.base_url, url='/queues/',
                            headers=self.gov_headers).json()['queues']
