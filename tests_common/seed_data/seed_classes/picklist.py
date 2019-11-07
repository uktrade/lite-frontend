from .seed_class import SeedClass
from ..make_requests import make_request


class Picklist(SeedClass):
    def post_picklist(self, key):
        return make_request("POST", base_url=self.base_url, url='/picklist/', body=self.request_data[key],
                            headers=self.gov_headers).json()['picklist_item']

    def add_ecju_query_picklist(self):
        self.log("Creating ECJU Query picklist item ...")
        return self.post_picklist('ecju_query_picklist')

    def add_proviso_picklist(self):
        self.log("Creating proviso picklist item ...")
        return self.post_picklist('proviso_picklist')

    def add_standard_advice_picklist(self):
        self.log("Creating standard advice picklist item ...")
        return self.post_picklist('standard_advice_picklist')

    def add_report_summary_picklist(self):
        self.log("Creating standard advice picklist item ...")
        return self.post_picklist('report_picklist')

    def add_letter_paragraph_picklist(self):
        self.log("Creating standard advice picklist item ...")
        return self.post_picklist('letter_paragraph_picklist')
