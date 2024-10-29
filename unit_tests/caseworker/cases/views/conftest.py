import pytest
from core import client


@pytest.fixture()
def mock_cases_head(requests_mock, queue_pk):
    url = client._build_absolute_uri(f"/cases/?queue_id={queue_pk}&page=1")
    yield requests_mock.head(
        url=url,
        headers={"Resource-Count": ""},
    )


@pytest.fixture()
def mock_cases(requests_mock, queue_pk):
    url = client._build_absolute_uri(f"/cases/?queue_id={queue_pk}&page=1")
    yield requests_mock.get(
        url=url,
        json={
            "results": {
                "queues": [],
                "cases": [],
                "filters": {
                    "gov_users": [],
                    "case_types": [],
                    "statuses": [],
                    "advice_types": [],
                },
            }
        },
    )
