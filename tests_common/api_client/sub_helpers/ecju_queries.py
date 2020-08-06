class EcjuQueries:
    def __init__(self, api_client, request_data, **kwargs):
        super().__init__(**kwargs)
        self.api_client = api_client
        self.request_data = request_data

    def add_ecju_response(self, question, response):
        case_id = self.api_client.context["case_id"]
        ecju_queries = self.api_client.make_request(
            method="GET", url="/cases/" + case_id + "/ecju-queries/", headers=self.api_client.gov_headers,
        ).json()["ecju_queries"]

        ecju_query_id = None
        for ecju_query in ecju_queries:
            if ecju_query["question"] == question:
                ecju_query_id = ecju_query["id"]
                break

        self.api_client.make_request(
            method="PUT",
            url="/cases/" + case_id + "/ecju-queries/" + ecju_query_id + "/",
            headers=self.api_client.exporter_headers,
            body={"response": response},
        )

    def add_ecju_query(self, case_id):
        self.api_client.make_request(
            method="POST",
            url="/cases/" + case_id + "/ecju-queries/",
            headers=self.api_client.gov_headers,
            body=self.request_data["ecju_query"],
        )
