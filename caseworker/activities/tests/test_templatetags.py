from uuid import uuid4
from caseworker.activities.templatetags.url_helpers import get_notes_and_timelines_url

from django.urls import reverse

import pytest


@pytest.mark.parametrize(
    "reference_code, expected_url_name, expected" "_extra_kwargs",
    (
        (
            "F680/2025/0000001",
            "cases:f680:notes_and_timeline",
            {},
        ),
        (
            "SIEL/2025/0000001",
            "cases:activities:notes-and-timeline",
            {},
        ),
    ),
)
def test_get_notes_and_timelines_url(reference_code, expected_url_name, expected_extra_kwargs):
    case_id = uuid4()
    queue_id = "00000000-0000-0000-0000-000000000001"
    result = get_notes_and_timelines_url(case_id, reference_code, queue_id)

    expected_url = reverse(expected_url_name, kwargs={"queue_pk": queue_id, "pk": case_id, **expected_extra_kwargs})

    assert result == expected_url
