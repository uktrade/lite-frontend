import uuid

from django.urls import reverse

from core import client


def test_matching_denials(authorized_client, requests_mock, mock_case, queue_pk, open_case_pk):

    requests_mock.post(f"/applications/{open_case_pk}/denial-matches/")

    url = reverse("cases:matching-denials", kwargs={"category": "partial", "pk": open_case_pk, "queue_pk": queue_pk})
    data = {"objects": ["1", "2", "3"]}

    response = authorized_client.post(url, data)

    assert response.status_code == 302
    assert response.url == reverse("cases:case", kwargs={"queue_pk": queue_pk, "pk": open_case_pk})

    assert requests_mock.request_history[0].json() == [
        {"application": open_case_pk, "denial": "1", "category": "partial"},
        {"application": open_case_pk, "denial": "2", "category": "partial"},
        {"application": open_case_pk, "denial": "3", "category": "partial"},
    ]


def test_remove_matching_denials(authorized_client, requests_mock, mock_queue, mock_case, queue_pk, open_case_pk):
    requests_mock.delete(client._build_absolute_uri(f"/applications/{open_case_pk}/denial-matches/"))

    url = reverse("cases:remove-matching-denials", kwargs={"pk": open_case_pk, "queue_pk": queue_pk})
    data = {"objects": ["1", "2", "3"]}

    response = authorized_client.post(url, data)

    assert response.status_code == 302
    assert response.url == reverse("cases:case", kwargs={"queue_pk": queue_pk, "pk": open_case_pk})

    assert requests_mock.request_history[0].json() == {"objects": ["1", "2", "3"]}


def test_remove_matching_sanctions_get(authorized_client, mock_case, open_case_pk, queue_pk, mock_queue):
    url = reverse("cases:remove-matching-sanctions", kwargs={"pk": open_case_pk, "queue_pk": queue_pk})

    response = authorized_client.get(f"{url}?objects=1")

    assert response.status_code == 200


def test_remove_matching_sanctions_submit(
    authorized_client, requests_mock, open_case_pk, queue_pk, mock_queue, mock_case
):
    requests_mock.patch(client._build_absolute_uri("/external-data/sanction/123/"))

    url = reverse("cases:remove-matching-sanctions", kwargs={"pk": open_case_pk, "queue_pk": queue_pk})

    response = authorized_client.post(f"{url}?objects=123", {"comment": "This is revoked"})

    assert response.status_code == 302
