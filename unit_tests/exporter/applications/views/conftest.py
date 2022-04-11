import pytest
from core import client


@pytest.fixture
def mock_good_get(requests_mock, data_standard_case):
    good = data_standard_case["case"]["data"]["goods"][0]
    url = client._build_absolute_uri(f'/goods/{good["good"]["id"]}/')
    yield requests_mock.get(url=url, json=good)


@pytest.fixture
def mock_good_put(requests_mock, data_standard_case):
    good = data_standard_case["case"]["data"]["goods"][0]["good"]
    url = client._build_absolute_uri(f'/goods/{good["id"]}/')
    yield requests_mock.put(url=url, json={})


@pytest.fixture
def mock_control_list_entries_get(requests_mock):
    url = client._build_absolute_uri(f"/static/control-list-entries/")
    yield requests_mock.get(url=url, json={"control_list_entries": [{"rating": "ML1a"}, {"rating": "ML22b"}]})


@pytest.fixture
def pv_gradings(requests_mock):
    requests_mock.get(
        "/static/private-venture-gradings/v2/",
        json={"pv_gradings": [{"official": "Official"}, {"restricted": "Restricted"}]},
    )
