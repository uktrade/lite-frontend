import pytest
import requests

from caseworker.cases.forms import review_goods
from caseworker.core.services import get_control_list_entries
from core.middleware import RequestsSessionMiddleware


@pytest.fixture
def control_list_entries(mock_control_list_entries, rf, client):
    request = rf.get("/")
    request.session = client.session
    request.requests_session = requests.Session()
    data = get_control_list_entries(request, convert_to_options=True)
    return [(item.value, item.key) for item in data]


def test_export_control_characteristics_form_no_clc(control_list_entries):
    form = review_goods.ExportControlCharacteristicsForm(
        control_list_entries_choices=control_list_entries,
        data={
            "control_list_entries": [],
            "report_summary": "Foo bar",
        },
    )
    assert form.is_valid() is False
    assert form.errors["does_not_have_control_list_entries"] == [form.MESSAGE_NO_CLC_REQUIRED]


def test_export_control_characteristics_form_mutex(control_list_entries):
    form = review_goods.ExportControlCharacteristicsForm(
        control_list_entries_choices=control_list_entries,
        data={
            "control_list_entries": ["ML1"],
            "does_not_have_control_list_entries": True,
            "report_summary": "Foo bar",
        },
    )
    assert form.is_valid() is False
    assert form.errors["does_not_have_control_list_entries"] == [form.MESSAGE_NO_CLC_MUTEX]


@pytest.mark.parametrize(
    "data",
    [
        {
            "control_list_entries": ["ML1"],
            "report_summary": "Foo bar",
        },
        {"control_list_entries": ["ML1"], "report_summary": "Foo bar", "is_precedent": True},
        {"control_list_entries": ["ML1"], "report_summary": "Foo bar", "is_precedent": False},
    ],
)
def test_export_control_characteristics_form_ok(control_list_entries, data):
    form = review_goods.ExportControlCharacteristicsForm(
        control_list_entries_choices=control_list_entries,
        data=data,
    )
    assert form.is_valid() is True
