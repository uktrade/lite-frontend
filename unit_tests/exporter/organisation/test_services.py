import pytest
import requests

from core import client
from exporter.organisation import services


@pytest.fixture
def default_request(rf, client):
    request = rf.get("/")
    request.session = client.session
    request.requests_session = requests.Session()
    return request


def test_get_document_on_organisation(requests_mock, default_request):

    requests_mock.get(
        client._build_absolute_uri(f"/organisations/1/document/2/"),
    )

    response = services.get_document_on_organisation(request=default_request, organisation_id=1, document_id=2)

    assert response.status_code == 200
