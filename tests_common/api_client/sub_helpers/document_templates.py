from ...tools import helpers


class DocumentTemplates:
    def __init__(self, api_client, request_data, **kwargs):
        super().__init__(**kwargs)
        self.api_client = api_client
        self.request_data = request_data

    def add_template(self, seed_picklist, advice_type=None):
        template_data = self.api_client.request_data["document_template"]
        template_data["layout"] = self.get_layouts()[0]["id"]
        paragraph = seed_picklist.add_letter_paragraph_picklist()
        template_data["letter_paragraphs"] = [paragraph["id"]]
        template_data["name"] = "0000" + helpers.get_formatted_date_time_m_d_h_s()
        template_data["visible_to_exporter"] = True
        if advice_type:
            template_data["decisions"] = advice_type
        template = self.api_client.make_request(
            method="POST", url="/letter-templates/", headers=self.api_client.gov_headers, body=template_data,
        ).json()
        template["paragraph"] = paragraph
        return template

    def get_paragraph(self, paragraph_id):
        return self.api_client.make_request(
            method="GET", url="/picklist/" + str(paragraph_id) + "/", headers=self.api_client.gov_headers,
        ).json()["picklist_item"]

    def get_layouts(self):
        return self.api_client.make_request(
            method="GET", url="/static/letter-layouts/", headers=self.api_client.gov_headers,
        ).json()["results"]
