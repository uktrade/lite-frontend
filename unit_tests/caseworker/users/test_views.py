import pytest
from django.urls import reverse
from core import client
from bs4 import BeautifulSoup
from core import client
from requests.exceptions import HTTPError


@pytest.fixture(autouse=True)
def default_feature_flags(settings):
    settings.FEATURE_MENTIONS_ENABLED = True


@pytest.mark.parametrize(
    "data, count",
    (
        (
            {
                "mentions": [
                    {
                        "case_queue_id": "f65fbf49-c14b-482b-833f-fe39bb26a51d",  # /PS-IGNORE
                        "case_id": "4966212d-5b52-4a6d-9e06-e589ab9dc221",  # /PS-IGNORE
                        "is_accessed": False,
                    }
                ]
            },
            1,
        ),
        (
            {
                "mentions": [
                    {
                        "case_queue_id": "f65fbf49-c14b-482b-833f-fe39bb26a51d",  # /PS-IGNORE
                        "case_id": "4966212d-5b52-4a6d-9e06-e589ab9dc221",  # /PS-IGNORE
                        "is_accessed": True,
                    },
                    {
                        "case_queue_id": "f65fbf49-c14b-482b-833f-fe39bb26a51d",  # /PS-IGNORE
                        "case_id": "4966212d-5b52-4a6d-9e06-e589ab9dc221",  # /PS-IGNORE
                        "is_accessed": False,
                    },
                    {
                        "case_queue_id": "f65fbf49-c14b-482b-833f-fe39bb26a51d",  # /PS-IGNORE
                        "case_id": "4966212d-5b52-4a6d-9e06-e589ab9dc221",  # /PS-IGNORE
                        "is_accessed": False,
                    },
                    {
                        "case_queue_id": "f65fbf49-c14b-482b-833f-fe39bb26a51d",  # /PS-IGNORE
                        "case_id": "4966212d-5b52-4a6d-9e06-e589ab9dc221",  # /PS-IGNORE
                        "is_accessed": False,
                    },
                ]
            },
            3,
        ),
    ),
)
def test_user_case_note_mention_count(data, count, authorized_client, requests_mock):
    requests_mock.get(
        client._build_absolute_uri("/cases/user-case-note-mentions/"),
        json=data,
    )

    url = reverse("users:user_case_note_mentions")
    response = authorized_client.get(url)
    assert response.status_code == 200
    assert response.context["NEW_MENTIONS_COUNT"] == count


def test_user_case_note_mention_count_error(authorized_client, requests_mock):
    data = {"mentions": []}
    requests_mock.get(
        client._build_absolute_uri("/cases/user-case-note-mentions/"),
        status_code=500,
        json=data,
    )

    url = reverse("users:user_case_note_mentions")
    with pytest.raises(HTTPError) as exc_info:
        response = authorized_client.get(url)
    exception = exc_info.value
    assert exception.response.status_code == 500


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
