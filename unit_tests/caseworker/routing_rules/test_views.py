import pytest

from django.urls import reverse


@pytest.fixture(autouse=True)
def setup(
    mock_routing_rules,
    mock_queues_list,
    mock_users_team_queues_list,
    mock_routing_rule_get,
    mock_team_queues_get,
    mock_case_types_get,
    mock_countries,
    mock_users_by_team_get,
):
    yield


def test_routing_rules_list(authorized_client):
    url = reverse("routing_rules:list")
    response = authorized_client.get(url)
    assert response.status_code == 200
