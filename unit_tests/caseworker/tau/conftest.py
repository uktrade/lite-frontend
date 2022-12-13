import pytest


@pytest.fixture
def mock_wassenaar_entries_get(requests_mock, wassenaar_regime_entry):
    requests_mock.get(
        "/static/regimes/entries/wassenaar/",
        json=[wassenaar_regime_entry],
    )


@pytest.fixture
def mock_mtcr_entries_get(requests_mock, mtcr_regime_entry):
    requests_mock.get(
        "/static/regimes/entries/mtcr/",
        json=[mtcr_regime_entry],
    )


@pytest.fixture
def mock_nsg_entries_get(requests_mock, nsg_regime_entry):
    requests_mock.get(
        "/static/regimes/entries/nsg/",
        json=[nsg_regime_entry],
    )


@pytest.fixture
def mock_cwc_entries_get(requests_mock, cwc_regime_entry):
    requests_mock.get(
        "/static/regimes/entries/cwc/",
        json=[cwc_regime_entry],
    )
