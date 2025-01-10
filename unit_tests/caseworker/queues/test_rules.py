import pytest

from caseworker.queues import rules as caseworker_rules
from caseworker.queues.rules import BULK_APPROVE_ALLOWED_QUEUES


@pytest.mark.parametrize(
    "queue, expected_result",
    (
        ({"id": BULK_APPROVE_ALLOWED_QUEUES["MOD_CAPPROT"]}, True),
        ({"id": BULK_APPROVE_ALLOWED_QUEUES["MOD_DI_INDIRECT"]}, True),
        ({"id": BULK_APPROVE_ALLOWED_QUEUES["MOD_DSR"]}, True),
        ({"id": BULK_APPROVE_ALLOWED_QUEUES["MOD_DSTL"]}, True),
        ({"id": "fake_queue"}, False),
    ),
)
def test_can_user_bulk_approve_cases(get_mock_request_user, queue, expected_result):
    assert caseworker_rules.can_user_bulk_approve_cases(get_mock_request_user(None), queue) is expected_result
