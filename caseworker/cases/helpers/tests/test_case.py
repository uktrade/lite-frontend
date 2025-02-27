import pytest

from ..case import get_case_detail_url


@pytest.mark.parametrize(
    "case, expected",
    (
        (
            {
                "id": "67271217-7e55-4345-9db4-31de1bfe4067",
                "case_type": {
                    "id": "00000000-0000-0000-0000-000000000007",
                    "reference": {"key": "f680", "value": "MOD F680 Clearance"},
                    "sub_type": {"key": "f680_clearance", "value": "MOD F680 Clearance"},
                    "type": {"key": "application", "value": "Application"},
                },
            },
            "/queues/00000000-0000-0000-0000-000000000001/cases/67271217-7e55-4345-9db4-31de1bfe4067/f680/",
        ),
        (
            {
                "id": "67271217-7e55-4345-9db4-31de1bfe4067",
                "case_type": {
                    "id": "00000000-0000-0000-0000-000000000004",
                    "reference": {"key": "siel", "value": "Standard Individual Export Licence"},
                    "type": {"key": "application", "value": "Application"},
                    "sub_type": {"key": "standard", "value": "Standard Licence"},
                },
            },
            "/queues/00000000-0000-0000-0000-000000000001/cases/67271217-7e55-4345-9db4-31de1bfe4067/details/",
        ),
    ),
)
def test_get_case_detail_url(case, expected):
    queue_id = "00000000-0000-0000-0000-000000000001"
    result = get_case_detail_url(case["id"], case["case_type"], queue_id)

    assert result == expected
