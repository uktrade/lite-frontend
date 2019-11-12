from http import HTTPStatus

from conf.client import get, post, put, delete
from conf.constants import APPLICATIONS_URL, END_USER_DOCUMENT_URL, ULTIMATE_END_USER_URL, DOCUMENT_URL, \
    CONSIGNEE_URL, THIRD_PARTIES_URL, CONSIGNEE_DOCUMENT_URL, APPLICATION_SUBMIT_URL, ADDITIONAL_DOCUMENT_URL, \
    CASES_URL, CASE_NOTES_URL, ECJU_QUERIES_URL, MANAGE_STATUS_URL
from conf.settings import AWS_STORAGE_BUCKET_NAME, STREAMING_CHUNK_SIZE
from django.http import StreamingHttpResponse
from s3chunkuploader.file_handler import s3_client

from core.helpers import remove_prefix


def get_draft_applications(request):
    data = get(request, APPLICATIONS_URL + '?submitted=false')
    return data.json().get('applications') if data.status_code == HTTPStatus.OK else None


def get_applications(request):
    data = get(request, APPLICATIONS_URL + '?submitted=true')
    return data.json().get('applications') if data.status_code == HTTPStatus.OK else None


def get_application(request, pk):
    data = get(request, APPLICATIONS_URL + pk)
    return data.json().get('application') if data.status_code == HTTPStatus.OK else None


def post_application(request, json):
    data = post(request, APPLICATIONS_URL, json)
    return data.json(), data.status_code


def put_application(request, pk, json):
    data = put(request, APPLICATIONS_URL + pk + '/', json)
    return data.json(), data.status_code


def delete_application(request, pk):
    data = delete(request, APPLICATIONS_URL + pk)
    return data.json(), data.status_code


def submit_application(request, pk):
    data = put(request, APPLICATIONS_URL + pk + APPLICATION_SUBMIT_URL, json={})
    return data.json(), data.status_code


# Goods
def get_application_goods(request, pk):
    data = get(request, APPLICATIONS_URL + pk + '/goods/')
    return data.json().get('goods') if data.status_code == HTTPStatus.OK else None


def validate_application_good(request, pk, json):
    post_data = get_data_from_post_good_on_app(json)
    post_data['validate_only'] = True
    return post(request, APPLICATIONS_URL + pk + '/goods/', post_data)


def get_application_goods_types(request, pk):
    data = get(request, APPLICATIONS_URL + pk + '/goodstypes/')
    return data.json().get('goods') if data.status_code == HTTPStatus.OK else None


def post_good_on_application(request, pk, json):
    post_data = get_data_from_post_good_on_app(json)
    if 'good_id' not in post_data:
        post_data['good_id'] = json['good_id']
    data = post(request, APPLICATIONS_URL + pk + '/goods/', post_data)
    return data.json(), data.status_code


def get_data_from_post_good_on_app(json):
    if json.get('good_on_app_value') or json.get('good_on_app_value') == "":
        post_data = remove_prefix(json, 'good_on_app_')
    else:
        post_data = json
    return post_data


# Countries
def get_application_countries(request, pk):
    data = get(request, APPLICATIONS_URL + pk + '/countries/')
    return data.json()['countries']


def post_application_countries(request, pk, json):
    data = post(request, APPLICATIONS_URL + pk + '/countries/', json)
    return data.json(), data.status_code


# End User
def post_end_user(request, pk, json):
    data = post(request, APPLICATIONS_URL + pk + '/end-user/', json)
    return data.json(), data.status_code


# End user Documents
def get_end_user_document(request, pk):
    data = get(request, APPLICATIONS_URL + pk + END_USER_DOCUMENT_URL)
    return data.json(), data.status_code


def post_end_user_document(request, pk, json):
    data = post(request, APPLICATIONS_URL + pk + END_USER_DOCUMENT_URL, json)
    return data.json(), data.status_code


def delete_end_user(request, pk):
    data = delete(request, APPLICATIONS_URL + pk + '/end-user/')
    return data.status_code


def delete_end_user_document(request, pk):
    data = delete(request, APPLICATIONS_URL + pk + END_USER_DOCUMENT_URL)
    return data.status_code


# Ultimate End Users
def get_ultimate_end_users(request, pk):
    data = get(request, APPLICATIONS_URL + pk + '/ultimate-end-users/')
    return data.json()['ultimate_end_users']


def post_ultimate_end_user(request, pk, json):
    data = post(request, APPLICATIONS_URL + pk + '/ultimate-end-users/', json)
    return data.json(), data.status_code


def delete_ultimate_end_user(request, pk, ueu_pk):
    data = delete(request, APPLICATIONS_URL + pk + '/ultimate-end-users/' + ueu_pk)
    return data.json(), data.status_code


# Ultimate end user Documents
def get_ultimate_end_user_document(request, pk, ueu_pk):
    data = get(request, APPLICATIONS_URL + pk + ULTIMATE_END_USER_URL + ueu_pk + DOCUMENT_URL)
    return data.json(), data.status_code


def post_ultimate_end_user_document(request, pk, ueu_pk, json):
    data = post(request, APPLICATIONS_URL + pk + ULTIMATE_END_USER_URL + ueu_pk + DOCUMENT_URL, json)
    return data.json(), data.status_code


def delete_ultimate_end_user_document(request, pk, ueu_pk):
    data = delete(request, APPLICATIONS_URL + pk + ULTIMATE_END_USER_URL + ueu_pk + DOCUMENT_URL)
    return data.status_code


# Third parties
def get_third_parties(request, pk):
    data = get(request, APPLICATIONS_URL + pk + THIRD_PARTIES_URL)
    return data.json()['third_parties']


def post_third_party(request, pk, json):
    data = post(request, APPLICATIONS_URL + pk + THIRD_PARTIES_URL, json)
    return data.json(), data.status_code


def delete_third_party(request, pk, tp_pk):
    data = delete(request, APPLICATIONS_URL + pk + THIRD_PARTIES_URL + tp_pk)
    return data.status_code


# Third party Documents
def get_third_party_document(request, pk, tp_pk):
    data = get(request, APPLICATIONS_URL + pk + THIRD_PARTIES_URL + tp_pk + DOCUMENT_URL)
    return data.json(), data.status_code


def post_third_party_document(request, pk, tp_pk, json):
    data = post(request, APPLICATIONS_URL + pk + THIRD_PARTIES_URL + tp_pk + DOCUMENT_URL, json)
    return data.json(), data.status_code


def delete_third_party_document(request, pk, tp_pk):
    data = delete(request, APPLICATIONS_URL + pk + THIRD_PARTIES_URL + tp_pk + DOCUMENT_URL)
    return data.status_code


# Consignee
def post_consignee(request, pk, json):
    data = post(request, APPLICATIONS_URL + pk + CONSIGNEE_URL, json)
    return data.json(), data.status_code


def delete_consignee(request, pk):
    data = delete(request, APPLICATIONS_URL + pk + CONSIGNEE_URL)
    return data.status_code


# Consignee Documents
def get_consignee_document(request, pk):
    data = get(request, APPLICATIONS_URL + pk + CONSIGNEE_DOCUMENT_URL)
    return data.json(), data.status_code


def post_consignee_document(request, pk, json):
    data = post(request, APPLICATIONS_URL + pk + CONSIGNEE_DOCUMENT_URL, json)
    return data.json(), data.status_code


def delete_consignee_document(request, pk):
    data = delete(request, APPLICATIONS_URL + pk + CONSIGNEE_DOCUMENT_URL)
    return data.status_code


# Additional Documents
def post_additional_document(request, pk, json):
    data = post(request, APPLICATIONS_URL + pk + ADDITIONAL_DOCUMENT_URL, json)
    return data.json(), data.status_code


def get_additional_documents(request, pk):
    data = get(request, APPLICATIONS_URL + pk + ADDITIONAL_DOCUMENT_URL)
    return data.json(), data.status_code


def get_additional_document(request, pk, doc_pk):
    data = get(request, APPLICATIONS_URL + pk + ADDITIONAL_DOCUMENT_URL + doc_pk + '/')
    return data.json(), data.status_code


def delete_additional_party_document(request, pk, doc_pk):
    data = delete(request, APPLICATIONS_URL + pk + ADDITIONAL_DOCUMENT_URL + doc_pk + '/')
    return data.status_code


def delete_application_preexisting_good(request, good_on_application_pk):
    response = delete(request, APPLICATIONS_URL + 'good-on-application/' + good_on_application_pk)
    return response.status_code


# Case related
def get_case_notes(request, pk):
    data = get(request, CASES_URL + pk + CASE_NOTES_URL)
    return data.json()


def post_application_case_notes(request, pk, json):
    data = post(request, CASES_URL + pk + CASE_NOTES_URL, json)
    return data.json(), data.status_code


def get_ecju_query(request, pk, query_pk):
    data = get(request, CASES_URL + pk + ECJU_QUERIES_URL + query_pk).json()['ecju_query']
    return data


def put_ecju_query(request, pk, query_pk, json):
    data = put(request, CASES_URL + pk + ECJU_QUERIES_URL + query_pk + '/', json)
    return data.json(), data.status_code


def get_application_ecju_queries(request, pk):
    data = get(request, CASES_URL + pk + ECJU_QUERIES_URL).json()['ecju_queries']

    open_queries = [x for x in data if not x['response']]
    closed_queries = [x for x in data if x['response']]

    return open_queries, closed_queries


def set_application_status(request, pk, status):
    json = {'status': status}
    data = put(request, APPLICATIONS_URL + pk + MANAGE_STATUS_URL, json)
    return data.json(), data.status_code


def add_document_data(request):
    files = request.FILES.getlist("file")
    if not files:
        return None, 'No files attached'
    if len(files) != 1:
        return None, 'Multiple files attached'

    file = files[0]
    try:
        original_name = file.original_name
    except Exception: # noqa
        original_name = file.name

    data = {
        'name': original_name,
        's3_key': file.name,
        'size': int(file.size // 1024) if file.size else 0,  # in kilobytes
    }
    if 'description' in request.POST:
        data['description'] = request.POST.get('description')

    return data, None


# Stream file
def generate_file(result):
    for chunk in iter(lambda: result['Body'].read(STREAMING_CHUNK_SIZE), b''):
        yield chunk


def download_document_from_s3(s3_key, original_file_name):
    s3 = s3_client()
    s3_response = s3.get_object(Bucket=AWS_STORAGE_BUCKET_NAME, Key=s3_key)
    _kwargs = {}
    if s3_response.get('ContentType'):
        _kwargs['content_type'] = s3_response['ContentType']
    response = StreamingHttpResponse(generate_file(s3_response), **_kwargs)
    response['Content-Disposition'] = f'attachment; filename="{original_file_name}"'
    return response