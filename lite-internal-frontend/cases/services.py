from cases.helpers import clean_advice
from conf.client import post, get, put, delete
from conf.constants import CASE_URL, CASE_NOTES_URL, APPLICATIONS_URL, ACTIVITY_URL, CLC_QUERIES_URL, DOCUMENTS_URL, \
    END_USER_ADVISORY_URL, CASE_FLAGS_URL, ECJU_QUERIES_URL, GOOD_URL, FLAGS_URL, ASSIGN_FLAGS_URL, \
    GOODS_TYPE_URL, USER_ADVICE_URL, TEAM_ADVICE_URL, FINAL_ADVICE_URL, VIEW_TEAM_ADVICE_URL, VIEW_FINAL_ADVICE_URL



def get_case(request, pk):
    data = get(request, CASE_URL + pk)
    return data.json()['case']


def put_case(request, pk, json):
    data = put(request, CASE_URL + pk, json)
    return data.json(), data.status_code


# Applications
def put_applications(request, pk, json):
    data = put(request, APPLICATIONS_URL + pk, json)
    return data.json(), data.status_code


# CLC Queries
def put_control_list_classification_query(request, pk, json):
    data = put(request, CLC_QUERIES_URL + pk, json)
    return data.json(), data.status_code


# EUA Queries
def put_end_user_advisory_query(request, pk, json):
    data = put(request, END_USER_ADVISORY_URL + str(pk), json)
    return data.json(), data.status_code


# Case Notes
def get_case_notes(request, pk):
    data = get(request, CASE_URL + pk + CASE_NOTES_URL)
    return data.json(), data.status_code


def post_case_notes(request, pk, json):
    data = post(request, CASE_URL + pk + CASE_NOTES_URL, json)
    return data.json(), data.status_code


# Case Flags
def put_case_flags(request, pk, flags):
    data = put(request, CASE_URL + pk + CASE_FLAGS_URL, flags)
    return data.json(), data.status_code


# Activity
def get_activity(request, pk):
    data = get(request, CASE_URL + pk + ACTIVITY_URL + '?fields=status,flags')
    return data.json()['activity']


# Case Documents
def get_case_document(request, pk, document_metadata_id):
    data = get(request, CASE_URL + pk + DOCUMENTS_URL + document_metadata_id)
    return data.json(), data.status_code


def get_case_documents(request, pk):
    data = get(request, CASE_URL + pk + DOCUMENTS_URL)
    return data.json(), data.status_code


def post_case_documents(request, pk, json):
    data = post(request, CASE_URL + pk + DOCUMENTS_URL, json)
    return data.json(), data.status_code


def delete_case_document(request, pk, s3_key):
    data = delete(request, CASE_URL + pk + DOCUMENTS_URL + s3_key)
    return data.json(), data.status_code


# Advice
def get_user_case_advice(request, case_pk):
    data = get(request, CASE_URL + case_pk + USER_ADVICE_URL)
    return data.json(), data.status_code


def get_team_case_advice(request, case_pk, team_pk):
    data = get(request, CASE_URL + case_pk + VIEW_TEAM_ADVICE_URL + team_pk)
    return data.json(), data.status_code


def coalesce_user_advice(request, case_pk):
    data = get(request, CASE_URL + case_pk + TEAM_ADVICE_URL)
    return data.json(), data.status_code


def clear_team_advice(request, case_pk):
    data = delete(request, CASE_URL + case_pk + TEAM_ADVICE_URL)
    return data.json(), data.status_code


def get_final_case_advice(request, case_pk):
    data = get(request, CASE_URL + case_pk + VIEW_FINAL_ADVICE_URL)
    return data.json(), data.status_code


def coalesce_team_advice(request, case_pk):
    data = get(request, CASE_URL + case_pk + FINAL_ADVICE_URL)
    return data.json(), data.status_code


def clear_final_advice(request, case_pk):
    data = delete(request, CASE_URL + case_pk + FINAL_ADVICE_URL)
    return data.json(), data.status_code


def return_non_empty(data):
    for item in data:
        if item:
            return item


def build_case_advice(key, value, base_data):
    data = base_data.copy()
    data[key] = value
    return data


def prepare_data_for_advice(json):
    json = clean_advice(json)

    # Split the json data into multiple
    base_data = {
        'type': json['type'],
        'text': json['advice'],
        'note': json['note']
    }

    if json.get('type') == 'refuse':
        base_data['denial_reasons'] = json['denial_reasons']

    if json.get('type') == 'proviso':
        base_data['proviso'] = json['proviso']

    new_data = []
    single_cases = ['end_user', 'consignee']
    multiple_cases = {'ultimate_end_users': 'ultimate_end_user', 'third_parties': 'third_party',
                      'countries': 'country', 'goods': 'good', 'goods_types': 'good_type'}

    for entity_name in single_cases:
        if json.get(entity_name):
            new_data.append(build_case_advice(entity_name, json.get(entity_name), base_data))

    for entity_name, entity_name_singular in multiple_cases.items():
        if json.get(entity_name):
            for entity in json.get(entity_name, []):
                new_data.append(build_case_advice(entity_name_singular, entity, base_data))

    return new_data


def post_user_case_advice(request, case_pk, json):
    new_data = prepare_data_for_advice(json)
    data = post(request, CASE_URL + case_pk + USER_ADVICE_URL, new_data)
    return data.json(), data.status_code


def post_team_case_advice(request, case_pk, json):
    new_data = prepare_data_for_advice(json)
    data = post(request, CASE_URL + case_pk + TEAM_ADVICE_URL, new_data)
    return data.json(), data.status_code


def post_final_case_advice(request, case_pk, json):
    new_data = prepare_data_for_advice(json)
    data = post(request, CASE_URL + case_pk + FINAL_ADVICE_URL, new_data)
    return data.json(), data.status_code


def get_document(request, pk):
    data = get(request, DOCUMENTS_URL + pk)
    return data.json(), data.status_code


# ECJU Queries
def get_ecju_queries(request, pk):
    data = get(request, CASE_URL + pk + ECJU_QUERIES_URL)
    return data.json(), data.status_code


def post_ecju_query(request, pk, json):
    data = post(request, CASE_URL + pk + ECJU_QUERIES_URL, json)
    return data.json(), data.status_code


def get_good(request, pk):
    data = get(request, GOOD_URL + pk)
    return data.json(), data.status_code


def get_goods_type(request, pk):
    data = get(request, GOODS_TYPE_URL + pk)
    return data.json(), data.status_code


# Good Flags
def get_flags_for_team_of_level(request, level):
    """

    :param request:
    :param level: 'cases', 'goods'
    :return:
    """
    data = get(request, FLAGS_URL + '?level=' + level + '&team=True')
    return data.json(), data.status_code


def put_flag_assignments(request, json):
    data = put(request, ASSIGN_FLAGS_URL, json)
    return data.json(), data.status_code
