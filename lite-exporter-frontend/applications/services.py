from conf.client import get


def get_applications(request):
    data = get(request, '/applications/')
    return data.json(), data.status_code


def get_application(request, pk):
    data = get(request, '/applications/' + pk)
    return data.json(), data.status_code
