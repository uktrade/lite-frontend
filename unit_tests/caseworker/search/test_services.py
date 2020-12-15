import pytest
import requests

from caseworker.search import services


@pytest.fixture
def default_request(rf, client):
    request = rf.get("/")
    request.session = client.session
    request.requests_session = requests.Session()
    return request
