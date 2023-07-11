import logging

from collections import OrderedDict
from datetime import datetime, date
from decimal import Decimal
from urllib.parse import urlencode

from crispy_forms_gds.fields import DateInputField

from django import forms
from django.conf import settings

from caseworker.users.services import get_gov_user
from core import client
from core.helpers import decompose_date

logger = logging.getLogger(__name__)


ENRICHED_DATE_FORMAT = "%d-%m-%Y"


def fetch_bookmarks(request, bookmark_base_url, bookmark_form_provider):
    response = client.get(request, "/bookmarks/")
    if response.status_code >= 300:
        # Not important enough to break the page, so return an empty set of bookmarks.
        logger.error("Error retrieving bookmarks. Status code: %s; Message: %s", response.status_code, response.json)
        return {"user": []}

    bookmarks = response.json()["user"]
    enricher = BookmarkEnricher(bookmark_base_url, bookmark_form_provider)
    enriched_bookmarks = enricher.enrich_for_display(bookmarks)

    return {"user": enriched_bookmarks}


def add_bookmark(request, data, keys_to_remove):
    filter_to_save = enrich_filter_for_saving(data, keys_to_remove)
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
    def __init__(self, bookmark_base_url, bookmark_form_provider):
        self.bookmark_base_url = bookmark_base_url
        self.bookmark_form_provider = bookmark_form_provider

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
        except Exception:  # pylint: disable=broad-except
            if settings.DEBUG:
                raise
            logger.exception("Error enriching bookmark")
            return None

    def _description_from_filter(self, bookmark_filter):
        # We split the dates here because the form is expecting data as if it
        # were originally posted from the form but we store the date as a single
        # value so we need to split it out again
        data = self._split_dates(bookmark_filter)
        form = self.bookmark_form_provider.get_bound_bookmark_form(data)
        form.full_clean()
        return get_description_from_form(form)

    def _split_dates(self, bookmark_filter):
        bookmark_filter = {**bookmark_filter}
        form_class = self.bookmark_form_provider.get_bookmark_form_class()
        for field_name, field in form_class.declared_fields.items():
            if not isinstance(field, DateInputField):
                continue
            if field_name not in bookmark_filter:
                continue
            d = datetime.strptime(bookmark_filter[field_name], ENRICHED_DATE_FORMAT).date()
            del bookmark_filter[field_name]
            bookmark_filter.update(decompose_date(field_name, d))
        return bookmark_filter

    def _url_from_bookmark(self, bookmark_filter):
        bookmark_filter = self._split_dates(bookmark_filter)
        query = urlencode(bookmark_filter, doseq=True)
        return f"{self.bookmark_base_url}?{query}"


def enrich_filter_for_saving(data, keys_to_remove):
    common_keys_to_remove = [
        "csrfmiddlewaretoken",
        "return_to",
    ]
    keys_to_remove = common_keys_to_remove + keys_to_remove

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
            filters[key] = value.strftime(ENRICHED_DATE_FORMAT)
            continue
        filters[key] = value

    return OrderedDict(sorted(filters.items()))
