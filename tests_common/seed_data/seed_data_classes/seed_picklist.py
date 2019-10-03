from shared.seed_data.seed_data_classes.seed_class import SeedClass
from shared.seed_data.make_requests import make_request


class SeedPicklist(SeedClass):
    def add_ecju_query_picklist(self):
        self.log("Creating ECJU Query picklist item ...")
        data = self.request_data['ecju_query_picklist']
        response = make_request("POST", base_url=self.base_url, url='/picklist/', body=data, headers=self.gov_headers)
        return response.json()['picklist_item']

    def add_proviso_picklist(self):
        self.log("Creating proviso picklist item ...")
        data = self.request_data['proviso_picklist']
        response = make_request("POST", base_url=self.base_url, url='/picklist/', body=data, headers=self.gov_headers)
        return response.json()['picklist_item']

    def add_standard_advice_picklist(self):
        self.log("Creating standard advice picklist item ...")
        data = self.request_data['standard_advice_picklist']
        response = make_request("POST", base_url=self.base_url, url='/picklist/', body=data, headers=self.gov_headers)
        return response.json()['picklist_item']

    def add_report_summary_picklist(self):
        self.log("Creating standard advice picklist item ...")
        data = self.request_data['report_picklist']
        response = make_request("POST", base_url=self.base_url, url='/picklist/', body=data, headers=self.gov_headers)
        return response.json()['picklist_item']
