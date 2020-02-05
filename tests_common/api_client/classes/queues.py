from .api_client import ApiClient


class Queues(ApiClient):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def add_queue(self, queue_name):
        self.context["queue_name"] = queue_name
        data = self.request_data["queue"]
        data["name"] = queue_name
        queue = self.make_request(method="POST", url="/queues/", headers=ApiClient.gov_headers, body=data,).json()[
            "queue"
        ]
        self.add_to_context("queue_id", queue["id"])

    def get_queues(self):
        return self.make_request(method="GET", url="/queues/", headers=ApiClient.gov_headers).json()["queues"]
