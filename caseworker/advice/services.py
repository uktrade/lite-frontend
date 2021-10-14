from core import client


def post_approval_advice(request, case, data):
    product_ids = [item["id"] for item in case["data"]["goods"]]
    json = [
        {
            "type": "proviso" if data["proviso"] else "approve",
            "text": data["approval_reasons"],
            "proviso": data["proviso"],
            "note": data["instructions_to_exporter"],
            "footnote_required": True if data["footnote_details"] else False,
            "footnote": data["footnote_details"],
            "good": product_id,
            "denial_reasons": [],
        }
        for product_id in product_ids
    ]

    response = client.post(request, f"/cases/{case['id']}/user-advice/", json)
    response.raise_for_status()
    return response.json(), response.status_code


def post_refusal_advice(request, case, data):
    product_ids = [item["id"] for item in case["data"]["goods"]]
    json = [
        {
            "type": "refuse",
            "text": data["refusal_reasons"],
            "footnote_required": False,
            "good": product_id,
            "denial_reasons": data["denial_reasons"],
        }
        for product_id in product_ids
    ]

    response = client.post(request, f"/cases/{case['id']}/user-advice/", json)
    response.raise_for_status()
    return response.json(), response.status_code
