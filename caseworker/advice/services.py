from core import client


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
