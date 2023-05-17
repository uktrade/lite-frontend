import pytest

from caseworker.activities import forms
import requests
from core import client
from django.conf import settings


@pytest.fixture
def mock_request(rf, authorized_client):
    request = rf.get("/")
    request.session = authorized_client.session
    request.requests_session = requests.Session()
    yield request


@pytest.fixture()
def mock_post_site(requests_mock, organisation_pk):
    url = client._build_absolute_uri(f"/organisations/{organisation_pk}/sites/")
    yield requests_mock.post(
        url=url, json={"site": {"name": "Test site", "id": "00000000-0000-0000-0000-000000000001"}}
    )


@pytest.fixture()
def mock_validate_site(requests_mock, organisation_pk):
    url = client._build_absolute_uri(f"/organisations/{organisation_pk}/sites/")
    yield requests_mock.post(url=url, json={})


@pytest.mark.parametrize(
    "data, valid_status",
    (
        ({"text": ""}, False),
        ({"text": "this is text", "is_urgent": False}, True),
        ({"text": "this is text", "mentions": ["1f288b81-2c26-439f-ac32-2a43c8b1a5cb"]}, True),  # /PS-IGNORE
        (
            {"text": "this is text", "mentions": ["1f288b81-2c26-439f-ac32-2a43c8b1a5cb"], "is_urgent": False},
            True,
        ),  # /PS-IGNORE
        (
            {
                "text": "this is text",
                "mentions": [
                    "1f288b81-2c26-439f-ac32-2a43c8b1a5cb",
                    "d832b2fb-e128-4367-9cfe-6f6d37d270f7",
                ],  # /PS-IGNORE
                "is_urgent": False,
            },
            True,
        ),
        (
            {
                "text": "this is text",
                "mentions": [
                    "1f288b81-2c26-439f-ac32-2a43c8b1a5cb",
                    "d832b2fb-e128-4367-9cfe-6f6d37d270f7",
                ],  # /PS-IGNORE
                "is_urgent": True,
            },
            True,
        ),
    ),
)
def test_notes_and_timeline(data, valid_status, mock_request, requests_mock, mock_gov_users):
    url = "/gov-users/"
    json = {
        "results": mock_gov_users,
    }
    requests_mock.get(client._build_absolute_uri(url), json=json)
    form = forms.NotesAndTimelineForm(data=data, request=mock_request)
    assert form.is_valid() == valid_status


@pytest.mark.parametrize(
    "data, expected",
    (
        ({"text": "this is text", "mentions": ["1f288b81-2c26-439f-ac32-2a43c8b1a5cb"]}, False),  # /PS-IGNORE
        (
            {"text": "this is text", "mentions": ["1f288b81-2c26-439f-ac32-2a43c8b1a5cb"], "is_urgent": False},
            False,
        ),  # /PS-IGNORE
        (
            {
                "text": "this is text",
                "mentions": [
                    "1f288b81-2c26-439f-ac32-2a43c8b1a5cb",
                    "d832b2fb-e128-4367-9cfe-6f6d37d270f7",
                ],  # /PS-IGNORE
                "is_urgent": False,
            },
            False,
        ),
        (
            {
                "text": "this is text",
                "mentions": [
                    "1f288b81-2c26-439f-ac32-2a43c8b1a5cb",
                    "d832b2fb-e128-4367-9cfe-6f6d37d270f7",
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
                "mentions": ["1f288b81-2c26-439f-ac32-2a43c8b1a5cb"],
                "is_urgent": False,
            },  # /PS-IGNORE
            [{"user": "1f288b81-2c26-439f-ac32-2a43c8b1a5cb"}],  # /PS-IGNORE
        ),
        (
            {
                "text": "this is text",
                "mentions": [
                    "1f288b81-2c26-439f-ac32-2a43c8b1a5cb",
                    "d832b2fb-e128-4367-9cfe-6f6d37d270f7",
                ],  # /PS-IGNORE
                "is_urgent": False,
            },
            [
                {"user": "1f288b81-2c26-439f-ac32-2a43c8b1a5cb"},
                {"user": "d832b2fb-e128-4367-9cfe-6f6d37d270f7"},
            ],  # /PS-IGNORE
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
                "mentions": ["1f288b81-2c26-439f-ac32-2a43c8b1a5cb"],
                "is_urgent": False,
            },  # /PS-IGNORE
            [{"user": "1f288b81-2c26-439f-ac32-2a43c8b1a5cb"}],  # /PS-IGNORE
        ),
        (
            {
                "text": "this is text",
                "mentions": [
                    "1f288b81-2c26-439f-ac32-2a43c8b1a5cb",
                    "d832b2fb-e128-4367-9cfe-6f6d37d270f7",
                ],  # /PS-IGNORE
                "is_urgent": False,
            },
            [
                {"user": "1f288b81-2c26-439f-ac32-2a43c8b1a5cb"},
                {"user": "d832b2fb-e128-4367-9cfe-6f6d37d270f7"},
            ],  # /PS-IGNORE
        ),
    ),
)
def test_notes_and_timeline_feature_flag(data, expected, mock_request, requests_mock, mock_gov_users, settings):
    url = "/gov-users/"
    json = {
        "results": mock_gov_users,
    }
    requests_mock.get(client._build_absolute_uri(url), json=json)
    form = forms.NotesAndTimelineForm(data=data, request=mock_request)
    assert list(form.fields.keys()) == ["text", "mentions", "is_urgent"]
    settings.FEATURE_MENTIONS_ENABLED = False
    form = forms.NotesAndTimelineForm(data=data, request=mock_request)
    assert list(form.fields.keys()) == ["text"]
