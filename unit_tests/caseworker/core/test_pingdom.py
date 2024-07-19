from django.urls import reverse


def test_pingdom_health_check(client):
    response = client.get(reverse("healthcheck-pingdom"))
    assert response.status_code == 200
