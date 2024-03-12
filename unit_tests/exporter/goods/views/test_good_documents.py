import io
import uuid

from pytest_django.asserts import assertContains

from django.http import StreamingHttpResponse
from django.urls import reverse

from core import client


def test_document_download(authorized_client, requests_mock):
    good_pk = uuid.uuid4()
    file_pk = uuid.uuid4()

    goods_document_url = client._build_absolute_uri(f"/goods/{good_pk}/documents/{file_pk}/")
    requests_mock.get(
        goods_document_url,
        json={
            "document": {
                "id": str(uuid.uuid4()),
            },
        },
    )

    goods_document_stream_url = client._build_absolute_uri(f"/goods/{good_pk}/documents/{file_pk}/stream/")
    requests_mock.get(
        goods_document_stream_url,
        body=io.BytesIO(b"test"),
        headers={
            "Content-Type": "application/doc",
            "Content-Disposition": 'attachment; filename="fakefile.doc"',
        },
    )

    url = reverse(
        "goods:document",
        kwargs={
            "pk": good_pk,
            "file_pk": file_pk,
        },
    )
    response = authorized_client.get(url)

    assert response.status_code == 200
    assert isinstance(response, StreamingHttpResponse)
    assert response.headers["Content-Type"] == "application/doc"
    assert response.headers["Content-Disposition"] == 'attachment; filename="fakefile.doc"'
    assert b"".join(response.streaming_content) == b"test"


def test_document_download_no_document_response(authorized_client, requests_mock):
    good_pk = uuid.uuid4()
    file_pk = uuid.uuid4()

    goods_document_url = client._build_absolute_uri(f"/goods/{good_pk}/documents/{file_pk}/")
    requests_mock.get(
        goods_document_url,
        status_code=404,
    )

    url = reverse(
        "goods:document",
        kwargs={
            "pk": good_pk,
            "file_pk": file_pk,
        },
    )
    response = authorized_client.get(url)
    assert response.status_code == 404


def test_document_download_no_stream_response(authorized_client, requests_mock):
    good_pk = uuid.uuid4()
    file_pk = uuid.uuid4()

    goods_document_url = client._build_absolute_uri(f"/goods/{good_pk}/documents/{file_pk}/")
    requests_mock.get(
        goods_document_url,
        json={
            "document": {
                "id": str(uuid.uuid4()),
            },
        },
    )

    goods_document_stream_url = client._build_absolute_uri(f"/goods/{good_pk}/documents/{file_pk}/stream/")
    requests_mock.get(
        goods_document_stream_url,
        status_code=404,
    )

    url = reverse(
        "goods:document",
        kwargs={
            "pk": good_pk,
            "file_pk": file_pk,
        },
    )

    response = authorized_client.get(url)
    assert response.status_code == 200
    assertContains(response, "Unexpected error downloading document")
