import pytest
from django.urls import reverse


@pytest.fixture(autouse=True)
def setup(
    mock_queue,
    mock_cases_with_filter_data,
    mock_cases_head,
):
    pass


def test_no_bookmarks_present(authorized_client, mock_no_bookmarks):
    url = reverse("core:index")
    response = authorized_client.get(url)
    context = response.context
    assert context["return_to"] == url
    assert context["bookmarks"] == {"user": []}


def test_failed_bookmarks_displays_no_bookmarks(authorized_client, mock_failed_bookmarks_call):
    url = reverse("core:index")
    response = authorized_client.get(url)
    context = response.context
    assert context["return_to"] == url
    assert context["bookmarks"] == {"user": []}


def test_bookmarks_present(authorized_client, mock_bookmarks, gov_uk_user_id):
    url = reverse("core:index")
    response = authorized_client.get(url)
    context = response.context
    first = context["bookmarks"]["user"][0]
    second = context["bookmarks"]["user"][1]

    assert context["return_to"] == url

    assert first["name"] == "Bookmark1"
    assert first["filter_json"] == '{"country":"DE"}'
    assert first["description"] == "Country: DE"

    assert second["name"] == "Bookmark1"
    assert second["filter_json"] == f'{{"case_officer":"{gov_uk_user_id}"}}'
    assert second["description"] == "Case officer: John Smith"
