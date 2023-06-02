from datetime import datetime, date
import logging
from collections import OrderedDict

from django.urls import reverse
from django.utils.http import urlencode

from caseworker.users.services import get_gov_user
from core import client

logger = logging.getLogger(__name__)


def fetch_bookmarks(request, filter_data):
    response = client.get(request, "/bookmarks/")
    if response.status_code >= 300:
        # Not important enough to break the page, so return an empty set of bookmarks.
        logger.error("Error retrieving bookmarks. Status code: %s; Message: %s", response.status_code, response.json)
        return {"user": []}

    bookmarks = response.json()
    for bookmark in bookmarks["user"]:
        enrich_bookmark_for_display(bookmark, filter_data)

    return bookmarks


def add_bookmark(request, data, raw_filters):
    filter_to_save = enrich_filter_for_saving(data, raw_filters)
    now = datetime.today().strftime("%y%m%d-%H%M%S")
    filter_name = f"New unnamed filter ({now})"
    bookmark_name = filter_name
    user, _ = get_gov_user(request)
    user_id = user["user"]["id"]

    for k, v in filter_to_save.items():
        if type(v) == date:
            filter_to_save[k] = v.strftime("%d-%m-%Y")
    data = {
        "filter_json": filter_to_save,
        "name": bookmark_name,
        "user_id": user_id,
    }
    response = client.post(request, f"/bookmarks", data)

    return response


def delete_bookmark(request, bookmark_id):
    data = {"id": bookmark_id}
    response = client.delete(request, f"/bookmarks", data)
    return response


def rename_bookmark(request, bookmark_id, name):
    data = {"id": bookmark_id, "name": name}
    return client.put(request, f"/bookmarks", data)


def enrich_bookmark_for_display(bookmark, filter_data):
    base_url = reverse("queues:cases")
    bookmark_filter = bookmark["filter_json"]
    bookmark["description"] = description_from_filter(bookmark_filter, filter_data)

    for key in ["submitted_from", "submitted_to", "finalised_from", "finalised_to"]:
        if key in bookmark_filter:
            date_str = bookmark_filter[key]
            d, m, y = date_str.split("-")
            del bookmark_filter[key]
            bookmark_filter[f"{key}_0"] = d
            bookmark_filter[f"{key}_1"] = m
            bookmark_filter[f"{key}_2"] = y

    for key in list(bookmark_filter.keys()):
        if key.startswith("_id_"):
            del bookmark_filter[key]

    query = urlencode(bookmark_filter)
    url = f"{base_url}?{query}"
    bookmark["url"] = url


def description_from_filter(bookmark_filter, filter_data):
    filter_dict = {**bookmark_filter}

    _enrich_value_from_filter_data(filter_dict, filter_data, "assigned_user", "gov_users", "id", "full_name")
    _enrich_value_from_filter_data(filter_dict, filter_data, "case_officer", "gov_users", "id", "full_name")
    _enrich_value_from_filter_data(filter_dict, filter_data, "case_type", "case_types")
    _enrich_value_from_filter_data(filter_dict, filter_data, "status", "statuses")
    _enrich_value_from_filter_data(filter_dict, filter_data, "team_advice_type", "advice_types")
    _enrich_value_from_filter_data(filter_dict, filter_data, "final_advice_type", "advice_types")

    _swap_ids_for_readable_values(filter_dict)

    return ", ".join([f"{k.capitalize().replace('_', ' ')}: {v.replace('_', ' ')}" for (k, v) in filter_dict.items()])


def enrich_filter_for_saving(data, raw_filters):
    keys_to_remove = [
        "csrfmiddlewaretoken",
        "save",
        "save_filter",
        "saved_filter_description",
        "saved_filter_name",
        "return_to",
    ]

    filters = {k: data[k] for k in data.keys() if data[k] and k not in keys_to_remove}

    # Add in _id_ prefixed data to preserve country and regime names.
    for key in raw_filters:
        if key.startswith("_id_") and key[4:] in filters:
            filters[key] = raw_filters[key]

    return OrderedDict(sorted(filters.items()))


def _enrich_value_from_filter_data(
    bookmark_filter, filter_data, bookmark_filter_key, filter_data_key, id_key="key", value_key="value"
):
    if bookmark_filter_key in bookmark_filter:
        case_type = bookmark_filter[bookmark_filter_key]
        case_type_dict = {x[id_key]: x[value_key] for x in filter_data[filter_data_key]}
        bookmark_filter[bookmark_filter_key] = case_type_dict.get(case_type, case_type)


def _swap_ids_for_readable_values(filter_dict):
    for key in list(filter_dict.keys()):
        if key.startswith("_id_") and key[4:] in filter_dict:
            filter_dict[key[4:]] = filter_dict[key]
            del filter_dict[key]
