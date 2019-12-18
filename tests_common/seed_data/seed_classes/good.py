from .seed_class import SeedClass
from ..make_requests import make_request


class Good(SeedClass):
    def __init__(self, base_url, gov_headers, export_headers, request_data, context):
        super(Good, self).__init__(base_url, gov_headers, export_headers, request_data, context)
        self.add_good()

    def post_good(self, data):
        item = make_request(
            "POST", base_url=self.base_url, url="/goods/", headers=self.export_headers, body=data,
        ).json()["good"]
        self.add_good_document(item["id"])
        return item

    def get_goods(self):
        return make_request("GET", base_url=self.base_url, url="/goods/", headers=self.export_headers).json()["goods"]

    def add_good_to_draft(self, draft_id, good):
        good = self.request_data["add_good"] if good is None else good
        good["good_id"] = self.context["good_id"]
        make_request(
            "POST",
            base_url=self.base_url,
            url="/applications/" + draft_id + "/goods/",
            headers=self.export_headers,
            body=good,
        )

    def add_good(self, good=None):
        data = good if good else self.request_data["good"]
        item = self.post_good(data)
        self.add_to_context("good_id", item["id"])

    def add_good_document(self, good_id):
        data = [self.request_data["document"]]
        make_request(
            "POST",
            base_url=self.base_url,
            url="/goods/" + good_id + "/documents/",
            headers=self.export_headers,
            body=data,
        )
        self.add_to_context("document", self.request_data["document"])

    def add_good_end_product(self, item):
        good = self.find_good_by_name(self.request_data[item]["description"])
        if not good:
            self.post_good(self.request_data[item])
        self.add_to_context("goods_name", self.request_data[item]["description"])

    def find_good_by_name(self, good_name):
        goods = make_request("GET", base_url=self.base_url, url="/goods/", headers=self.export_headers).json()["goods"]
        good = next((item for item in goods if item["description"] == good_name), None)
        return good

    def add_open_draft_good(self, draft_id):
        data = self.request_data["good_type"]
        data["application"] = draft_id
        make_request(
            "POST",
            base_url=self.base_url,
            url="/applications/" + draft_id + "/goodstypes/",
            headers=self.export_headers,
            body=data,
        )
