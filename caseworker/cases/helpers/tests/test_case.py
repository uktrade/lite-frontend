import pytest
from uuid import uuid4

from django.urls import reverse

from ..case import get_case_detail_url


@pytest.mark.parametrize(
    "case_type, expected_url_name, expected_extra_kwargs",
    (
        (
            "f680_clearance",
            "cases:f680:details",
            {},
        ),
        (
            "standard",
            "cases:case",
            {"tab": "details"},
        ),
    ),
)
def test_get_case_detail_url(case_type, expected_url_name, expected_extra_kwargs):
    case_id = uuid4()
    queue_id = "00000000-0000-0000-0000-000000000001"
    result = get_case_detail_url(case_id, case_type, queue_id)

    expected_url = reverse(expected_url_name, kwargs={"queue_pk": queue_id, "pk": case_id, **expected_extra_kwargs})

    assert result == expected_url
