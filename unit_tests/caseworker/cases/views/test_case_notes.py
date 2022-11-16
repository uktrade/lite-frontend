import pytest

from pytest_django.asserts import assertContains

from django.urls import reverse


@pytest.fixture(autouse=True)
def setup(mock_queue):
    yield


@pytest.fixture
def case_notes_url(data_queue, data_standard_case):
    return reverse(
        "cases:case_notes",
        kwargs={
            "queue_pk": data_queue["id"],
            "pk": data_standard_case["case"]["id"],
        },
    )


@pytest.fixture
def mock_post_case_notes(requests_mock, data_standard_case):
    return requests_mock.post(
        f"/cases/{data_standard_case['case']['id']}/case-notes/",
        json={},
        status_code=201,
    )


def test_post_case_note(authorized_client, case_notes_url, mock_post_case_notes):
    response = authorized_client.post(
        case_notes_url,
        data={
            "text": "Note text",
        },
    )
    assert response.status_code == 302
    assert (
        response.url
        == "/queues/00000000-0000-0000-0000-000000000001/cases/8fb76bed-fd45-4293-95b8-eda9468aa254/activities/"
    )
    assert mock_post_case_notes.called
    assert mock_post_case_notes.last_request.json() == {"text": "Note text"}


def test_post_case_note_error(authorized_client, case_notes_url, data_standard_case, requests_mock):
    requests_mock.post(
        f"/cases/{data_standard_case['case']['id']}/case-notes/",
        json={
            "errors": {
                "text": ["Error with posting note"],
            }
        },
        status_code=400,
    )
    response = authorized_client.post(
        case_notes_url,
        data={
            "text": "Note text",
        },
    )
    assertContains(response, "Error with posting note")
