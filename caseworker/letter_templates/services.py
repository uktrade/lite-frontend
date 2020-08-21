from core import client
from core.helpers import convert_dict_to_query_params


def sort_letter_paragraphs(paragraphs, ids):
    """Order a list of letter paragraphs in the same order as a list of IDs."""
    sorted_paragraphs = []
    for id in ids:
        for paragraph in paragraphs:
            if id == paragraph["id"]:
                sorted_paragraphs.append(paragraph)
                break
    return sorted_paragraphs


def get_letter_paragraphs(request, ids: list):
    if not ids:
        return []

    data = client.get(request, "/picklist/?type=letter_paragraph&disable_pagination=True&ids=" + ",".join(ids))
    letter_paragraphs = data.json()["results"]
    return sort_letter_paragraphs(letter_paragraphs, ids)


def get_letter_template(request, pk, params=""):
    data = client.get(request, f"/letter-templates/{pk}/?{params}")
    return data.json(), data.status_code


def put_letter_template(request, pk, json):
    data = client.put(request, f"/letter-templates/{pk}/", json)
    return data.json(), data.status_code


def get_letter_templates(request, params=""):
    data = client.get(request, f"/letter-templates/?{params}")
    return data.json(), data.status_code


def post_letter_template(request, json):
    data = client.post(request, "/letter-templates/", json)
    return data.json(), data.status_code


def get_letter_layouts(request=None):
    data = client.get(request, "/static/letter-layouts/")
    return data.json()["results"]


def get_letter_layout(request, pk):
    data = client.get(request, f"/static/letter-layouts/{pk}")
    return data.json(), data.status_code


def get_letter_preview(request, layout_id, paragraph_ids):
    querystring = convert_dict_to_query_params({"layout": layout_id, "paragraphs": paragraph_ids})
    data = client.get(request, f"/letter-templates/generate-preview/?{querystring}")
    return data.json(), data.status_code
