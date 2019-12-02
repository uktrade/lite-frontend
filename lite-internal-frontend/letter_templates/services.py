from conf.client import get, post, put
from conf.constants import PICKLIST_URL, LETTER_TEMPLATES_URL, LETTER_LAYOUTS_URL, GENERATE_PREVIEW_URL
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

    data = get(request, PICKLIST_URL + "?type=letter_paragraph" + "&ids=" + ",".join(ids))
    letter_paragraphs = data.json()["picklist_items"]
    return sort_letter_paragraphs(letter_paragraphs, ids)


def get_letter_template(request, pk, generate_preview=False):
    data = get(request, LETTER_TEMPLATES_URL + pk + "?generate_preview=" + str(generate_preview))
    return data.json(), data.status_code


def put_letter_template(request, pk, json):
    data = put(request, LETTER_TEMPLATES_URL + pk, json)
    return data.json(), data.status_code


def get_letter_templates(request, params=None):
    url = LETTER_TEMPLATES_URL
    data = get(request, url + "?" + params)
    return data.json()["results"]


def post_letter_template(request, json):
    data = post(request, LETTER_TEMPLATES_URL, json)
    return data.json(), data.status_code


def get_letter_layouts(request=None):
    data = get(request, LETTER_LAYOUTS_URL)
    return data.json()["results"]


def get_letter_layout(request, pk):
    data = get(request, LETTER_LAYOUTS_URL + pk)
    return data.json(), data.status_code


def get_letter_preview(request, layout_id, paragraph_ids):
    data = {"layout": str(layout_id), "paragraphs": paragraph_ids}
    get_params = "?" + convert_dict_to_query_params(data)
    data = get(request, LETTER_TEMPLATES_URL + GENERATE_PREVIEW_URL + get_params)
    return data.json(), data.status_code
