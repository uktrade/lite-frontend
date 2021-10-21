import pytest

from django.urls import reverse


@pytest.fixture(autouse=True)
def setup(mock_queue, mock_case, mock_denial_reasons, mock_post_refusal_advice):
    yield


@pytest.fixture
def url(data_queue, data_standard_case):
    return reverse("cases:refuse_all", kwargs={"queue_pk": data_queue["id"], "pk": data_standard_case["case"]["id"]})


def test_refuse_all_get(authorized_client, url):
    response = authorized_client.get(url)
    assert response.status_code == 200


@pytest.mark.parametrize(
    "denial_reasons, refusal_reasons, expected_status_code",
    [
        # Valid form
        (["1"], "test", 302),
        # Valid form with 2 denial_reasons
        (["1", "1a"], "test", 302),
        # Invalid form - missing denial_reasons
        ([], "test", 200),
        # Invalid form - missing refusal_reasons
        (["1"], "", 200),
        # Invalid form - missing denial_reasons & refusal_reasons
        ([], "", 200),
    ],
)
def test_refuse_all_post(authorized_client, url, denial_reasons, refusal_reasons, expected_status_code):
    response = authorized_client.post(url, data={"denial_reasons": denial_reasons, "refusal_reasons": refusal_reasons})
    assert response.status_code == expected_status_code
