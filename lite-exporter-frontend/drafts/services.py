from conf.client import get, post, put, delete
from conf.constants import APPLICATIONS_URL, DRAFTS_URL


def get_drafts(request):
    data = get(request, DRAFTS_URL)
    return data.json(), data.status_code


def get_draft(request, pk):
    data = get(request, DRAFTS_URL + pk)
    return data.json(), data.status_code


def post_drafts(request, json):
    data = post(request, DRAFTS_URL, json)
    return data.json(), data.status_code


def put_draft(request, pk, json):
    data = put(request, DRAFTS_URL + pk + '/', json)
    return data.json(), data.status_code


def delete_draft(request, pk):
    data = delete(request, DRAFTS_URL + pk)
    return data.json(), data.status_code


def submit_draft(request, pk):
    data = post(request, APPLICATIONS_URL, {'id': pk})
    return data.json(), data.status_code


# Goods
def get_draft_goods(request, pk):
    data = get(request, DRAFTS_URL + pk + '/goods/')
    return data.json(), data.status_code


def get_draft_good(request, pk, good_pk):
    data = get(request, DRAFTS_URL + pk + '/goods/' + good_pk + '/')
    return data.json(), data.status_code


def post_draft_preexisting_goods(request, pk, json):
    data = post(request, DRAFTS_URL + pk + '/goods/', json)
    return data.json(), data.status_code


# End Users
def get_end_user(request, pk):
    data = get(request, DRAFTS_URL + pk + '/goods/')
    return data.json(), data.status_code


def post_end_user(request, pk, json):
    data = post(request, DRAFTS_URL + pk + '/end-user/', json)
    return data.json(), data.status_code
