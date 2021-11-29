class Documents:
    def __init__(self, api_client, request_data, **kwargs):
        super().__init__(**kwargs)
        self.api_client = api_client
        self.request_data = request_data

    def add_document(self, url, name, description, is_content_english=None, includes_company_letterhead=None, multi_upload_endpoint=False):
        document_s3_key = self._get_or_create_test_document()
        document_data = {
            "name": name,
            "description": description,
            "s3_key": document_s3_key,
        }

        if is_content_english != None:
            document_data["is_content_english"] = is_content_english
        if includes_company_letterhead != None:
            document_data["includes_company_letterhead"] = includes_company_letterhead

        if multi_upload_endpoint:
            document_data = [document_data]
        response = self.api_client.make_request(
            method="POST", url=url, headers=self.api_client.exporter_headers, body=document_data
        ).json()

        return response

    def _get_or_create_test_document(self):
        response = self.api_client.make_request(
            method="GET", url="/static/upload-document-for-tests/", headers=self.api_client.exporter_headers
        )

        if response.status_code == 200:
            return response.json()["s3_key"]
        else:
            raise Exception(response.json()["errors"])
