from django.urls import reverse
from bs4 import BeautifulSoup

from core import client


def test_user_case_note_mentions(authorized_client, requests_mock):
    mentions_data = {
        "mentions": [
            {
                "case_queue_id": "f65fbf49-c14b-482b-833f-fe39bb26a51d",  # /PS-IGNORE
                "case_id": "4966212d-5b52-4a6d-9e06-e589ab9dc221",  # /PS-IGNORE
                "id": "f65fbf49-c14b-482b-833f-hdkwhdke79",  # /PS-IGNORE
                "is_accessed": True,
                "user": {"id": 123},
            }
        ]
    }
    requests_mock.get(
        client._build_absolute_uri("/cases/user-case-note-mentions/"),
        json=mentions_data,
    )

    url = reverse("users:user_case_note_mentions")
    response = authorized_client.get(url)

    assert response.status_code == 200
    assert response.context["user_mentions"] == mentions_data

    soup = BeautifulSoup(response.content, "html.parser")
    assert soup.find("table", {"class": "govuk-table"}).find("tr", {"id": "mentions-row-1"})


def test_user_case_note_mentions_update_is_accessed(authorized_client, requests_mock):
    mentions_data = {
        "mentions": [
            {
                "case_queue_id": "f65fbf49-c14b-482b-833f-fe39bb26a51d",  # /PS-IGNORE
                "case_id": "4966212d-5b52-4a6d-9e06-e589ab9dc221",  # /PS-IGNORE
                "id": "f65fbf49-c14b-482b-833f-hdkwhdke79",  # /PS-IGNORE
                "is_accessed": False,
                "user": {"id": 123},
            }
        ]
    }
    requests_mock.get(
        client._build_absolute_uri("/cases/user-case-note-mentions/"),
        json=mentions_data,
    )

    mock_case_note_mention_update = requests_mock.put(client._build_absolute_uri("/cases/case-note-mentions/"), json={})

    url = reverse("users:user_case_note_mentions")
    response = authorized_client.get(url)

    assert response.status_code == 200
    assert mock_case_note_mention_update.called_once
    last_request = mock_case_note_mention_update.last_request
    assert last_request.json() == [{"id": "f65fbf49-c14b-482b-833f-hdkwhdke79", "is_accessed": True}]
