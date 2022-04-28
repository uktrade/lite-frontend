from collections import defaultdict
from core import client


def get_good_precedents(request, case_id):
    """For all the goods in the the given case, return the precedents."""
    response = client.get(request, f"/cases/{case_id}/good-precedents/")
    response.raise_for_status()
    return response.json()


def group_gonas_by_good(gonas):
    goods = defaultdict(list)
    for gona in gonas:
        goods[gona["good"]].append(gona)
    return goods


def get_last_precedent(gona, good_precedents):
    precedents = good_precedents[gona["good"]["id"]]
    if precedents:
        precedents.sort(key=lambda p: p["submitted_at"])
        return precedents[0]


def get_recent_precedent(request, case):
    """For all the goods in the given case, return the most recent precedents."""
    results = get_good_precedents(request, case.id)["results"]
    good_precedents = group_gonas_by_good(results)
    return {gona["id"]: get_last_precedent(gona, good_precedents) for gona in case.goods}
