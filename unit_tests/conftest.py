import pytest

from core import client


@pytest.fixture
def data_control_list_entries():
    # in relity there are around 3000 CLCs
    return {
        "control_list_entries": [
            {"rating": "ML1", "text": "Smooth-bore weapons with a calibre of less than 20mm, other firearms..."},
            {"rating": "ML1a", "text": "Rifles and combination guns, handguns, machine, sub-machine and volley guns"},
        ]
    }


@pytest.fixture
def mock_control_list_entries(requests_mock, data_control_list_entries):
    url = client._build_absolute_uri("/static/control-list-entries/")
    yield requests_mock.get(url=url, json=data_control_list_entries)
