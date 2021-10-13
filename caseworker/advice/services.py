from core import client


def post_advice(request, case, data):
    json = {}
    product_ids = [item["id"] for item in case["data"]["goods"]]
    json = []
    for product_id in product_ids:
        json.append({
            "type": "approve",
            "text": data["approval_reasons"],
            "proviso": data["proviso"],
            "note": data["instructions_to_exporter"],
            "footnote_required": True if data["footnote_details"] else False,
            "footnote": data["footnote_details"],
            "good": product_id,
            "denial_reasons": [],
        })

    response = client.post(request, f"/cases/{case['id']}/user-advice/", json)
    response.raise_for_status()
    return response.json(), response.status_code
