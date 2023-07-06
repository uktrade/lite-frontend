import logging

from collections import OrderedDict
from datetime import datetime, date
from decimal import Decimal
from urllib.parse import urlencode

from crispy_forms_gds.fields import DateInputField

from django import forms
from django.conf import settings

from caseworker.queues.views.forms import CasesFiltersForm
from caseworker.users.services import get_gov_user
from core import client

logger = logging.getLogger(__name__)


def fetch_bookmarks(request, filter_data, all_flags, all_cles, all_regimes, queue, bookmark_base_url):
    response = client.get(request, "/bookmarks/")
    if response.status_code >= 300:
        # Not important enough to break the page, so return an empty set of bookmarks.
        logger.error("Error retrieving bookmarks. Status code: %s; Message: %s", response.status_code, response.json)
        return {"user": []}

    bookmarks = response.json()["user"]
    enricher = BookmarkEnricher(request, filter_data, all_flags, all_cles, all_regimes, queue, bookmark_base_url)
    enriched_bookmarks = enricher.enrich_for_display(bookmarks)

    return {"user": enriched_bookmarks}


def add_bookmark(request, data):
    filter_to_save = enrich_filter_for_saving(data)
    now = datetime.today().strftime("%y%m%d-%H%M%S")
    filter_name = f"New unnamed filter ({now})"
    bookmark_name = filter_name
    user, _ = get_gov_user(request)
    user_id = user["user"]["id"]

    data = {
        "filter_json": filter_to_save,
        "name": bookmark_name,
        "user_id": user_id,
    }
    response = client.post(request, "/bookmarks", data)

    return response


def delete_bookmark(request, bookmark_id):
    data = {"id": bookmark_id}
    response = client.delete(request, "/bookmarks", data)
    return response


def rename_bookmark(request, bookmark_id, name):
    data = {"id": bookmark_id, "name": name}
    return client.put(request, "/bookmarks", data)


def get_label_from_field(field):
    return field.label


def get_readable_value_from_field(field, value):
    if isinstance(field, forms.MultipleChoiceField):
        choice_map = dict(field.choices)
        sorted_readable_values = sorted((choice_map[v] for v in value), key=lambda v: v[0])
        return ", ".join(sorted_readable_values)

    if isinstance(field, forms.ChoiceField):
        return dict(field.choices)[value]

    if isinstance(field, DateInputField):
        return value.strftime("%d-%m-%Y")

    return value


def get_description_from_form(form):
    labelled_values = []
    for field_name, field_value in form.cleaned_data.items():
        if not field_value:
            continue

        field = form.fields[field_name]
        label = get_label_from_field(field)
        readable_value = get_readable_value_from_field(field, field_value)
        labelled_values.append((label, readable_value))

    return ", ".join(f"{k}: {v}" for k, v in sorted(labelled_values, key=lambda v: v[0]))


class BookmarkEnricher:
    def __init__(self, request, filter_data, all_flags, all_cles, all_regimes, queue, bookmark_base_url):
        self.request = request
        self.filter_data = filter_data
        self.all_flags = all_flags
        self.all_cles = all_cles
        self.all_regimes = all_regimes
        self.queue = queue
        self.bookmark_base_url = bookmark_base_url

    def enrich_for_display(self, bookmarks):
        enriched_bookmarks = [self._enrich_bookmark_for_display(bookmark) for bookmark in bookmarks]
        return [bookmark for bookmark in enriched_bookmarks if bookmark is not None]

    def _enrich_bookmark_for_display(self, bookmark):
        try:
            out = {**bookmark}
            bookmark_filter = out["filter_json"]
            out["description"] = self._description_from_filter(bookmark_filter)
            out["url"] = self._url_from_bookmark(bookmark_filter)

            return out
        except Exception as ex:  # pylint: disable=broad-except
            logger.exception("Error enriching bookmark")
            if settings.DEBUG:
                raise
            return None

    def _description_from_filter(self, bookmark_filter):
        # We split the dates here because the form is expecting data as if it
        # were originally posted from the form but we store the date as a single
        # value so we need to split it out again
        data = self._split_dates(bookmark_filter)
        form = CasesFiltersForm(
            self.request,
            self.queue,
            self.filter_data,
            self.all_flags,
            self.all_cles,
            self.all_regimes,
            data=data,
        )
        form.full_clean()
        return get_description_from_form(form)

    def _split_dates(self, bookmark_filter):
        bookmark_filter = {**bookmark_filter}
        for key in ["submitted_from", "submitted_to", "finalised_from", "finalised_to"]:
            if key in bookmark_filter:
                date_str = bookmark_filter[key]
                d, m, y = date_str.split("-")
                del bookmark_filter[key]
                bookmark_filter[f"{key}_0"] = d
                bookmark_filter[f"{key}_1"] = m
                bookmark_filter[f"{key}_2"] = y
        return bookmark_filter

    def _url_from_bookmark(self, bookmark_filter):
        bookmark_filter = self._split_dates(bookmark_filter)
        query = urlencode(bookmark_filter, doseq=True)
        return f"{self.bookmark_base_url}?{query}"


def enrich_filter_for_saving(data):
    keys_to_remove = [
        "csrfmiddlewaretoken",
        "save",
        "save_filter",
        "saved_filter_description",
        "saved_filter_name",
        "return_to",
    ]

    filters = {}
    for key, value in data.items():
        if not value:
            continue
        if key in keys_to_remove:
            continue
        if isinstance(value, Decimal):
            filters[key] = str(value)
            continue
        if isinstance(value, date):
            filters[key] = value.strftime("%d-%m-%Y")
            continue
        filters[key] = value

    return OrderedDict(sorted(filters.items()))
