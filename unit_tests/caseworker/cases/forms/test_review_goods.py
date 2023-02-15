import pytest
import requests

from caseworker.core.services import get_control_list_entries


@pytest.fixture
def control_list_entries(mock_control_list_entries, rf, client):
    request = rf.get("/")
    request.session = client.session
    request.requests_session = requests.Session()
    data = get_control_list_entries(request, convert_to_options=True)
    return [(item.value, item.key) for item in data]
