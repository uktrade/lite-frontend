import pytest
from uuid import uuid4

from ..case import get_case_detail_url


@pytest.mark.parametrize(
    "case_type, expected",
    (
        (
            "f680_clearance",
            "f680",
        ),
        (
            "standard",
            "details",
        ),
    ),
)
def test_get_case_detail_url(case_type, expected):
    case_id = uuid4()
    queue_id = "00000000-0000-0000-0000-000000000001"
    result = get_case_detail_url(case_id, case_type, queue_id)

    assert result == f"/queues/{queue_id}/cases/{case_id}/{expected}/"
