from urllib.parse import urlencode

from core import client


def upload_denials(request, data):
    return client.post(
        request=request,
        appended_address="/external-data/denial/",
        data=data,
    )


def search_denials(request, search, filter):
    page = request.GET.get("page", 1)
    data = {"search": search, "page": page, **filter}

    querystring = urlencode(data, doseq=True, safe=":")

    response = client.get(request=request, appended_address=f"/external-data/denial-search/?{querystring}")
    return response.json(), response.status_code


def get_denial(request, pk):
    response = client.get(request=request, appended_address=f"/external-data/denial/{pk}/")
    response.raise_for_status()
    return response.json()


def revoke_denial(request, pk, comment):
    response = client.patch(
        request=request,
        appended_address=f"/external-data/denial/{pk}/",
        data={"is_revoked": True, "is_revoked_comment": comment},
    )
    response.raise_for_status()
    return response.json()


def get_sanction(request, pk):
    response = client.get(request=request, appended_address=f"/external-data/sanction/{pk}/")
    response.raise_for_status()
    return response.json()


def revoke_sanction(request, pk, comment):
    response = client.patch(
        request=request,
        appended_address=f"/external-data/sanction/{pk}/",
        data={"is_revoked": True, "is_revoked_comment": comment},
    )
    response.raise_for_status()
