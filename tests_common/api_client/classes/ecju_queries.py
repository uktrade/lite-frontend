from .api_client import ApiClient


class EcjuQueries(ApiClient):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def add_ecju_response(self, question, response):
        case_id = self.context["case_id"]
        ecju_queries = self.make_request(
            method="GET", url="/cases/" + case_id + "/ecju-queries/", headers=ApiClient.gov_headers,
        ).json()["ecju_queries"]

        ecju_query_id = None
        for ecju_query in ecju_queries:
            if ecju_query["question"] == question:
                ecju_query_id = ecju_query["id"]
                break

        self.make_request(
            method="PUT",
            url="/cases/" + case_id + "/ecju-queries/" + ecju_query_id + "/",
            headers=ApiClient.exporter_headers,
            body={"response": response},
        )

    def add_ecju_query(self, case_id):
        self.make_request(
            method="POST",
            url="/cases/" + case_id + "/ecju-queries/",
            headers=ApiClient.gov_headers,
            body=self.request_data["ecju_query"],
        )
