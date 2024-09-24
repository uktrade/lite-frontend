import uuid

import pytest
from django.urls import reverse

from core import client
from core.exceptions import ServiceError


def mock_post_bookmark(requests_mock, code=201):
    url = client._build_absolute_uri("/bookmarks/")
    return requests_mock.post(
        url=url,
        status_code=code,
        json={},
    )


def mock_delete_bookmark(requests_mock, code=200):
    url = client._build_absolute_uri("/bookmarks/")
    return requests_mock.delete(
        url=url,
        status_code=code,
        json={},
    )


def mock_edit_bookmark(requests_mock, code=200):
    url = client._build_absolute_uri("/bookmarks/")
    return requests_mock.put(
        url=url,
        status_code=code,
        json={},
    )


def test_add_bookmark_ok(
    authorized_client,
    mock_queue,
    mock_countries,
    mock_queues_list,
    mock_cases_with_filter_data,
    requests_mock,
    gov_uk_user_id,
    mock_control_list_entries,
    mock_regime_entries,
):
    mock_post = mock_post_bookmark(requests_mock)
    url = reverse("bookmarks:add_bookmark")
    return_to_url = "http://return-to.com"
    response = authorized_client.post(
        url,
        data={
            "return_to": return_to_url,
            "countries": ["GB"],
            "case_officer": gov_uk_user_id,
            "finalised_to_0": "22",
            "finalised_to_1": "09",
            "finalised_to_2": "2002",
        },
    )
    posted_content = mock_post.last_request.json()

    assert response.status_code == 302
    assert response.url == return_to_url
    assert posted_content["name"].startswith("New unnamed filter")
    assert posted_content["user_id"] == gov_uk_user_id

    expected_filter = {"case_officer": gov_uk_user_id, "countries": ["GB"], "finalised_to": "22-09-2002"}
    assert posted_content["filter_json"] == expected_filter


@pytest.mark.parametrize("return_code", [400, 500])
def test_add_bookmark_fail(
    authorized_client,
    mock_queue,
    mock_queues_list,
    mock_countries,
    mock_cases_with_filter_data,
    requests_mock,
    gov_uk_user_id,
    return_code,
    mock_control_list_entries,
    mock_regime_entries,
):
    mock_post_bookmark(requests_mock, return_code)
    url = reverse("bookmarks:add_bookmark")
    return_to_url = "http://return-to.com"

    with pytest.raises(ServiceError) as ex:
        authorized_client.post(url, data={"return_to": return_to_url, "country": "GB", "case_officer": gov_uk_user_id})

    assert ex.value.status_code == return_code
    assert ex.value.user_message == "Unexpected error saving filter"


def test_delete_bookmark_ok(authorized_client, mock_queue, mock_cases_with_filter_data, requests_mock):
    bookmark_id = str(uuid.uuid4())
    mock_delete = mock_delete_bookmark(requests_mock)
    url = reverse("bookmarks:delete_bookmark")
    return_to_url = "http://return-to.com"
    response = authorized_client.post(url, data={"return_to": return_to_url, "id": bookmark_id, "submit": "Delete"})
    posted_content = mock_delete.last_request.json()

    assert response.status_code == 302
    assert response.url == return_to_url
    assert posted_content["id"] == bookmark_id


@pytest.mark.parametrize("return_code", [400, 500])
def test_delete_bookmark_fail(
    authorized_client, mock_queue, mock_cases_with_filter_data, requests_mock, gov_uk_user_id, return_code
):
    bookmark_id = str(uuid.uuid4())
    mock_delete_bookmark(requests_mock, return_code)
    url = reverse("bookmarks:delete_bookmark")
    return_to_url = "http://return-to.com"

    with pytest.raises(ServiceError) as ex:
        authorized_client.post(url, data={"return_to": return_to_url, "id": bookmark_id, "submit": "Delete"})

    assert ex.value.status_code == return_code
    assert ex.value.user_message == "Unexpected error deleting filter"


def test_edit_bookmark_ok(authorized_client, mock_queue, mock_cases_with_filter_data, requests_mock):
    bookmark_id = str(uuid.uuid4())
    mock_edit = mock_edit_bookmark(requests_mock)
    url = reverse("bookmarks:rename_bookmark")
    return_to_url = "http://return-to.com"
    response = authorized_client.post(
        url, data={"return_to": return_to_url, "id": bookmark_id, "submit": "Save", "name": "UK Cases"}
    )
    posted_content = mock_edit.last_request.json()

    assert response.status_code == 302
    assert response.url == return_to_url
    assert posted_content["id"] == bookmark_id
    assert posted_content["name"] == "UK Cases"


@pytest.mark.parametrize("return_code", [400, 500])
def test_edit_bookmark_fail(
    authorized_client, mock_queue, mock_cases_with_filter_data, requests_mock, gov_uk_user_id, return_code
):
    bookmark_id = str(uuid.uuid4())
    mock_edit_bookmark(requests_mock, return_code)
    url = reverse("bookmarks:rename_bookmark")
    return_to_url = "http://return-to.com"

    with pytest.raises(ServiceError) as ex:
        authorized_client.post(
            url, data={"return_to": return_to_url, "id": bookmark_id, "submit": "Save", "name": "UK Cases"}
        )

    assert ex.value.status_code == return_code
    assert ex.value.user_message == "Unexpected error editing filter name"
