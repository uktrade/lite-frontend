from . import seed_class
from .. import make_requests


class SeedQueue(seed_class.SeedClass):
    def add_queue(self, queue_name):
        self.log("adding queue: ...")
        self.context['queue_name'] = queue_name
        data = self.request_data['queue']
        data['name'] = queue_name
        queue = make_requests.make_request("POST", base_url=self.base_url, url='/queues/',
                                           headers=self.gov_headers, body=data).json()['queue']
        self.add_to_context('queue_id', queue['id'])

    def get_queues(self):
        self.log("getting queues: ...")
        return make_requests.make_request("GET", base_url=self.base_url, url='/queues/',
                                          headers=self.gov_headers).json()['queues']
