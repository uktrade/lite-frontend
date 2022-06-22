from django.urls import reverse

import pytest


@pytest.fixture(autouse=True)
def setup(mock_queue, mock_case):
    yield


@pytest.mark.parametrize(
    "queue, is_all_cases_queue",
    (
        ("00000000-0000-0000-0000-000000000001", True),
        ("1b926457-5c9e-4916-8497-51886e51863a", False),
        ("c270b79b-370c-4c5e-b8b6-4d5210a58956", False),
    ),
)
def test_is_all_cases_queue(queue, is_all_cases_queue, authorized_client, data_standard_case):
    url = reverse(
        "cases:attach_documents",
        kwargs={"queue_pk": queue, "pk": data_standard_case["case"]["id"]},
    )
    resp = authorized_client.get(url)
    assert resp.context.get("is_all_cases_queue") == is_all_cases_queue
