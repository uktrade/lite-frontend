from core import client


def post_approval_advice(request, case, data, level="user-advice"):
    json = [
        {
            "type": "proviso" if data.get("proviso", False) else "approve",
            "text": data["approval_reasons"],
            "proviso": data.get("proviso", ""),
            "note": data.get("instructions_to_exporter", ""),
            "footnote_required": True if data.get("footnote_details") else False,
            "footnote": data.get("footnote_details", ""),
            "denial_reasons": [],
        }
    ]
    response = client.post(request, f"/cases/{case['id']}/{level}/", json)
    response.raise_for_status()
    return response.json(), response.status_code
