import pytest

from caseworker.queues import rules as caseworker_rules
from caseworker.advice.constants import (
    DESNZ_CHEMICAL_CASES_TO_REVIEW,
    DESNZ_NUCLEAR_CASES_TO_REVIEW,
    FCDO_CASES_TO_REVIEW_QUEUE,
    MOD_CAPPROT_CASES_TO_REVIEW,
    MOD_DI_DIRECT_CASES_TO_REVIEW,
    MOD_DI_INDIRECT_CASES_TO_REVIEW,
    MOD_DSR_CASES_TO_REVIEW,
    MOD_DSTL_CASES_TO_REVIEW,
    NCSC_CASES_TO_REVIEW,
)


@pytest.mark.parametrize(
    "queue_id, expected_result",
    (
        (DESNZ_CHEMICAL_CASES_TO_REVIEW, False),
        (DESNZ_NUCLEAR_CASES_TO_REVIEW, False),
        (FCDO_CASES_TO_REVIEW_QUEUE, False),
        (MOD_CAPPROT_CASES_TO_REVIEW, True),
        (MOD_DI_DIRECT_CASES_TO_REVIEW, True),
        (MOD_DI_INDIRECT_CASES_TO_REVIEW, True),
        (MOD_DSR_CASES_TO_REVIEW, True),
        (MOD_DSTL_CASES_TO_REVIEW, True),
        (NCSC_CASES_TO_REVIEW, True),
    ),
)
def test_can_user_bulk_approve_cases(get_mock_request_user, queue_id, expected_result):
    assert caseworker_rules.can_user_bulk_approve_cases(get_mock_request_user(None), queue_id) is expected_result
