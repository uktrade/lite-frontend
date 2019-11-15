from .seed_class import SeedClass
from ..manage_s3_documents import upload_test_document_to_aws
from ..make_requests import make_request
from ..request_data import create_document


class Party(SeedClass):
    def add_document(self, url):
        doc_s3_key = upload_test_document_to_aws(self.base_url)
        data = create_document("kebab", "tasty", doc_s3_key)
        make_request(
            "POST", base_url=self.base_url, url=url, headers=self.export_headers, body=data,
        )

    def add_end_user_document(self, draft_id):
        self.add_document("/applications/" + draft_id + "/end-user/document/")

    def add_ultimate_end_user_document(self, draft_id, ultimate_end_user_id):
        self.add_document("/applications/" + draft_id + "/ultimate-end-user/" + ultimate_end_user_id + "/document/")

    def add_third_party_document(self, draft_id, third_party_id):
        self.add_document("/applications/" + draft_id + "/third-parties/" + third_party_id + "/document/")

    def add_consignee_document(self, draft_id):
        self.add_document("/applications/" + draft_id + "/consignee/document/")

    def add_eua_query(self):
        self.log("Adding end user advisory: ...")
        data = self.request_data["end_user_advisory"]
        id = make_request(
            "POST", base_url=self.base_url, url="/queries/end-user-advisories/", headers=self.export_headers, body=data,
        ).json()["end_user_advisory"]["id"]
        self.add_to_context("end_user_advisory_id", str(id))
        case_id = make_request(
            "GET",
            base_url=self.base_url,
            url="/queries/end-user-advisories/" + str(id) + "/",
            headers=self.export_headers,
        ).json()["case_id"]
        self.add_to_context("end_user_advisory_case_id", case_id)

    def add_end_user(self, draft_id, enduser):
        self.log("Adding end user: ...")
        end_user_data = self.request_data["end-user"] if enduser is None else enduser
        end_user = make_request(
            "POST",
            base_url=self.base_url,
            url="/applications/" + draft_id + "/end-user/",
            headers=self.export_headers,
            body=end_user_data,
        ).json()["end_user"]
        self.log("Adding end user document: ...")
        self.add_end_user_document(draft_id)
        self.add_to_context("end_user", end_user)

    def add_ultimate_end_user(self, draft_id, ultimate_end_user):
        self.log("Adding ultimate end user: ...")
        ueu_data = self.request_data["ultimate_end_user"] if ultimate_end_user is None else ultimate_end_user
        ultimate_end_user_post = make_request(
            "POST",
            base_url=self.base_url,
            url="/applications/" + draft_id + "/ultimate-end-users/",
            headers=self.export_headers,
            body=ueu_data,
        )
        self.add_to_context("ultimate_end_user", ultimate_end_user_post.json()["ultimate_end_user"])
        ultimate_end_user_id = self.context["ultimate_end_user"]["id"]
        self.add_ultimate_end_user_document(draft_id, ultimate_end_user_id)
        return ultimate_end_user_id

    def add_consignee(self, draft_id, consignee):
        self.log("Adding consignee: ...")
        consignee_data = self.request_data["consignee"] if consignee is None else consignee
        consignee_response = make_request(
            "POST",
            base_url=self.base_url,
            url="/applications/" + draft_id + "/consignee/",
            headers=self.export_headers,
            body=consignee_data,
        )
        self.add_to_context("consignee", consignee_response.json()["consignee"])
        self.add_consignee_document(draft_id)

    def add_third_party(self, draft_id, third_party):
        third_party_data = self.request_data["third_party"] if third_party is None else third_party
        third_party_response = make_request(
            "POST",
            base_url=self.base_url,
            url="/applications/" + draft_id + "/third-parties/",
            headers=self.export_headers,
            body=third_party_data,
        )
        self.add_to_context("third_party", third_party_response.json()["third_party"])
        third_party_id = self.context["third_party"]["id"]
        self.add_third_party_document(draft_id, third_party_id)
        return third_party_id
