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
    bookmark["url"] = url_from_bookmark(base_url, bookmark_filter)


def url_from_bookmark(base_url, bookmark_filter):
    for key in ["submitted_from", "submitted_to", "finalised_from", "finalised_to"]:
        if key in bookmark_filter:
            date_str = bookmark_filter[key]
            d, m, y = date_str.split("-")
            del bookmark_filter[key]
            bookmark_filter[f"{key}_0"] = d
            bookmark_filter[f"{key}_1"] = m
            bookmark_filter[f"{key}_2"] = y

    # We don't need the _id_ prefixed entries in the url
    for key in list(bookmark_filter.keys()):
        if key.startswith("_id_"):
            del bookmark_filter[key]

    query = urlencode(bookmark_filter)
    return f"{base_url}?{query}"


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

    # Add in _id_ prefixed data to preserve country and regime names. This is to prevent
    # unnecessary lookup when we display the bookmarks later, as the description and
    # url display need different values for these filters (status, gov_user etc)
    # the former needing the display value and the latter an id.
    for key in raw_filters:
        if key.startswith("_id_") and key[4:] in filters:
            filters[key] = raw_filters[key]

    return OrderedDict(sorted(filters.items()))


def _enrich_value_from_filter_data(
    bookmark_filter, filter_data, bookmark_filter_key, filter_data_key, id_key="key", value_key="value"
):
    """
    Some filters (e.g. assigned_user, status) have their ids stored rather than human readable value.
    For these, we have access to the human readable value in the filter_data lists which are
    used in the lookups for those filters. This function replaces those ids with the
    looked up entry in the filter_data for display purposes.

    The filter_data is a dictionary with the data type as key (e.g. 'statuses' or 'gov_users')
    and a list of the objects for the dropdown as the value. e.g.

    {
    'statuses': [{'id': '00000000-0000-0000-0000-000000000001', 'key': 'submitted', 'value': 'Submitted', ...],
    'gov_users': {...
    }

    Params:
    bookmark_filter: the bookmark filter we are enriching
    filter_data: the filter data dictionary to fetch the enrichment data from
    bookmark_filter_key: the entry in the filter we want to enrich
    filter_data_key: key for the data type we want to look up
    id_key: the key in the filter_data object that our id should match. Usually just "key", but "id" for users.
    value_key: the key in the filter_data object that contains the human readable value we are enriching with.
    """
    if bookmark_filter_key in bookmark_filter:
        entry_id = bookmark_filter[bookmark_filter_key]
        matching_data_item = [entry for entry in filter_data[filter_data_key] if entry[id_key] == entry_id]
        if matching_data_item:
            bookmark_filter[bookmark_filter_key] = matching_data_item[0][value_key]


def _swap_ids_for_readable_values(filter_dict):
    """
    Some filters (notably the Regime and Country filters) store their id in the field entry
    and (counterintuitively) store the human readable variant of this in an '_id_' prefixed
    entry in the filter dictionary. We preserve this in the filter_json in order to avoid
    having to look this data up at this enrichment stage. This function replaces the id in
    these fields with the human readable value from the _id_ prefixed entry.
    """
    for key in list(filter_dict.keys()):
        if key.startswith("_id_") and key[4:] in filter_dict:
            filter_dict[key[4:]] = filter_dict[key]
            # We don't want to display these _id_ fields, so delete them after we've used them.
            del filter_dict[key]
