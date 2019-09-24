import json

import requests

from conf.settings import env
from helpers.wait import wait_for_ultimate_end_user_document, wait_for_document


class SeedData:
    base_url = ''
    exporter_user_email = env('TEST_EXPORTER_SSO_EMAIL')

    gov_headers = {'content-type': 'application/json'}
    export_headers = {'content-type': 'application/json'}
    context = {}
    org_name = 'Test Org'
    org_name_for_switching_organisations = 'Octopus Systems'
    logging = True
    case_note_text = 'I Am Easy to Find'
    ecju_query_text = 'This is a question, please answer'
    first_name = 'Test'
    last_name = 'Lite'
    good_end_product_true = 'Hot Cross Buns'
    good_end_product_false = 'Falafels'

    request_data = {
        'organisation': {
            'name': org_name,
            'eori_number': '1234567890AAA',
            'sic_number': '2345',
            'vat_number': 'GB1234567',
            'registration_number': '09876543',
            'user': {
                'first_name': first_name,
                'last_name': last_name,
                'email': exporter_user_email
            },
            'site': {
                'name': 'Headquarters',
                'address': {
                    'address_line_1': '42 Question Road',
                    'postcode': 'Islington',
                    'city': 'London',
                    'region': 'London',
                    'country': 'GB'
                }
            }
        },
        'organisation_for_switching_organisations': {
            'name': org_name_for_switching_organisations,
            'eori_number': '1234567890AAA',
            'sic_number': '2345',
            'vat_number': 'GB1234567',
            'registration_number': '09876543',
            'user': {
                'first_name': first_name,
                'last_name': last_name,
                'email': exporter_user_email
            },
            'site': {
                'name': 'Headquarters',
                'address': {
                    'address_line_1': '42 Question Road',
                    'postcode': 'Islington',
                    'city': 'London',
                    'region': 'London',
                    'country': 'GB'
                }
            }
        },
        'good': {
            'description': 'Lentils',
            'is_good_controlled': 'yes',
            'control_code': '1234',
            'is_good_end_product': True,
            'part_number': '1234',
            'validate_only': False,
        },
        'good_end_product_true': {
            'description': good_end_product_true,
            'is_good_controlled': 'yes',
            'control_code': '1234',
            'is_good_end_product': True,
            'part_number': '1234',
            'validate_only': False
        },
        'good_end_product_false': {
            'description': good_end_product_false,
            'is_good_controlled': 'yes',
            'control_code': '1234',
            'is_good_end_product': False,
            'part_number': '1234',
            'validate_only': False,
        },
        'gov_user': {
            'email': 'test-uat-user@digital.trade.gov.uk',
            'first_name': 'ecju',
            'last_name': 'user'},
        'export_user': {
            'email': exporter_user_email,
            'password': 'password'
        },
        'draft': {
            'name': 'application',
            'licence_type': 'standard_licence',
            'export_type': 'permanent',
            'have_you_been_informed': 'yes',
            'reference_number_on_information_form': '1234'
        },
        'end-user': {
            'name': 'Government',
            'address': 'Westminster, London SW1A 0AA',
            'country': 'Ukraine',
            'sub_type': 'government',
            'website': 'https://www.gov.uk'
        },
        'ultimate_end_user': {
            'name': 'Individual',
            'address': 'Bullring, Birmingham SW1A 0AA',
            'country': 'GB',
            'sub_type': 'commercial',
            'website': 'https://www.anothergov.uk'
        },
        'consignee': {
            'name': 'Government',
            'address': 'Westminster, London SW1A 0BB',
            'country': 'GB',
            'sub_type': 'government',
            'website': 'https://www.gov.uk'
        },
        'add_good': {
            'good_id': '',
            'quantity': 1234,
            'unit': 'NAR',
            'value': 123.45
        },
        'clc_good': {
            'description': 'Targus',
            'is_good_controlled': 'unsure',
            'control_code': '1234',
            'is_good_end_product': True,
            'part_number': '1234',
            'validate_only': False,
            'details': 'Kebabs'
        },
        'case_note': {
            'text': case_note_text,
            'is_visible_to_exporter': True
        },
        'ecju_query': {
            'question': ecju_query_text
        },
        'document': {
            'name': 'document 1',
            's3_key': env('TEST_S3_KEY'),
            'size': 0,
            'description': 'document for test setup'
        }
    }

    def __init__(self, api_url, logging=True):
        self.base_url = api_url.rstrip('/')
        self.auth_gov_user()
        self.setup_org()
        self.auth_export_user()
        self.add_good()
        self.logging = logging

    def log(self, text):
        if self.logging:
            print(text)

    def add_to_context(self, name, value):
        self.log(name + ': ' + value)
        self.context[name] = value

    def auth_gov_user(self):
        data = self.request_data['gov_user']
        response = self.make_request('POST', url='/gov-users/authenticate/', body=data)
        self.add_to_context('gov_user_token', json.loads(response.text)['token'])
        self.gov_headers['gov-user-token'] = self.context['gov_user_token']

    def auth_export_user(self):
        data = self.request_data['export_user']
        response = self.make_request('POST', url='/users/authenticate/', body=data)
        self.add_to_context('export_user_token', json.loads(response.text)['token'])
        self.export_headers['exporter-user-token'] = self.context['export_user_token']
        self.export_headers['organisation-id'] = self.context['org_id']

    def setup_org(self):
        organisation = self.find_org_by_name(self.org_name)
        if not organisation:
            organisation = self.add_org('organisation')
        org_id = organisation['id']
        self.add_to_context('org_id', org_id)
        self.add_to_context('first_name', self.first_name)
        self.add_to_context('last_name', self.last_name)
        self.add_to_context('primary_site_id', self.get_org_primary_site_id(org_id))
        self.add_to_context('org_name', self.org_name)

    def setup_org_for_switching_organisations(self):
        organisation = self.find_org_by_name(self.org_name_for_switching_organisations)
        if not organisation:
            self.add_org('organisation_for_switching_organisations')
        self.add_to_context('org_name_for_switching_organisations', self.org_name_for_switching_organisations)

    def add_good(self):
        self.log('Adding good: ...')
        data = self.request_data['good']
        response = self.make_request('POST', url='/goods/', headers=self.export_headers, body=data)
        item = json.loads(response.text)['good']
        self.add_to_context('good_id', item['id'])
        self.add_good_document(item['id'])

    def add_clc_good(self):
        self.log('Adding clc good: ...')
        data = self.request_data['clc_good']
        response = self.make_request('POST', url='/goods/', headers=self.export_headers, body=data)
        item = json.loads(response.text)['good']
        self.add_to_context('clc_good_id', item['id'])
        self.add_good_document(item['id'])
        data = {'good_id': self.context['clc_good_id'],
                'not_sure_details_control_code': 'a',
                'not_sure_details_details': 'b'}
        response = self.make_request('POST', url='/queries/control-list-classifications/', headers=self.export_headers, body=data)
        response_data = json.loads(response.text)
        self.add_ecju_query(response_data['case_id'])

    def find_good_by_name(self, good_name):
        response = self.make_request('GET', url='/goods/', headers=self.export_headers)
        goods = json.loads(response.text)['goods']
        good = next((item for item in goods if item['description'] == good_name), None)
        return good

    def add_good_end_product_false(self):
        self.log('Adding good: ...')
        good = self.find_good_by_name(self.good_end_product_false)
        if not good:
            data = self.request_data['good_end_product_false']
            response = self.make_request('POST', url='/goods/', headers=self.export_headers, body=data)
            item = json.loads(response.text)['good']
            self.add_good_document(item['id'])
        self.add_to_context('goods_name', self.good_end_product_false)

    def add_good_end_product_true(self):
        self.log('Adding good: ...')
        good = self.find_good_by_name(self.good_end_product_true)
        if not good:
            data = self.request_data['good_end_product_true']
            response = self.make_request('POST', url='/goods/', headers=self.export_headers, body=data)
            item = json.loads(response.text)['good']
            self.add_good_document(item['id'])
        self.add_to_context('goods_name', self.good_end_product_true)

    def add_org(self, key):
        self.log('Creating org: ...')
        data = self.request_data[key]
        response = self.make_request('POST', url='/organisations/', body=data)
        organisation = json.loads(response.text)['organisation']
        return organisation

    def add_case_note(self, context):
        self.log('Creating case note: ...')
        data = self.request_data['case_note']
        context.text = self.case_note_text
        _ = self.make_request("POST", url='/cases/' + context.case_id + '/case-notes/', headers=self.gov_headers, body=data) # noqa

    def add_ecju_query(self, case_id):
        self.log("Creating ecju query: ...")
        data = self.request_data['ecju_query']
        _ = self.make_request("POST", url='/cases/' + case_id + '/ecju-queries/', headers=self.gov_headers, body=data) # noqa

    def find_org_by_name(self, org_name):
        response = self.make_request('GET', url='/organisations/')
        organisations = json.loads(response.text)['organisations']
        organisation = next((item for item in organisations if item['name'] == org_name), None)
        return organisation

    def get_org_primary_site_id(self, org_id):
        response = self.make_request('GET', url='/organisations/' + org_id)
        organisation = json.loads(response.text)['organisation']
        return organisation['primary_site']['id']

    def add_good_document(self, good_id):
        data = [self.request_data['document']]
        self.make_request("POST", url='/goods/' + good_id + '/documents/', headers=self.export_headers, body=data)

    def add_document(self, url):
        data = self.request_data['document']
        self.make_request("POST", url=url, headers=self.export_headers, body=data)

    def add_end_user_document(self, draft_id):
        self.add_document('/drafts/' + draft_id + '/end-user/document/')

    def add_ultimate_end_user_document(self, draft_id, ultimate_end_user_id):
        self.add_document('/drafts/' + draft_id + '/ultimate-end-user/' + ultimate_end_user_id + '/document/')

    def add_consignee_document(self, draft_id):
        self.add_document('/drafts/' + draft_id + '/consignee/document/')

    def check_documents(self, draft_id, ultimate_end_user_id):
        end_user_document_is_processed = wait_for_document(
            func=self.check_end_user_document_is_processed, draft_id=draft_id)
        assert end_user_document_is_processed, "End user document wasn't successfully processed"
        consignee_document_is_processed = wait_for_document(
            func=self.check_consignee_document_is_processed, draft_id=draft_id)
        assert consignee_document_is_processed, "Consignee document wasn't successfully processed"
        ultimate_end_user_document_is_processed = wait_for_ultimate_end_user_document(
            func=self.check_ultimate_end_user_document_is_processed, draft_id=draft_id,
            ultimate_end_user_id=ultimate_end_user_id)
        assert ultimate_end_user_document_is_processed, "Ultimate end user document wasn't successfully processed"

    def add_draft(self, draft=None, good=None, enduser=None, ultimate_end_user=None, consignee=None):
        self.log('Creating draft: ...')
        data = self.request_data['draft'] if draft is None else draft
        response = self.make_request('POST', url='/drafts/', headers=self.export_headers, body=data)
        draft_id = json.loads(response.text)['draft']['id']
        self.add_to_context('draft_id', draft_id)
        self.log('Adding site: ...')
        self.make_request('POST', url='/drafts/' + draft_id + '/sites/', headers=self.export_headers,
                          body={'sites': [self.context['primary_site_id']]})
        self.log('Adding end user: ...')
        data = self.request_data['end-user'] if enduser is None else enduser
        self.make_request('POST', url='/drafts/' + draft_id + '/end-user/', headers=self.export_headers,
                          body=data)
        self.add_end_user_document(draft_id)
        self.log("Adding good: ...")
        data = self.request_data['add_good'] if good is None else good
        data['good_id'] = self.context['good_id']
        self.make_request('POST', url='/drafts/' + draft_id + '/goods/', headers=self.export_headers, body=data)
        self.log('Adding ultimate end user: ...')
        data = self.request_data['ultimate_end_user'] if ultimate_end_user is None else ultimate_end_user
        ultimate_end_user_post = self.make_request('POST', url='/drafts/' + draft_id + '/ultimate-end-users/',
                                              headers=self.export_headers, body=data)
        ultimate_end_user_id = json.loads(ultimate_end_user_post.text)['ultimate_end_user']['id']
        self.add_ultimate_end_user_document(draft_id, ultimate_end_user_id)
        consignee_data = self.request_data['consignee'] if consignee is None else consignee
        self.make_request('POST', url='/drafts/' + draft_id + '/consignee/', headers=self.export_headers,
                          body=consignee_data)
        self.add_consignee_document(draft_id)
        self.check_documents(draft_id=draft_id, ultimate_end_user_id=ultimate_end_user_id)

    def submit_application(self, draft_id=None):
        self.log('submitting application: ...')
        draft_id_to_submit = draft_id if None else self.context['draft_id']  # noqa
        data = {'id': draft_id_to_submit}
        response = self.make_request('POST', url='/applications/', headers=self.export_headers, body=data)
        item = json.loads(response.text)['application']
        self.add_to_context('application_id', item['id'])
        self.add_to_context('case_id', item['case_id'])

    def check_document(self, url):
        data = self.make_request("GET", url=url, headers=self.export_headers)
        return json.loads(data.text)['document']['safe']

    def check_end_user_document_is_processed(self, draft_id):
        return self.check_document('/drafts/' + draft_id + '/end-user/document/')

    def check_consignee_document_is_processed(self, draft_id):
        return self.check_document('/drafts/' + draft_id + '/consignee/document/')

    def check_ultimate_end_user_document_is_processed(self, draft_id, ultimate_end_user_id):
        return self.check_document('/drafts/' + draft_id + '/ultimate-end-user/' + ultimate_end_user_id + '/document/')

    def make_request(self, method, url, headers=None, body=None, files=None):
        if headers is None:
            headers = self.gov_headers
        if body:
            response = requests.request(method, self.base_url + url,
                                        data=json.dumps(body),
                                        headers=headers,
                                        files=files)
        else:
            response = requests.request(method, self.base_url + url, headers=headers)
        if not response.ok:
            raise Exception('bad response: ' + response.text)
        return response
