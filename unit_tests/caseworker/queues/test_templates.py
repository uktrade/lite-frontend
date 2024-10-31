import pytest
from bs4 import BeautifulSoup
from django.template.loader import render_to_string

from caseworker.queues.views.forms import CasesFiltersForm


@pytest.fixture()
def all_regimes(data_regime_entries):
    return [
        {"id": regime["pk"], "name": regime["name"]} for regime in sorted(data_regime_entries, key=lambda r: r["name"])
    ]


@pytest.mark.parametrize(
    "duration",
    [
        0,
        None,
        10,
        25,
    ],
)
def test_sla_display_hours(duration):
    context = {"case": {"sla_hours_since_raised": duration, "case_subtype": {"sub_type": {"key": "hmrc"}}}}
    assert render_to_string("includes/sla_display.html", context)


@pytest.mark.parametrize(
    "elapsed,remaining",
    [
        (0, 0),
        (None, None),
        (10, 10),
        (25, 25),
    ],
)
def test_sla_display_days(elapsed, remaining):
    context = {
        "case": {
            "sla_days": elapsed,
            "sla_remaining_days": remaining,
        }
    }
    assert render_to_string("includes/sla_display.html", context)


def test_cases_with_flags(
    data_standard_case,
    flags,
    all_cles,
    all_regimes,
    data_countries,
):
    context = {}
    context["queue"] = {"id": "00000000-0000-0000-0000-000000000001"}
    case = data_standard_case["case"]
    case["goods_flags"] = [
        {
            "name": "Item not verified",
            "label": "not-verified",
            "colour": "default",
        }
    ]
    case["destinations_flags"] = [
        {
            "name": "Red Destination",
            "label": None,
            "colour": "red",
        }
    ]
    filters = {
        "case_types": [],
        "statuses": [],
        "gov_users": [],
        "advice_types": [],
    }
    queue = {"id": "cfac8bf4-d325-4e8e-9c28-0fe93c0ecf80", "is_system_queue": True}

    context["data"] = {"results": {"cases": [case]}}
    context["form"] = CasesFiltersForm(
        queue,
        filters,
        flags,
        all_cles,
        all_regimes,
        data_countries["countries"],
        [],
    )

    html = render_to_string("queues/cases.html", context)
    soup = BeautifulSoup(html, "html.parser")

    flags = soup.find("ol", class_="app-flags--list").text
    assert "Enforcement Check Req" in flags
    assert "Item not verified" in flags
    assert "Red Destination" in flags


def test_cases_without_flags(
    data_standard_case,
    flags,
    all_cles,
    all_regimes,
    data_countries,
):
    context = {}
    context["queue"] = {"id": "00000000-0000-0000-0000-000000000001"}
    case = data_standard_case["case"]
    case["flags"] = []
    filters = {
        "case_types": [],
        "statuses": [],
        "gov_users": [],
        "advice_types": [],
    }
    queue = {"id": "cfac8bf4-d325-4e8e-9c28-0fe93c0ecf80", "is_system_queue": True}

    context["data"] = {"results": {"cases": [case]}}
    context["form"] = CasesFiltersForm(
        queue,
        filters,
        flags,
        all_cles,
        all_regimes,
        data_countries["countries"],
        [],
    )

    html = render_to_string("queues/cases.html", context)
    soup = BeautifulSoup(html, "html.parser")

    assert not soup.find("ol", class_="app-flags--list")
