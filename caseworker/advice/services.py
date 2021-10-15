from core import client


def post_approval_advice(request, case, data):
    licenceable_products = [
        product for product in case["data"]["goods"] if product["is_good_controlled"]["key"] == "True"
    ]
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
        for product in licenceable_products
    ]

    response = client.post(request, f"/cases/{case['id']}/user-advice/", json)
    response.raise_for_status()
    return response.json(), response.status_code


def post_refusal_advice(request, case, data):
    licenceable_products = [
        product for product in case["data"]["goods"] if product["is_good_controlled"]["key"] == "True"
    ]
    json = [
        {
            "type": "refuse",
            "text": data["refusal_reasons"],
            "footnote_required": False,
            "good": product["id"],
            "denial_reasons": data["denial_reasons"],
        }
        for product in licenceable_products
    ]

    response = client.post(request, f"/cases/{case['id']}/user-advice/", json)
    response.raise_for_status()
    return response.json(), response.status_code
