import requests
from tools.wait import wait_for_ultimate_end_user_document, wait_for_document
from request_data import create_request_data, first_name, last_name


class SeedData:
    base_url = ''
    context = {}
    gov_headers = {'content-type': 'application/json'}
    export_headers = {'content-type': 'application/json'}

    def __init__(self, seed_data_config):
        exporter_user_email = seed_data_config['email']
        test_s3_key = seed_data_config['s3_key']
        self.base_url = seed_data_config['api_url'].rstrip('/')
        self.auth_gov_user()
        self.setup_org()
        self.auth_export_user()
        self.add_good()
        self.request_data = create_request_data(exporter_user_email, test_s3_key)

    def log(self, text):
        print(text)

    def add_to_context(self, name, value):
        self.log(name + ': ' + value)
        self.context[name] = value

    def auth_gov_user(self):
        data = self.request_data['gov_user']
        response = self.make_request('POST', url='/gov-users/authenticate/', body=data)
        self.add_to_context('gov_user_token', response.json()['token'])
        self.gov_headers['gov-user-token'] = self.context['gov_user_token']

    def auth_export_user(self):
        data = self.request_data['export_user']
        response = self.make_request('POST', url='/users/authenticate/', body=data)
        self.add_to_context('export_user_token', response.json()['token'])
        self.export_headers['exporter-user-token'] = self.context['export_user_token']
        self.export_headers['organisation-id'] = self.context['org_id']

    def setup_org(self):
        organisation = self.find_org_by_name(self.request_data['organisation']['name'])
        if not organisation:
            organisation = self.add_org('organisation')
        org_id = organisation['id']
        self.add_to_context('org_id', org_id)
        self.add_to_context('first_name', first_name)
        self.add_to_context('last_name', last_name)
        self.add_to_context('primary_site_id', self.get_org_primary_site_id(org_id))
        self.add_to_context('org_name', self.request_data['organisation']['name'])

    def setup_org_for_switching_organisations(self):
        organisation = self.find_org_by_name(self.request_data['organisation_for_switching_organisations']['name'])
        if not organisation:
            self.add_org('organisation_for_switching_organisations')
        self.add_to_context('org_name_for_switching_organisations', self.request_data['organisation_for_switching_organisations']['name'])

    def add_good(self):
        self.log('Adding good: ...')
        data = self.request_data['good']
        response = self.make_request('POST', url='/goods/', headers=self.export_headers, body=data)
        item = response.json()['good']
        self.add_to_context('good_id', item['id'])
        self.add_good_document(item['id'])

    def add_clc_good(self):
        self.log('Adding clc good: ...')
        data = self.request_data['clc_good']
        response = self.make_request('POST', url='/goods/', headers=self.export_headers, body=data)
        item = response.json()['good']
        self.add_to_context('clc_good_id', item['id'])
        self.add_good_document(item['id'])
        data = {'good_id': self.context['clc_good_id'],
                'not_sure_details_control_code': 'ML1a',
                'not_sure_details_details': 'b'}
        response = self.make_request('POST', url='/queries/control-list-classifications/', headers=self.export_headers,
                                     body=data)
        response_data = response.json()
        self.add_ecju_query(response_data['case_id'])

    def add_eua_query(self):
        self.log("Adding end user advisory: ...")
        data = self.request_data['end_user_advisory']
        response = self.make_request("POST", url='/queries/end-user-advisories/', headers=self.export_headers, body=data)
        id = response.json()['end_user_advisory']['id']
        self.add_to_context('end_user_advisory_id', str(id))
        response = self.make_request("GET", url='/queries/end-user-advisories/' + str(id) + '/', headers=self.export_headers)
        self.add_to_context('end_user_advisory_case_id', response.json()['case_id'])

    def find_good_by_name(self, good_name):
        response = self.make_request('GET', url='/goods/', headers=self.export_headers)
        goods = response.json()['goods']
        good = next((item for item in goods if item['description'] == good_name), None)
        return good

    def add_good_end_product_false(self):
        self.log('Adding good: ...')
        good = self.find_good_by_name(self.request_data['good_end_product_false']['description'])
        if not good:
            data = self.request_data['good_end_product_false']
            response = self.make_request('POST', url='/goods/', headers=self.export_headers, body=data)
            item = response.json()['good']
            self.add_good_document(item['id'])
        self.add_to_context('goods_name', self.request_data['good_end_product_false']['description'])

    def add_good_end_product_true(self):
        self.log('Adding good: ...')
        good = self.find_good_by_name(self.request_data['good_end_product_true']['description'])
        if not good:
            data = self.request_data['good_end_product_true']
            response = self.make_request('POST', url='/goods/', headers=self.export_headers, body=data)
            item = response.json()['good']
            self.add_good_document(item['id'])
        self.add_to_context('goods_name', self.request_data['good_end_product_true']['description'])

    def add_org(self, key):
        self.log('Creating org: ...')
        data = self.request_data[key]
        response = self.make_request('POST', url='/organisations/', body=data)
        organisation = response.json()['organisation']
        return organisation

    def add_case_note(self, context, case_id):
        self.log('Creating case note: ...')
        data = self.request_data['case_note']
        context.text = self.request_data['case_note']['text']
        self.make_request("POST", url='/cases/' + case_id + '/case-notes/', headers=self.gov_headers, body=data)  # noqa

    def add_ecju_query(self, case_id):
        self.log("Creating ecju query: ...")
        data = self.request_data['ecju_query']
        self.make_request("POST", url='/cases/' + case_id + '/ecju-queries/', headers=self.gov_headers, body=data)  # noqa

    def find_org_by_name(self, org_name):
        response = self.make_request('GET', url='/organisations/')
        organisations = response.json()['organisations']
        organisation = next((item for item in organisations if item['name'] == org_name), None)
        return organisation

    def get_org_primary_site_id(self, org_id):
        response = self.make_request('GET', url='/organisations/' + org_id)
        organisation = response.json()['organisation']
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
        draft_id = response.json()['draft']['id']
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
        ultimate_end_user_id = ultimate_end_user_post.json()['ultimate_end_user']['id']
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
        item = response.json()['application']
        self.add_to_context('application_id', item['id'])
        self.add_to_context('case_id', item['case_id'])

    def check_document(self, url):
        response = self.make_request("GET", url=url, headers=self.export_headers)
        return response.json()['document']['safe']

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
                                        json=body,
                                        headers=headers,
                                        files=files)
        else:
            response = requests.request(method, self.base_url + url, headers=headers)
        if not response.ok:
            raise Exception('bad response: ' + response.text)
        return response
