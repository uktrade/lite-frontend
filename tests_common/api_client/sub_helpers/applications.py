from ...tools.wait import wait_for_function


class Applications:
    def __init__(self, api_client, documents, parties, goods, request_data, **kwargs):
        super().__init__(**kwargs)
        self.api_client = api_client
        self.request_data = request_data
        self.parties = parties
        self.goods = goods
        self.documents = documents

    def create_draft(self, draft=None):
        data = draft or self.request_data["application"]
        response = self.api_client.make_request(
            method="POST", url="/applications/", headers=self.api_client.exporter_headers, body=data
        )
        draft_id = response.json()["id"]
        self.api_client.add_to_context("draft_id", draft_id)
        return draft_id

    def add_countries(self, draft_id):
        self.api_client.make_request(
            method="POST",
            url="/applications/" + draft_id + "/countries/",
            headers=self.api_client.exporter_headers,
            body={"countries": ["US"]},
        )
        self.api_client.add_to_context("country", {"code": "US", "name": "United States"})

    def add_additional_document(self, draft_id):
        url = "/applications/" + draft_id + "/documents/"
        additional_document_metadata = self.documents.add_document(
            url=url, name="additional document", description="this is a test additional document"
        )
        self.api_client.add_to_context("additional_document", additional_document_metadata)
        return self.api_client.context["additional_document"]["document"]["id"]

    def add_site(self, draft_id, is_hmrc=False):
        if is_hmrc:
            primary_site_id_key = "hmrc_primary_site_id"
        else:
            primary_site_id_key = "primary_site_id"
        self.api_client.make_request(
            method="POST",
            url="/applications/" + draft_id + "/sites/",
            headers=self.api_client.exporter_headers,
            body={"sites": [self.api_client.context[primary_site_id_key]]},
        )

    def add_f680_clearance_types(self, draft_id, types):
        self.api_client.make_request(
            method="PUT",
            url="/applications/" + draft_id + "/",
            headers=self.api_client.exporter_headers,
            body={"types": types},
        )

    def add_draft(
        self,
        draft=None,
        good=None,
        end_user=None,
        has_end_user=True,
        has_ultimate_end_user=True,
        ultimate_end_user=None,
        has_consignee=True,
        has_location=True,
        consignee=None,
        third_party=None,
        has_third_party=True,
        f680_clearance_types=None,
    ):
        draft_id = self.create_draft(draft=draft)
        if has_location:
            self.add_site(draft_id=draft_id)

        if draft["application_type"] != "exhc":
            self.goods.add_good_to_draft(draft_id=draft_id, good=good)
        else:
            self.goods.add_good_to_draft(draft_id=draft_id, good=self.request_data["add_exhibition_good"])
            self.add_site(draft_id=draft_id)

        parties = []

        if has_end_user:
            parties.append(self.parties.add_party(request_data_key="end_user", draft_id=draft_id, party=end_user))

        if has_third_party:
            parties.append(self.parties.add_party(request_data_key="third_party", draft_id=draft_id, party=third_party))

        if has_ultimate_end_user:
            parties.append(
                self.parties.add_party(request_data_key="ultimate_end_user", draft_id=draft_id, party=ultimate_end_user)
            )

        if has_consignee:
            parties.append(self.parties.add_party(request_data_key="consignee", draft_id=draft_id, party=consignee))

        if f680_clearance_types:
            self.add_f680_clearance_types(draft_id=draft_id, types=f680_clearance_types)

        additional_document_id = self.add_additional_document(draft_id=draft_id)

        self._assert_all_documents_are_processed(
            draft_id=draft_id, parties=parties, additional_document_id=additional_document_id,
        )

        return draft_id

    def add_hmrc_draft(self, draft=None, end_user=None):
        draft_id = self.create_draft(draft)
        self.add_site(draft_id, is_hmrc=True)
        end_user = self.parties.add_party(request_data_key="end_user", draft_id=draft_id, party=end_user)
        self.goods.add_open_draft_good(draft_id)
        additional_document_id = self.add_additional_document(draft_id=draft_id)
        self._assert_all_documents_are_processed(
            draft_id=draft_id, parties=[end_user], additional_document_id=additional_document_id,
        )

        return draft_id

    def add_open_draft(self, draft=None):
        draft_id = self.create_draft(draft)
        self.api_client.add_to_context("open_draft_id", draft_id)
        self.add_site(draft_id)
        self.add_countries(draft_id)
        self.goods.add_open_draft_good(draft_id)

        return draft_id

    def submit_application(self, draft_id=None):
        draft_id_to_submit = draft_id or self.api_client.context["draft_id"]
        response = self.api_client.make_request(
            method="PUT",
            url="/applications/" + draft_id_to_submit + "/submit/",
            headers=self.api_client.exporter_headers,
        )
        data = response.json()
        self.api_client.add_to_context("application_id", draft_id)
        self.api_client.add_to_context("case_id", draft_id)
        self.api_client.add_to_context("reference_code", data["application"]["reference_code"])
        return data

    def copy_application(self, draft_id, data):
        response = self.api_client.make_request(
            method="POST",
            url="/applications/" + draft_id + "/copy/",
            headers=self.api_client.exporter_headers,
            body=data,
        )
        return response.json()

    def add_copied_application(self, draft_id, data):
        response = self.copy_application(draft_id, data)
        self.submit_application(response["data"])
        self.api_client.add_to_context("application_id", response["data"])
        self.api_client.add_to_context("case_id", response["data"])

    def is_party_document_processed(self, draft_id, party_id):
        url = "/applications/" + draft_id + "/parties/" + party_id + "/document/"
        return self.is_document_processed(url)

    def is_additional_document_processed(self, draft_id, document_id):
        return self.is_document_processed("/applications/" + draft_id + "/documents/" + document_id + "/")

    def is_document_processed(self, url):
        response = self.api_client.make_request(method="GET", url=url, headers=self.api_client.exporter_headers)
        return response.json()["document"]["safe"]

    def _assert_all_documents_are_processed(self, draft_id, parties, additional_document_id):
        for party in parties:
            self._assert_document_is_processed(
                document_type=party["type"],
                callback_function=self.is_party_document_processed,
                draft_id=draft_id,
                party_id=party["id"],
            )

        self._assert_document_is_processed(
            document_type="Additional",
            callback_function=self.is_additional_document_processed,
            draft_id=draft_id,
            document_id=additional_document_id,
        )

    @staticmethod
    def _assert_document_is_processed(**kwargs):
        document_type = kwargs.pop("document_type")
        callback_function = kwargs.pop("callback_function")
        assert wait_for_function(callback_function, **kwargs), document_type + " document wasn't successfully processed"

    def post_exhibition_details(self, draft_id, data):
        data = data if data else self.request_data["exhibition_details"]
        self.api_client.make_request(
            method="POST",
            url="/applications/" + draft_id + "/exhibition-details/",
            headers=self.api_client.exporter_headers,
            body=data,
        )
