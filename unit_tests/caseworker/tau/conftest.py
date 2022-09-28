import pytest


@pytest.fixture
def mock_mtcr_entries_get(requests_mock):
    requests_mock.get(
        "/static/regimes/mtcr/entries/",
        json=[{"pk": "c760976f-fd14-4356-9f23-f6eaf084475d", "name": "mtcr-1"}],
    )
