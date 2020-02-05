from .api_client import ApiClient


class Parties(ApiClient):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def add_end_user_document(self, draft_id):
        self.add_document(
            url="/applications/" + draft_id + "/end-user/document/",
            name="end user document",
            description="this is a test end user document",
        )

    def add_consignee_document(self, draft_id):
        self.add_document(
            url="/applications/" + draft_id + "/consignee/document/",
            name="consignee document",
            description="this is a test consignee document",
        )

    def add_ultimate_end_user_document(self, draft_id, ultimate_end_user_id):
        self.add_document(
            url="/applications/" + draft_id + "/ultimate-end-user/" + ultimate_end_user_id + "/document/",
            name="ultimate end user document",
            description="this is a test ultimate end user document",
        )

    def add_third_party_document(self, draft_id, third_party_id):
        self.add_document(
            url="/applications/" + draft_id + "/third-parties/" + third_party_id + "/document/",
            name="third party document",
            description="this is a test third party document",
        )

    def add_eua_query(self):
        data = self.request_data["end_user_advisory"]
        data = self.make_request(
            method="POST", url="/queries/end-user-advisories/", headers=ApiClient.exporter_headers, body=data,
        ).json()["end_user_advisory"]
        self.add_to_context("end_user_advisory_id", str(data["id"]))
        self.add_to_context("end_user_advisory_reference_code", str(data["reference_code"]))

    def add_end_user(self, draft_id, end_user=None):
        end_user_data = end_user or self.request_data["end-user"]
        end_user = self.make_request(
            method="POST",
            url="/applications/" + draft_id + "/end-user/",
            headers=ApiClient.exporter_headers,
            body=end_user_data,
        ).json()["end_user"]
        self.add_end_user_document(draft_id)
        self.add_to_context("end_user", end_user)

    def add_ultimate_end_user(self, draft_id, ultimate_end_user=None):
        ueu_data = ultimate_end_user or self.request_data["ultimate_end_user"]
        ultimate_end_user_post = self.make_request(
            method="POST",
            url="/applications/" + draft_id + "/ultimate-end-users/",
            headers=ApiClient.exporter_headers,
            body=ueu_data,
        )
        self.add_to_context("ultimate_end_user", ultimate_end_user_post.json()["ultimate_end_user"])
        ultimate_end_user_id = self.context["ultimate_end_user"]["id"]
        self.add_ultimate_end_user_document(draft_id, ultimate_end_user_id)
        return ultimate_end_user_id

    def add_consignee(self, draft_id, consignee=None):
        consignee_data = consignee or self.request_data["consignee"]
        consignee_response = self.make_request(
            method="POST",
            url="/applications/" + draft_id + "/consignee/",
            headers=ApiClient.exporter_headers,
            body=consignee_data,
        )
        self.add_to_context("consignee", consignee_response.json()["consignee"])
        self.add_consignee_document(draft_id)

    def add_third_party(self, draft_id, third_party=None):
        third_party_data = third_party or self.request_data["third_party"]
        third_party_response = self.make_request(
            method="POST",
            url="/applications/" + draft_id + "/third-parties/",
            headers=ApiClient.exporter_headers,
            body=third_party_data,
        )
        self.add_to_context("third_party", third_party_response.json()["third_party"])
        third_party_id = self.context["third_party"]["id"]
        self.add_third_party_document(draft_id, third_party_id)
        return third_party_id
