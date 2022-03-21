from faker import Faker

fake = Faker()


class Goods:
    def __init__(self, api_client, documents, request_data, **kwargs):
        super().__init__(**kwargs)
        self.api_client = api_client
        self.documents = documents
        self.request_data = request_data

    def post_good(self, data):
        item = self.api_client.make_request(
            method="POST",
            url="/goods/",
            headers=self.api_client.exporter_headers,
            body=data,
        ).json()["good"]
        self.add_goods_document(item["id"])
        return item

    def get_goods(self, extra_params=""):
        return self.api_client.make_request(
            method="GET", url="/goods/?" + extra_params, headers=self.api_client.exporter_headers
        ).json()["results"]

    def add_good_to_draft(self, draft_id, good, count=0):
        if not good.get("good_id"):
            data = self.request_data["good"]
            item = self.post_good(data)
            self.api_client.add_to_context("good_id", item["id"])
            self.api_client.add_to_context(f"good_id{count}", item["id"])
            good["good_id"] = item["id"]

        good_on_app = good or self.request_data["add_good"]
        item = self.api_client.make_request(
            method="POST",
            url="/applications/" + draft_id + "/goods/",
            headers=self.api_client.exporter_headers,
            body=good_on_app,
        ).json()["good"]
        self.api_client.add_to_context("good_on_application_id", item["id"])
        self.api_client.add_to_context(f"good_on_application_id{count}", item["id"])

    def add_good(self, good=None):
        data = good or self.request_data["good"]
        item = self.post_good(data)
        self.api_client.add_to_context("good_id", item["id"])

    def add_goods_document(self, good_id):
        url = "/goods/" + good_id + "/documents/"
        goods_document_metadata = self.documents.add_document(
            url=url, name="goods document", description="this is a test goods document", multi_upload_endpoint=True
        )
        self.api_client.add_to_context("goods_document", goods_document_metadata)

    def add_good_end_product(self, item):
        good = self.find_good_by_name(self.request_data[item]["description"])
        if not good:
            self.post_good(self.request_data[item])
        self.api_client.add_to_context("goods_name", self.request_data[item]["description"])

    def find_good_by_name(self, good_name):
        goods = self.api_client.make_request(
            method="GET", url="/goods/", headers=self.api_client.exporter_headers
        ).json()["results"]
        good = next((item for item in goods if item["description"] == good_name), None)
        return good

    def add_open_draft_good(self, draft_id):
        data = self.request_data["good_type"]
        data["application"] = draft_id
        self.api_client.make_request(
            method="POST",
            url="/applications/" + draft_id + "/goodstypes/",
            headers=self.api_client.exporter_headers,
            body=data,
        )

    def add_hmrc_goods_type(self, hmrc_draft_id):
        data = {"description": fake.bs()}
        self.api_client.make_request(
            method="POST",
            url="/applications/" + hmrc_draft_id + "/goodstypes/",
            headers=self.api_client.exporter_headers,
            body=data,
        )

    def update_good_clc(self, *, good_id, good_on_application_id, case_id, **kwargs):
        self.api_client.make_request(
            method="POST",
            url=f"/goods/control-list-entries/{case_id}/",
            headers=self.api_client.gov_headers,
            body={
                "control_list_entries": kwargs.get("control_list_entries", []),
                "is_precedent": kwargs.get("is_precedent", False),
                "is_good_controlled": kwargs.get("is_good_controlled", True),
                "end_use_control": kwargs.get("end_use_control", []),
                "report_summary": kwargs.get("report_summary", ""),
                "comment": kwargs.get("comment", ""),
                "current_object": good_on_application_id,
                "objects": [good_id],
            },
        )
