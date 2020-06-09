class Parties:
    def __init__(self, api_client, documents, request_data, **kwargs):
        super().__init__(**kwargs)
        self.api_client = api_client
        self.documents = documents
        self.request_data = request_data

    def add_eua_query(self):
        data = self.request_data["end_user_advisory"]
        data = self.api_client.make_request(
            method="POST", url="/queries/end-user-advisories/", headers=self.api_client.exporter_headers, body=data,
        ).json()["end_user_advisory"]
        self.api_client.add_to_context("end_user_advisory_id", str(data["id"]))
        self.api_client.add_to_context("end_user_advisory_reference_code", str(data["reference_code"]))

    def add_party(self, draft_id, request_data_key, party=None):
        party_data = party or self.request_data[request_data_key if request_data_key != "end_user" else "end-user"]
        party = self.api_client.make_request(
            method="POST",
            url=f"/applications/{draft_id}/parties/",
            headers=self.api_client.exporter_headers,
            body=party_data,
        ).json()[party_data["type"]]
        self.add_party_document(draft_id, party["id"])
        self.api_client.add_to_context(request_data_key, party)
        return party

    def delete_party(self, draft_id, party):
        party = self.api_client.make_request(
            "DELETE", url=f"/applications/{draft_id}/parties/{party['id']}/", headers=self.api_client.exporter_headers,
        ).json()["party"]

        self.api_client.add_to_context("inactive_party", party)

    def add_party_document(self, draft_id, party_id):
        self.documents.add_document(
            url=f"/applications/{draft_id}/parties/{party_id}/document/",
            name="Party document",
            description="Test party document",
        )

    def add_additional_contact(self, draft_id, data):
        return self.api_client.make_request(
            method="POST",
            url=f"/cases/{draft_id}/additional-contacts/",
            headers=self.api_client.gov_headers,
            body=data,
        ).json()
