from django.urls import reverse
from core import client


def test_user_case_note_mentions(authorized_client, requests_mock):
    mentions_data = {
        "mentions": [
            {
                "case_queue_id": "f65fbf49-c14b-482b-833f-fe39bb26a51d",  # /PS-IGNORE
                "case_id": "4966212d-5b52-4a6d-9e06-e589ab9dc221",  # /PS-IGNORE
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
