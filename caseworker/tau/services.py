from collections import defaultdict

from core import client


def get_good_precedents(request, case_id):
    """For all the goods in the the given case, return the precedents."""
    response = client.get(request, f"/cases/{case_id}/good-precedents/")
    response.raise_for_status()
    return response.json()


def get_first_precedents(case, good_precedents):
    """For all the goods in the given case, return the first
    precedent per CLEs"""
    results = {}
    for gona in case.goods:
        results[gona["id"]] = get_first_cles_precedents(gona, good_precedents)
    return results


def group_gonas_by_good(gonas):
    goods = defaultdict(list)
    for gona in gonas:
        goods[gona["good"]].append(gona)
    return goods


def get_latest_precedents(case, good_precedents):
    results = {}
    for gona in case.goods:
        precedents = [p for p in good_precedents[gona["good"]["id"]] if p["submitted_at"]]
        precedents.sort(key=lambda p: p["submitted_at"], reverse=True)
        if precedents:
            results[gona["id"]] = precedents[0]
    return results


def get_first_cles_precedents(gona, good_precedents):
    # The following is for a weird case that broke during testing b/c
    # submitted_at for a case that has been submitted was None!
    precedents = [p for p in good_precedents[gona["good"]["id"]] if p["submitted_at"]]
    cle_precedents = {}
    for precedent in precedents:
        cles = ",".join(sorted(precedent["control_list_entries"]))
        # Add the precedent for this CLE if its not there yet or it is older
        # than the one that is currently there
        if cles not in cle_precedents or precedent["submitted_at"] < cle_precedents[cles]["submitted_at"]:
            cle_precedents[cles] = precedent
    return cle_precedents.values()


def get_document(request, pk):
    data = client.get(request, f"/documents/{pk}")
    return data.json(), data.status_code


def post_document_internal_good_on_application(request, goods_on_application_pk, data):
    response = client.post(request, f"/goods/document_internal_good_on_application/{goods_on_application_pk}/", data)
    response.raise_for_status()
    return response.json(), response.status_code


def delete_good_on_application_document(request, doc_pk):
    response = client.delete(request, f"/goods/document_internal_good_on_application_detail/{doc_pk}/")
    response.raise_for_status()
    return response.json(), response.status_code


def edit_good_on_application_document(request, doc_pk, data):
    response = client.put(request, f"/goods/document_internal_good_on_application_detail/{doc_pk}/", data)
    response.raise_for_status()
    return response.json(), response.status_code
