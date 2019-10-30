import uuid

from ...seed_data.make_requests import make_request
from ...seed_data.seed_data_classes.seed_class import SeedClass


class SeedDocumentTemplate(SeedClass):
    def add_template(self, seed_picklist):
        template_data = self.request_data['document_template']
        paragraph = seed_picklist.add_letter_paragraph_picklist()
        template_data['letter_paragraphs'] = [paragraph['id']]
        template_data['name'] = str(uuid.uuid4())[:35]
        template = make_request('POST', base_url=self.base_url, url='/letter-templates/',
                                headers=self.gov_headers, body=template_data).json()
        template['paragraph'] = paragraph
        return template

    def get_paragraph(self, paragraph_id):
        return make_request('GET', base_url=self.base_url,
                            url='/picklist/' + str(paragraph_id) + '/',
                            headers=self.gov_headers).json()['picklist_item']
