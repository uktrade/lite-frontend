from core import client


def upload_denials(request, data):
    return client.post(request=request, appended_address="/external-data/denial/", data=data,)


def search_denials(request, data):
    return client.get(request=request, appended_address="/external-data/denial-search/", data=data)


def get_denial(request, pk):
    response = client.get(request=request, appended_address=f"/external-data/denial/{pk}/")
    response.raise_for_status()
    return response.json()


def revoke_denial(request, pk):
    response = client.patch(request=request, appended_address=f"/external-data/denial/{pk}/", data={'is_revoked': True})
    response.raise_for_status()
    return response.json()
