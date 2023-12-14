import pytest
from django.urls import reverse

from core import client

from core import client


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


@pytest.fixture
def mock_good_precedent_endpoint_empty(requests_mock, data_standard_case, data_queue):
    case_id = data_standard_case["case"]["id"]

    results = []

    precedents_url = client._build_absolute_uri(f"/cases/{case_id}/good-precedents/")
    requests_mock.get(
        precedents_url,
        json={"results": results},
    )


@pytest.fixture
def api_make_assessment_url(data_standard_case):
    return client._build_absolute_uri(f"/assessments/make-assessments/{data_standard_case['case']['id']}/")


@pytest.fixture
def tau_assessment_url(data_standard_case):
    return reverse(
        "cases:tau:home",
        kwargs={"queue_pk": "1b926457-5c9e-4916-8497-51886e51863a", "pk": data_standard_case["case"]["id"]},
    )


@pytest.fixture
def mock_assessment_put(requests_mock, data_standard_case):
    return requests_mock.put(
        client._build_absolute_uri(f"/assessments/make-assessments/{data_standard_case['case']['id']}"), json={}
    )
