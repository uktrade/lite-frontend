class GoodsQueries:
    def __init__(self, api_client, request_data, **kwargs):
        super().__init__(**kwargs)
        self.api_client = api_client
        self.request_data = request_data

    def submit_to_goods_queries(self, good_id):
        data = self.request_data["not_sure_details"]
        data["good_id"] = good_id
        return self.api_client.make_request(
            method="POST",
            url="/queries/goods-queries/",
            headers=self.api_client.exporter_headers,
            body=data,
        ).json()["id"]

    def add_goods_clc_query(self, seed_good):
        good = seed_good.post_good(self.request_data["clc_good"])
        case_id = self.submit_to_goods_queries(good["id"])
        self.api_client.add_to_context("case_id", case_id)

    def add_clc_good(self, seed_good, seed_ecju):
        good = seed_good.post_good(self.request_data["clc_good"])
        case_id = self.submit_to_goods_queries(good["id"])
        self.api_client.add_to_context("goods_query_good_id", good["id"])
        seed_ecju.add_ecju_query(case_id)

    def add_goods_grading_query(self, seed_good):
        good = seed_good.post_good(self.request_data["grading_good"])
        case_id = self.submit_to_goods_queries(good["id"])
        self.api_client.add_to_context("case_id", case_id)

    def add_grading_good(self, seed_good, seed_ecju):
        good = seed_good.post_good(self.request_data["grading_good"])
        case_id = self.submit_to_goods_queries(good["id"])
        self.api_client.add_to_context("goods_query_good_id", good["id"])
        seed_ecju.add_ecju_query(case_id)
