from core import client
from caseworker.cases.services import put_case_queues


def filter_licenceable_products(products):
    return [product for product in products if product["is_good_controlled"]["key"] == "True"]


def filter_nlr_products(products):
    return [
        product
        for product in products
        if not product["is_good_controlled"] or product["is_good_controlled"]["key"] == "False"
    ]


def filter_current_user_advice(all_advice, user_id):
    return [
        advice
        for advice in all_advice
        if advice["level"] == "user"
        and advice["type"]["key"] in ["approve", "proviso", "refuse"]
        and (advice["user"]["id"] == user_id)
    ]


def filter_advice_by_type(all_advice, advice_types):
    return [advice for advice in all_advice if advice["type"]["key"] in advice_types]


def filter_advice_by_level(all_advice, advice_levels):
    return [advice for advice in all_advice if advice["level"] in advice_levels]


def filter_advice_by_users_team(all_advice, caseworker):
    return [advice for advice in all_advice if advice["user"]["team"]["id"] == caseworker["team"]["id"]]


def get_advice_to_countersign(case, caseworker):
    advice_by_team = filter_advice_by_users_team(case["advice"], caseworker)
    return filter_advice_by_level(advice_by_team, ["user"])


def get_advice_subjects(case, countries=None):
    """The "advice subject" is an item on a case (eg a good, end user, consignee etc)
    that can have advice related to it. See lite-api/api/cases/models.py for foreign
    key fields on the Advice model.
    """
    destinations = []
    for dest in case.destinations:
        if countries is not None:
            if dest["country"]["id"] not in countries:
                continue
        destinations.append((dest["type"], dest["id"]))
    goods = [("good", good["id"]) for good in case.goods if good["is_good_controlled"]]
    return destinations + goods


def post_approval_advice(request, case, data):
    json = [
        {
            "type": "proviso" if data["proviso"] else "approve",
            "text": data["approval_reasons"],
            "proviso": data["proviso"],
            "note": data["instructions_to_exporter"],
            "footnote_required": True if data["footnote_details"] else False,
            "footnote": data["footnote_details"],
            "good": product["id"],
            "denial_reasons": [],
        }
        for product in filter_licenceable_products(case["data"]["goods"])
    ]

    response = client.post(request, f"/cases/{case['id']}/user-advice/", json)
    response.raise_for_status()
    return response.json(), response.status_code


def post_refusal_advice(request, case, data):
    json = [
        {
            "type": "refuse",
            "text": data["refusal_reasons"],
            "footnote_required": False,
            "good": product["id"],
            "denial_reasons": data["denial_reasons"],
        }
        for product in filter_licenceable_products(case["data"]["goods"])
    ]

    response = client.post(request, f"/cases/{case['id']}/user-advice/", json)
    response.raise_for_status()
    return response.json(), response.status_code


def delete_user_advice(request, case_pk):
    response = client.delete(request, f"/cases/{case_pk}/user-advice/")
    response.raise_for_status()
    return response.json(), response.status_code


def get_users_team_queues(request, user):
    response = client.get(request, f"/users/{user}/team-queues/")
    response.raise_for_status()
    return response.json(), response.status_code


def countersign_advice(request, case, caseworker, formset_data):
    data = []
    queues = []
    case_pk = case["id"]
    advice_to_countersign = get_advice_to_countersign(case, caseworker)

    for index, advice in enumerate(advice_to_countersign):
        form_data = formset_data[index]
        comments = ""
        if form_data["agree_with_recommendation"] == "yes":
            comments = form_data["approval_reasons"]
        elif form_data["agree_with_recommendation"] == "no":
            comments = form_data["refusal_reasons"]
            if form_data["queue_to_return"] not in queues:
                queues.append(form_data["queue_to_return"])

        data.append({"id": advice["id"], "countersigned_by": caseworker["id"], "countersign_comments": comments})

    response = client.put(request, f"/cases/{case_pk}/countersign-advice/", data)
    response.raise_for_status()

    if queues:
        put_case_queues(request, case_pk, json={"queues": queues})

    return response.json(), response.status_code
