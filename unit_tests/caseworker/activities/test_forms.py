import pytest

from caseworker.activities import forms
import requests
from core import client


@pytest.fixture
def mock_request(rf, authorized_client):
    request = rf.get("/")
    request.session = authorized_client.session
    request.requests_session = requests.Session()
    yield request


@pytest.mark.parametrize(
    "data, valid_status, error_message",
    (
        ({"text": ""}, False, {"text": ["Case Notes are Required"]}),
        ({"text": "this is text", "is_urgent": False}, True, {}),
        ({"text": "this is text", "mentions": ["1f288b81-2c26-439f-ac32-2a43c8b1a5cb"]}, True, {}),  # /PS-IGNORE
        (
            {"text": "this is text", "mentions": ["Invalid User"], "is_urgent": False},
            False,
            {"mentions": ["Select a valid choice. Invalid User is not one of the available choices."]},
        ),
        (
            {
                "text": "this is text",
                "mentions": ["1f288b81-2c26-439f-ac32-2a43c8b1a5cb"],  # /PS-IGNORE
                "is_urgent": False,
            },
            True,
            {},
        ),
        (
            {
                "text": "this is text",
                "mentions": [
                    "1f288b81-2c26-439f-ac32-2a43c8b1a5cb",  # /PS-IGNORE
                    "d832b2fb-e128-4367-9cfe-6f6d37d270f7",  # /PS-IGNORE
                ],
                "is_urgent": False,
            },
            True,
            {},
        ),
        (
            {
                "text": "this is text",
                "mentions": [
                    "1f288b81-2c26-439f-ac32-2a43c8b1a5cb",  # /PS-IGNORE
                    "d832b2fb-e128-4367-9cfe-6f6d37d270f7",  # /PS-IGNORE
                ],
                "is_urgent": True,
            },
            True,
            {},
        ),
    ),
)
def test_notes_and_timeline(data, valid_status, error_message, mock_request, requests_mock, mock_gov_users):
    url = "/gov-users/"
    json = {
        "results": mock_gov_users,
    }
    requests_mock.get(client._build_absolute_uri(url), json=json)
    form = forms.NotesAndTimelineForm(data=data, request=mock_request)
    assert form.is_valid() == valid_status
    assert form.errors == error_message


@pytest.mark.parametrize(
    "data, expected",
    (
        ({"text": "this is text", "mentions": ["1f288b81-2c26-439f-ac32-2a43c8b1a5cb"]}, False),  # /PS-IGNORE
        (
            {
                "text": "this is text",
                "mentions": ["1f288b81-2c26-439f-ac32-2a43c8b1a5cb"],  # /PS-IGNORE
                "is_urgent": False,
            },
            False,
        ),
        (
            {
                "text": "this is text",
                "mentions": [
                    "1f288b81-2c26-439f-ac32-2a43c8b1a5cb",  # /PS-IGNORE
                    "d832b2fb-e128-4367-9cfe-6f6d37d270f7",  # /PS-IGNORE
                ],
                "is_urgent": False,
            },
            False,
        ),
        (
            {
                "text": "this is text",
                "mentions": [
                    "1f288b81-2c26-439f-ac32-2a43c8b1a5cb",  # /PS-IGNORE
                    "d832b2fb-e128-4367-9cfe-6f6d37d270f7",  # /PS-IGNORE
                ],  # /PS-IGNORE
                "is_urgent": True,
            },
            True,
        ),
    ),
)
def test_notes_and_timeline_clean_is_urgent(data, expected, mock_request, requests_mock, mock_gov_users):
    url = "/gov-users/"
    json = {
        "results": mock_gov_users,
    }
    requests_mock.get(client._build_absolute_uri(url), json=json)
    form = forms.NotesAndTimelineForm(data=data, request=mock_request)
    form.is_valid()
    assert form.cleaned_data["is_urgent"] == expected


@pytest.mark.parametrize(
    "data, expected",
    (
        (
            {"text": "this is text", "mentions": ["1f288b81-2c26-439f-ac32-2a43c8b1a5cb"]},  # /PS-IGNORE
            [{"user": "1f288b81-2c26-439f-ac32-2a43c8b1a5cb"}],  # /PS-IGNORE
        ),
        (
            {
                "text": "this is text",
                "mentions": ["1f288b81-2c26-439f-ac32-2a43c8b1a5cb"],  # /PS-IGNORE
                "is_urgent": False,
            },
            [{"user": "1f288b81-2c26-439f-ac32-2a43c8b1a5cb"}],  # /PS-IGNORE
        ),
        (
            {
                "text": "this is text",
                "mentions": [
                    "1f288b81-2c26-439f-ac32-2a43c8b1a5cb",  # /PS-IGNORE
                    "d832b2fb-e128-4367-9cfe-6f6d37d270f7",  # /PS-IGNORE
                ],
                "is_urgent": False,
            },
            [
                {"user": "1f288b81-2c26-439f-ac32-2a43c8b1a5cb"},  # /PS-IGNORE
                {"user": "d832b2fb-e128-4367-9cfe-6f6d37d270f7"},  # /PS-IGNORE
            ],
        ),
    ),
)
def test_notes_and_timeline_clean_mentions(data, expected, mock_request, requests_mock, mock_gov_users):
    url = "/gov-users/"
    json = {
        "results": mock_gov_users,
    }
    requests_mock.get(client._build_absolute_uri(url), json=json)
    form = forms.NotesAndTimelineForm(data=data, request=mock_request)
    form.is_valid()
    assert form.cleaned_data["mentions"] == expected
