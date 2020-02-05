from ...tools import helpers
from .api_client import ApiClient


class DocumentTemplates(ApiClient):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def add_template(self, seed_picklist):
        template_data = self.request_data["document_template"]
        template_data["layout"] = self.get_layouts()[0]["id"]
        paragraph = seed_picklist.add_letter_paragraph_picklist()
        template_data["letter_paragraphs"] = [paragraph["id"]]
        template_data["name"] = "0000" + helpers.get_formatted_date_time_m_d_h_s()
        template = self.make_request(
            method="POST", url="/letter-templates/", headers=ApiClient.gov_headers, body=template_data,
        ).json()
        template["paragraph"] = paragraph
        return template

    def get_paragraph(self, paragraph_id):
        return self.make_request(
            method="GET", url="/picklist/" + str(paragraph_id) + "/", headers=ApiClient.gov_headers,
        ).json()["picklist_item"]

    def get_layouts(self):
        return self.make_request(method="GET", url="/static/letter-layouts/", headers=ApiClient.gov_headers,).json()[
            "results"
        ]
