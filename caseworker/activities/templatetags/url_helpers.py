from django import template
from django.urls import reverse
from caseworker.cases.constants import CaseType

register = template.Library()


@register.simple_tag
def get_notes_and_timelines_url(case_id, reference_code, queue_id):
    if reference_code and reference_code.startswith("F680"):
        case_type = CaseType.F680.value
    else:
        case_type = CaseType.STANDARD.value

    destinations = {
        "f680_clearance": {"url": "cases:f680:notes_and_timeline", "kwargs": {"queue_pk": queue_id, "pk": case_id}},
        "standard": {"url": "cases:activities:notes-and-timeline", "kwargs": {"queue_pk": queue_id, "pk": case_id}},
    }

    url_name = destinations[case_type]["url"]
    kwargs = destinations[case_type]["kwargs"]
    return reverse(url_name, kwargs=kwargs)
