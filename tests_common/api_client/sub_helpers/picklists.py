from ...api_client.api_client import ApiClient


class Picklists:
    def __init__(self, api_client, request_data, **kwargs):
        super().__init__(**kwargs)
        self.api_client = api_client
        self.request_data = request_data

    def post_picklist(self, key):
        return self.api_client.make_request(
            method="POST", url="/picklist/", body=self.request_data[key], headers=ApiClient.gov_headers,
        ).json()["picklist_item"]

    def add_ecju_query_picklist(self):
        return self.post_picklist("ecju_query_picklist")

    def add_proviso_picklist(self):
        return self.post_picklist("proviso_picklist")

    def add_standard_advice_picklist(self):
        return self.post_picklist("standard_advice_picklist")

    def add_report_summary_picklist(self):
        return self.post_picklist("report_picklist")

    def add_letter_paragraph_picklist(self):
        return self.post_picklist("letter_paragraph_picklist")
