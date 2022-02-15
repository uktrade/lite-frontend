import pytest

from django.template.loader import render_to_string


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
