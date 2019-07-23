from conf.client import get, post


def get_applications(request):
    data = get(request, '/applications/')
    return data.json(), data.status_code


def get_application(request, pk):
    data = get(request, '/applications/' + pk + '/pk-user/')
    return data.json(), data.status_code


def post_application_notes(request, pk, json):
    data = post(request, '/cases/' + pk + '/case_notes/', json)
    return data.json(), data.status_code
