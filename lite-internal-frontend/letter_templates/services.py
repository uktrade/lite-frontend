from conf.client import get, post, put
from conf.constants import PICKLIST_URL, LETTER_TEMPLATES_URL, LETTER_LAYOUTS_URL


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

    data = get(request, PICKLIST_URL + "?type=letter_paragraph" + "&ids=" + ",".join(ids))
    letter_paragraphs = data.json()["picklist_items"]
    return sort_letter_paragraphs(letter_paragraphs, ids)


def get_letter_template(request, pk):
    data = get(request, LETTER_TEMPLATES_URL + pk)
    return data.json()


def put_letter_template(request, pk, json):
    data = put(request, LETTER_TEMPLATES_URL + pk, json)
    return data.json(), data.status_code


def get_letter_templates(request, params):
    data = get(request, LETTER_TEMPLATES_URL + "?" + params)
    return data.json()


def post_letter_template(request, json):
    data = post(request, LETTER_TEMPLATES_URL, json)
    return data.json(), data.status_code


def get_letter_layouts(request=None):
    data = get(request, LETTER_LAYOUTS_URL)
    return data.json()["results"]


def get_letter_layout(request, pk):
    data = get(request, LETTER_LAYOUTS_URL + pk)
    return data.json(), data.status_code
