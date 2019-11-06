import uuid

from seed_data.helper_classes import seed_class
from seed_data import make_requests


class SeedDocumentTemplate(seed_class.SeedClass):
    def add_template(self, seed_picklist):
        template_data = self.request_data['document_template']
        template_data['layout'] = self.get_layouts()[0]['id']
        paragraph = seed_picklist.add_letter_paragraph_picklist()
        template_data['letter_paragraphs'] = [paragraph['id']]
        template_data['name'] = str(uuid.uuid4())[:35]
        template = make_requests.make_request('POST', base_url=self.base_url, url='/letter-templates/',
                                              headers=self.gov_headers, body=template_data).json()
        template['paragraph'] = paragraph
        return template

    def get_paragraph(self, paragraph_id):
        return make_requests.make_request('GET', base_url=self.base_url,
                                          url='/picklist/' + str(paragraph_id) + '/',
                                          headers=self.gov_headers).json()['picklist_item']

    def get_layouts(self):
        return make_requests.make_request('GET', base_url=self.base_url, url='/static/letter-layouts/',
                                          headers=self.gov_headers).json()['results']
