import pytest


@pytest.fixture
def mock_wassenaar_entries_get(requests_mock):
    requests_mock.get(
        "/static/regimes/wassenaar/entries/",
        json=[
            {
                "pk": "d73d0273-ef94-4951-9c51-c291eba949a0",
                "name": "wassenaar-1",
                "shortened_name": "w-1",
                "subsection": {
                    "pk": "a67b1acd-0578-4b83-af66-36ac56f00296",
                    "name": "Wassenaar Arrangement",
                    "regime": {
                        "pk": "66e5fc8d-67c7-4a5a-9d11-2eb8dbc57f7d",
                        "name": "WASSENAAR",
                    },
                },
            }
        ],
    )


@pytest.fixture
def mock_mtcr_entries_get(requests_mock):
    requests_mock.get(
        "/static/regimes/mtcr/entries/",
        json=[
            {
                "pk": "c760976f-fd14-4356-9f23-f6eaf084475d",
                "name": "mtcr-1",
                "subsection": {
                    "pk": "e529df3d-d471-49be-94d7-7a4e5835df90",
                    "name": "MTCR Category 1",
                    "regime": {
                        "pk": "b1c1f990-a7be-4bc8-9292-a8b5ea25c0dd",
                        "name": "MTCR",
                    },
                },
            }
        ],
    )
