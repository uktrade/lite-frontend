import pytest


BASE_ENTRIES_URL = "/static/regimes/entries/{}/"


@pytest.fixture
def mock_wassenaar_entries_get(requests_mock, wassenaar_regime_entry):
    requests_mock.get(
        BASE_ENTRIES_URL.format("wassenaar"),
        json=[wassenaar_regime_entry],
    )


@pytest.fixture
def mock_mtcr_entries_get(requests_mock, mtcr_regime_entry):
    requests_mock.get(
        BASE_ENTRIES_URL.format("mtcr"),
        json=[mtcr_regime_entry],
    )


@pytest.fixture
def mock_nsg_entries_get(requests_mock, nsg_regime_entry):
    requests_mock.get(
        BASE_ENTRIES_URL.format("nsg"),
        json=[nsg_regime_entry],
    )


@pytest.fixture
def mock_cwc_entries_get(requests_mock, cwc_regime_entry):
    requests_mock.get(
        BASE_ENTRIES_URL.format("cwc"),
        json=[cwc_regime_entry],
    )


@pytest.fixture
def mock_ag_entries_get(requests_mock, ag_regime_entry):
    requests_mock.get(
        BASE_ENTRIES_URL.format("ag"),
        json=[ag_regime_entry],
    )
