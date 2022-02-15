class Queues:
    def __init__(self, api_client, request_data, **kwargs):
        super().__init__(**kwargs)
        self.api_client = api_client
        self.request_data = request_data

    def add_queue(self, queue_name):
        self.api_client.context["queue_name"] = queue_name
        data = self.request_data["queue"]
        data["name"] = queue_name
        queue = self.api_client.make_request(
            method="POST",
            url="/queues/",
            headers=self.api_client.gov_headers,
            body=data,
        ).json()["queue"]
        self.api_client.add_to_context("queue_id", queue["id"])
        self.api_client.add_to_context("queue_name", queue["name"])

    def get_queues(self):
        return self.api_client.make_request(method="GET", url="/queues/", headers=self.api_client.gov_headers).json()[
            "queues"
        ]

    def case_assignment(self, queue_pk, case_pk, users):
        data = {"case_assignments": [{"case_id": case_pk, "users": users}]}
        self.api_client.make_request(
            method="PUT",
            url="/queues/" + queue_pk + "/case-assignments/",
            headers=self.api_client.gov_headers,
            body=data,
        )
