from shared.tools.wait import wait_for_ultimate_end_user_document, wait_for_third_party_document, wait_for_additional_document, wait_for_document
from shared.seed_data.request_data import create_request_data
from shared.seed_data.make_requests import make_request
from shared.seed_data.seed_data_classes.seed_good import SeedGood
from shared.seed_data.seed_data_classes.seed_user import SeedUser
from shared.seed_data.seed_data_classes.seed_organisation import SeedOrganisation
from shared.seed_data.seed_data_classes.seed_clc import SeedClc
from shared.seed_data.seed_data_classes.seed_party import SeedParty


class SeedData:
    base_url = ''
    gov_headers = {'content-type': 'application/json'}
    export_headers = {'content-type': 'application/json'}
    context = {}
    logging = True
    org_name = "Test Org"

    def __init__(self, seed_data_config):
        exporter_user = seed_data_config['exporter']
        gov_user = seed_data_config['gov']
        test_s3_key = seed_data_config['s3_key']
        self.base_url = seed_data_config['api_url'].rstrip('/')
        self.request_data = create_request_data(
            exporter_user=exporter_user,
            test_s3_key=test_s3_key,
            gov_user=gov_user
        )
        self.seed_user = SeedUser(self.base_url, self.gov_headers, self.export_headers, self.request_data, self.context)
        self.seed_user.auth_gov_user()
        self.seed_org = SeedOrganisation(self.base_url, self.gov_headers, self.export_headers, self.request_data,
                                         self.context)
        self.seed_org.setup_org()
        self.seed_user.auth_export_user()

        self.seed_good = SeedGood(self.base_url, self.gov_headers, self.export_headers, self.request_data, self.context)
        self.seed_good.add_good()

        self.seed_clc = SeedClc(self.base_url, self.gov_headers, self.export_headers, self.request_data, self.context)
        self.seed_party = SeedParty(self.base_url, self.gov_headers, self.export_headers, self.request_data, self.context)

    def log(self, text):
        print(text)

    def add_to_context(self, name, value):
        self.log(name + ': ' + str(value))
        self.context[name] = value

    def setup_org_for_switching_organisations(self):
        self.seed_org.setup_org_for_switching_organisations()

    def add_clc_query(self):
        self.seed_clc.add_clc_query(self.seed_good)

    def add_eua_query(self):
        self.log("Adding end user advisory: ...")
        data = self.request_data['end_user_advisory']
        response = make_request("POST", base_url=self.base_url, url='/queries/end-user-advisories/', headers=self.export_headers, body=data)
        id = response.json()['end_user_advisory']['id']
        self.add_to_context('end_user_advisory_id', str(id))
        response = make_request("GET", base_url=self.base_url, url='/queries/end-user-advisories/' + str(id) + '/', headers=self.export_headers)
        self.add_to_context('end_user_advisory_case_id', response.json()['case_id'])

    def find_good_by_name(self, good_name):
        response = make_request('GET', base_url=self.base_url, url='/goods/', headers=self.export_headers)
        goods = response.json()['goods']
        good = next((item for item in goods if item['description'] == good_name), None)
        return good

    def add_case_note(self, context, case_id):
        self.log('Creating case note: ...')
        data = self.request_data['case_note']
        context.case_note_text = self.request_data['case_note']['text']
        make_request("POST", base_url=self.base_url, url='/cases/' + case_id + '/case-notes/', headers=self.gov_headers, body=data)  # noqa

    def add_ecju_query(self, case_id):
        self.log("Creating ecju query: ...")
        data = self.request_data['ecju_query']
        make_request("POST", base_url=self.base_url, url='/cases/' + case_id + '/ecju-queries/', headers=self.gov_headers, body=data)  # noqa

    def check_documents(self, draft_id, ultimate_end_user_id, third_party_id, additional_document_id):
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
        third_party_document_is_processed = wait_for_third_party_document(
            func=self.check_third_party_document_is_processed, draft_id=draft_id,
            third_party_id=third_party_id)
        assert third_party_document_is_processed, "Third party document wasn't successfully processed"
        additional_document_is_processed = wait_for_additional_document(
            func=self.check_additional_document_is_processed, draft_id=draft_id,
            document_id=additional_document_id)
        assert additional_document_is_processed, "Additional document wasn't successfully processed"

    def add_draft(self, draft=None, good=None, enduser=None, ultimate_end_user=None, consignee=None, third_party=None,
                  additional_documents=None):
        self.log("Creating draft: ...")
        data = self.request_data['draft'] if draft is None else draft
        response = make_request("POST", base_url=self.base_url, url='/drafts/', headers=self.export_headers, body=data)
        draft_id = response.json()['draft']['id']
        self.add_to_context('draft_id', draft_id)
        self.log("Adding site: ...")
        make_request("POST", base_url=self.base_url, url='/drafts/' + draft_id + '/sites/', headers=self.export_headers,
                          body={'sites': [self.context['primary_site_id']]})
        self.log("Adding end user: ...")
        end_user_data = self.request_data['end-user'] if enduser is None else enduser
        end_user_post = make_request("POST", base_url=self.base_url, url='/drafts/' + draft_id + '/end-user/', headers=self.export_headers,
                          body=end_user_data)
        self.log("Adding end user document: ...")
        self.seed_party.add_end_user_document(draft_id)
        self.add_to_context('end_user', end_user_post.json()['end_user'])
        self.log("Adding good: ...")
        data = self.request_data['add_good'] if good is None else good
        data['good_id'] = self.context['good_id']
        make_request("POST", base_url=self.base_url, url='/drafts/' + draft_id + '/goods/', headers=self.export_headers, body=data)
        self.log("Adding ultimate end user: ...")
        ueu_data = self.request_data['ultimate_end_user'] if ultimate_end_user is None else ultimate_end_user
        ultimate_end_user_post = make_request('POST', base_url=self.base_url, url='/drafts/' + draft_id + '/ultimate-end-users/',
                                                   headers=self.export_headers, body=ueu_data)
        self.add_to_context('ultimate_end_user', ultimate_end_user_post.json()['ultimate_end_user'])
        ultimate_end_user_id = self.context['ultimate_end_user']['id']
        self.seed_party.add_ultimate_end_user_document(draft_id, ultimate_end_user_id)

        consignee_data = self.request_data['consignee'] if consignee is None else consignee
        consignee_response = make_request('POST', base_url=self.base_url, url='/drafts/' + draft_id + '/consignee/',
                                               headers=self.export_headers, body=consignee_data)
        self.add_to_context('consignee', consignee_response.json()['consignee'])
        self.seed_party.add_consignee_document(draft_id)

        third_party_data = self.request_data['third_party'] if third_party is None else third_party
        third_party_response = make_request('POST', base_url=self.base_url, url='/drafts/' + draft_id + '/third-parties/',
                                                 headers=self.export_headers, body=third_party_data)
        self.add_to_context('third_party', third_party_response.json()['third_party'])
        third_party_id = self.context['third_party']['id']
        self.seed_party.add_third_party_document(draft_id, third_party_id)

        additional_documents_data = \
            self.request_data['additional_document'] if additional_documents is None else additional_documents
        additional_documents_response = make_request('POST', base_url=self.base_url, url='/drafts/' + draft_id + '/documents/',
                                                          headers=self.export_headers, body=additional_documents_data)
        self.add_to_context('additional_document',
                            additional_documents_response.json()['document'])
        additional_document_id = self.context['additional_document']['id']

        self.check_documents(draft_id=draft_id, ultimate_end_user_id=ultimate_end_user_id, third_party_id=third_party_id,
                             additional_document_id=additional_document_id)

    def add_open_draft(self, draft=None):
        self.log("Creating draft: ...")
        data = self.request_data['draft'] if draft is None else draft
        response = make_request("POST", base_url=self.base_url, url='/drafts/', headers=self.export_headers, body=data)
        draft_id = response.json()['draft']['id']
        self.add_to_context('draft_id', draft_id)
        self.log("Adding site: ...")
        make_request("POST", base_url=self.base_url, url='/drafts/' + draft_id + '/sites/', headers=self.export_headers,
                          body={'sites': [self.context['primary_site_id']]})
        self.log("Adding countries: ...")
        make_request("POST", base_url=self.base_url, url='/drafts/' + draft_id + '/countries/', headers=self.export_headers,
                          body={'countries': ['US', 'AL', 'ZM']})
        self.log("Adding goods_type: ...")
        data = {
            'description': 'A goods type',
            'is_good_controlled': True,
            'control_code': 'ML1a',
            'is_good_end_product': True,
            'content_type': 'draft',
            'object_id': draft_id
        }
        make_request("POST", base_url=self.base_url, url='/goodstype/', headers=self.export_headers, body=data)

    def submit_application(self, draft_id=None):
        self.log('submitting application: ...')
        draft_id_to_submit = draft_id if None else self.context['draft_id']  # noqa
        data = {'id': draft_id_to_submit}
        response = make_request('POST', base_url=self.base_url, url='/applications/', headers=self.export_headers, body=data)
        item = response.json()['application']
        self.add_to_context('application_id', item['id'])
        self.add_to_context('case_id', item['case_id'])

    def submit_open_application(self, draft_id=None):
        self.log("submitting application: ...")
        draft_id_to_submit = draft_id if None else self.context['draft_id']  # noqa
        data = {'id': draft_id_to_submit}
        response = make_request("POST", base_url=self.base_url, url='/applications/', headers=self.export_headers, body=data)
        item = response.json()['application']
        self.add_to_context('open_application_id', item['id'])
        self.add_to_context('open_case_id', item['case_id'])

    def add_queue(self, queue_name):
        self.log("adding queue: ...")
        self.context['queue_name'] = queue_name
        data = {'team': '00000000-0000-0000-0000-000000000001',
                'name': queue_name
                }
        response = make_request("POST", base_url=self.base_url, url='/queues/', headers=self.gov_headers, body=data)
        item = response.json()['queue']
        self.add_to_context('queue_id', item['id'])

    def get_queues(self):
        self.log("getting queues: ...")
        response = make_request("GET", base_url=self.base_url, url='/queues/', headers=self.gov_headers)
        queues = response.json()['queues']
        return queues

    def assign_case_to_queue(self, case_id=None, queue_id=None):
        self.log("assigning case to queue: ...")
        queue_id = self.context['queue_id'] if queue_id is None else queue_id
        case_id = self.context['case_id'] if case_id is None else case_id
        data = {'queues': [queue_id]}
        make_request("PUT", base_url=self.base_url, url='/cases/' + case_id + '/', headers=self.gov_headers, body=data)

    def assign_test_cases_to_bin(self, bin_queue_id, new_cases_queue_id):
        self.log("assigning cases to bin: ...")
        response = make_request("GET", base_url=self.base_url, url='/queues/' + new_cases_queue_id + '/', headers=self.gov_headers)
        queue = response.json()['queue']
        cases = queue['cases']
        for case in cases:
            data = {'queues': [bin_queue_id]}
            make_request("PUT", base_url=self.base_url, url='/cases/' + case['id'] + '/', headers=self.gov_headers, body=data)

    def add_ecju_response(self, question, response):
        self.log("adding response to ecju: ...")
        case_id = self.context['case_id']
        ecju_queries = make_request("GET", base_url=self.base_url, url='/cases/' + case_id + '/ecju-queries/', headers=self.gov_headers)
        ecju_query_id = None
        for ecju_query in ecju_queries.json()['ecju_queries']:
            if ecju_query['question'] == question:
                ecju_query_id = ecju_query['id']
                break
        data = {'response': response}
        make_request("PUT", base_url=self.base_url, url='/cases/' + case_id + '/ecju-queries/' + ecju_query_id + '/',
                          headers=self.export_headers, body=data)

    def check_document(self, url):
        response = make_request("GET", base_url=self.base_url, url=url, headers=self.export_headers)
        return response.json()['document']['safe']

    def check_end_user_document_is_processed(self, draft_id):
        return self.check_document('/drafts/' + draft_id + '/end-user/document/')

    def check_consignee_document_is_processed(self, draft_id):
        return self.check_document('/drafts/' + draft_id + '/consignee/document/')

    def check_ultimate_end_user_document_is_processed(self, draft_id, ultimate_end_user_id):
        return self.check_document('/drafts/' + draft_id + '/ultimate-end-user/' + ultimate_end_user_id + '/document/')

    def check_third_party_document_is_processed(self, draft_id, third_party_id):
        return self.check_document('/drafts/' + draft_id + '/third-parties/' + third_party_id + '/document/')

    def check_additional_document_is_processed(self, draft_id, document_id):
        return self.check_document('/drafts/' + draft_id + '/documents/' + document_id + '/')

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
