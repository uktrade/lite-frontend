from importlib import import_module, reload
import sys

from collections import defaultdict
from datetime import datetime

from django.utils import timezone
from django.conf import settings
from django.urls import clear_url_caches


def reload_urlconf(urlconfs=None):
    if not urlconfs:
        urlconfs = [settings.ROOT_URLCONF]
    clear_url_caches()
    for urlconf in urlconfs:
        if urlconf in sys.modules:
            reload(sys.modules[urlconf])
        else:
            import_module(urlconf)


def mocked_now():
    return datetime(2020, 1, 1, tzinfo=timezone.utc)


def merge_summaries(summary_1, summary_2):
    get_summary_dict = lambda summary: {item[0]: (item[0], item[1], item[2]) for item in summary}
    summary_1_dict = get_summary_dict(summary_1)
    summary_2_dict = get_summary_dict(summary_2)
    combined_summary = {**summary_1_dict, **summary_2_dict}
    return tuple(combined_summary.values())


def get_rows(table):
    rows = []
    for table_row in table.select("tbody .govuk-table__row"):
        cells = []
        for row_cell in table_row.select(".govuk-table__cell"):
            cells.append(row_cell.text)
        rows.append(cells)
    return rows


def sort_request_history(request_history):
    history = defaultdict(list)
    for request in request_history:
        history[request.path].append(request)
    return history
