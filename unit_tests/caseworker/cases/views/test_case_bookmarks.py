import pytest
from django.urls import reverse


@pytest.fixture(autouse=True)
def setup(
    mock_queue,
    mock_cases_with_filter_data,
    mock_cases_head,
):
    pass


def test_no_bookmarks_present(
    authorized_client,
    mock_queues_list,
    mock_countries,
    mock_no_bookmarks,
    mock_control_list_entries,
    mock_regime_entries,
):
    url = reverse("core:index")
    response = authorized_client.get(url)
    context = response.context
    assert context["return_to"] == url
    assert context["bookmarks"] == {"user": []}


def test_failed_bookmarks_displays_no_bookmarks(
    authorized_client,
    mock_queues_list,
    mock_countries,
    mock_failed_bookmarks_call,
    mock_control_list_entries,
    mock_regime_entries,
):
    url = reverse("core:index")
    response = authorized_client.get(url)
    context = response.context
    assert context["return_to"] == url
    assert context["bookmarks"] == {"user": []}


def test_bookmarks_present(
    authorized_client,
    mock_bookmarks,
    mock_flags,
    mock_queues_list,
    mock_countries,
    gov_uk_user_id,
    mock_control_list_entries,
    mock_regime_entries,
):
    url = reverse("core:index")
    response = authorized_client.get(url)
    context = response.context
    first = context["bookmarks"]["user"][0]
    second = context["bookmarks"]["user"][1]
    third = context["bookmarks"]["user"][2]

    assert context["return_to"] == url

    assert first["name"] == "Bookmark1"
    assert first["filter_json"] == {"countries": ["DE"]}
    assert first["description"] == "Country: Germany"

    assert second["name"] == "Bookmark2"
    assert second["filter_json"] == {"case_officer": gov_uk_user_id}
    assert second["description"] == "Licensing Unit case officer: John Smith"

    assert third["name"] == "Bookmark3"
    assert third["filter_json"] == {
        "flags": ["64cbcf98-9beb-41ad-8f5d-276dee768990", "8f02e308-9861-4284-a7f0-f05495efce31"]
    }
    assert third["description"] == "Show only cases with these flags: AG Biological, AG Chemical"
    assert "flags=64cbcf98-9beb-41ad-8f5d-276dee768990" in third["url"]
    assert "flags=8f02e308-9861-4284-a7f0-f05495efce31" in third["url"]
