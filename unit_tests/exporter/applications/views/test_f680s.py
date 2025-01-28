import pytest

from bs4 import BeautifulSoup
from django.urls import reverse


@pytest.fixture
def authorized_client(authorized_client_factory, mock_exporter_user):
    return authorized_client_factory(mock_exporter_user["user"])


def test_apply_f680_view(authorized_client):
    url = reverse("f680:apply")

    response = authorized_client.get(url)
    assert response.status_code == 200

    soup = BeautifulSoup(response.content, "html.parser")
    assert "Name of the application" in soup.find("h1").text
