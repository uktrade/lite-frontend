from core import client


def filter_licenceable_products(products):
    return [product for product in products if product["is_good_controlled"] == {"key": "True", "value": "Yes"}]


def filter_nlr_products(products):
    return [
        product
        for product in products
        if not product["is_good_controlled"] or product["is_good_controlled"] == {"key": "False", "value": "No"}
    ]


def filter_current_user_advice(all_advice, user_id):
    return [
        advice
        for advice in all_advice
        if advice["level"] == "user"
        and advice["type"]["key"] in ["approve", "proviso", "refuse"]
        and (advice["user"]["id"] == user_id)
    ]


def get_advice_subjects(case):
    return [(destination["type"], destination["id"], None) for destination in case.destinations] + [
        ("good", good["id"], good["is_good_controlled"]) for good in case.goods
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
            subject_name: subject_id,
            "denial_reasons": [],
        }
        for subject_name, subject_id, licensable in get_advice_subjects(case)
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
            subject_name: subject_id,
            "denial_reasons": data["denial_reasons"],
        }
        for subject_name, subject_id, licensable in get_advice_subjects(case)
        if subject_name == "good" and licensable == {"key": "True", "value": "Yes"}
    ]

    response = client.post(request, f"/cases/{case['id']}/user-advice/", json)
    response.raise_for_status()
    return response.json(), response.status_code


def delete_user_advice(request, case_pk):
    response = client.delete(request, f"/cases/{case_pk}/user-advice/")
    response.raise_for_status()
    return response.json(), response.status_code
