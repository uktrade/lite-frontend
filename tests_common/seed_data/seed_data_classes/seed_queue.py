from shared.seed_data.seed_data_classes.seed_class import SeedClass
from shared.seed_data.make_requests import make_request


class SeedQueue(SeedClass):
    def add_queue(self, queue_name):
        self.log("adding queue: ...")
        self.context['queue_name'] = queue_name
        data = {'team': '00000000-0000-0000-0000-000000000001',
                'name': queue_name
                }
        response = make_request("POST", base_url=self.base_url, url='/queues/', headers=self.gov_headers, body=data)
        item = response.json()['queue']
        self.add_to_context('queue_id', item['id'])

    def get_queues(self):
        self.log("getting queues: ...")
        response = make_request("GET", base_url=self.base_url, url='/queues/', headers=self.gov_headers)
        queues = response.json()['queues']
        return queues
