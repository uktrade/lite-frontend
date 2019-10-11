from conf.client import get, post, put, delete
from conf.constants import APPLICATIONS_URL, END_USER_DOCUMENT_URL, ULTIMATE_END_USER_URL, DOCUMENT_URL, \
    CONSIGNEE_URL, THIRD_PARTIES_URL, CONSIGNEE_DOCUMENT_URL, APPLICATION_SUBMIT_URL, ADDITIONAL_DOCUMENT_URL


def get_draft_applications(request):
    data = get(request, APPLICATIONS_URL + '?submitted=false')
    return data.json(), data.status_code


def get_draft_application(request, pk):
    data = get(request, APPLICATIONS_URL + pk + '?submitted=false')
    return data.json(), data.status_code


def post_draft_application(request, json):
    data = post(request, APPLICATIONS_URL, json)
    return data.json(), data.status_code


def put_draft_application(request, pk, json):
    data = put(request, APPLICATIONS_URL + pk + '/', json)
    return data.json(), data.status_code


def delete_draft_application(request, pk):
    data = delete(request, APPLICATIONS_URL + pk)
    return data.json(), data.status_code


def submit_draft_application(request, pk):
    data = put(request, APPLICATIONS_URL + pk + APPLICATION_SUBMIT_URL, json={})
    return data.json(), data.status_code


# Goods
def get_draft_application_goods(request, pk):
    data = get(request, APPLICATIONS_URL + pk + '/goods/')
    return data.json(), data.status_code


def get_application_goods_types(request, pk):
    data = get(request, APPLICATIONS_URL + pk + '/goodstype/')
    return data.json(), data.status_code


def get_draft_good(request, pk, good_pk):
    data = get(request, APPLICATIONS_URL + pk + '/goods/' + good_pk + '/')
    return data.json(), data.status_code


def post_draft_preexisting_goods(request, pk, json):
    data = post(request, APPLICATIONS_URL + pk + '/goods/', json)
    return data.json(), data.status_code


# Countries
def get_draft_countries(request, pk):
    data = get(request, APPLICATIONS_URL + pk + '/countries/')
    return data.json(), data.status_code


def post_draft_countries(request, pk, json):
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


def delete_end_user_document(request, pk):
    data = delete(request, APPLICATIONS_URL + pk + END_USER_DOCUMENT_URL)
    return data.status_code


# Ultimate End Users
def get_ultimate_end_users(request, pk):
    data = get(request, APPLICATIONS_URL + pk + '/ultimate-end-users/')
    return data.json(), data.status_code


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
    return data.json(), data.status_code


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
