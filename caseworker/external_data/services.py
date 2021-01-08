from core import client


def upload_denials(request, data):
    return client.post(request=request, appended_address="/external-data/denial/", data=data,)


def search_denials(request, data):
    return client.get(request=request, appended_address="/external-data/denial-search/", data=data)
