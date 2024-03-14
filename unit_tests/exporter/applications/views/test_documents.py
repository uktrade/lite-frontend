import io
import uuid

from http import HTTPStatus

from django.http import (
    HttpResponse,
    StreamingHttpResponse,
)
from django.urls import reverse

from pytest_django.asserts import assertContains

from core import client


def test_download_appeal_document(
    authorized_client,
    data_standard_case,
    requests_mock,
):
    appeal_pk = uuid.uuid4()
    document_pk = uuid.uuid4()
    document_api_url = client._build_absolute_uri(f"/appeals/{appeal_pk}/documents/{document_pk}/")
    requests_mock.get(
        document_api_url,
        json={
            "id": str(document_pk),
            "s3_key": "123",
            "name": "fakefile.doc",
            "safe": True,
        },
    )
    document_api_stream_url = client._build_absolute_uri(f"/appeals/{appeal_pk}/documents/{document_pk}/stream/")
    requests_mock.get(
        document_api_stream_url,
        body=io.BytesIO(b"test"),
        headers={
            "Content-Type": "application/doc",
            "Content-Disposition": 'attachment; filename="fakefile.doc"',
        },
    )

    url = reverse(
        "applications:appeal_document",
        kwargs={
            "case_pk": data_standard_case["case"]["id"],
            "appeal_pk": appeal_pk,
            "document_pk": document_pk,
        },
    )
    response = authorized_client.get(url)

    assert response.status_code == 200
    assert isinstance(response, StreamingHttpResponse)
    assert response.headers["Content-Type"] == "application/doc"
    assert response.headers["Content-Disposition"] == 'attachment; filename="fakefile.doc"'
    assert b"".join(response.streaming_content) == b"test"


def test_download_appeal_document_failure(
    authorized_client,
    data_standard_case,
    requests_mock,
):
    appeal_pk = uuid.uuid4()
    document_pk = uuid.uuid4()
    document_api_url = client._build_absolute_uri(f"/appeals/{appeal_pk}/documents/{document_pk}")
    requests_mock.get(
        document_api_url,
        json={},
        status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
    )

    url = reverse(
        "applications:appeal_document",
        kwargs={
            "case_pk": data_standard_case["case"]["id"],
            "appeal_pk": appeal_pk,
            "document_pk": document_pk,
        },
    )

    response = authorized_client.get(url)
    assert response.status_code == HTTPStatus.OK
    assert isinstance(response, HttpResponse)
    assertContains(response, "Unexpected error downloading appeal document")


def test_download_unsafe_appeal_document(
    authorized_client,
    data_standard_case,
    requests_mock,
):
    appeal_pk = uuid.uuid4()

    document_pk = uuid.uuid4()
    document_api_url = client._build_absolute_uri(f"/appeals/{appeal_pk}/documents/{document_pk}")
    requests_mock.get(
        document_api_url,
        json={
            "s3_key": "123",
            "name": "fakefile.doc",
            "safe": False,
        },
    )

    url = reverse(
        "applications:appeal_document",
        kwargs={
            "case_pk": data_standard_case["case"]["id"],
            "appeal_pk": appeal_pk,
            "document_pk": document_pk,
        },
    )
    response = authorized_client.get(url)

    assert response.status_code == HTTPStatus.OK
    assert isinstance(response, HttpResponse)
    assertContains(response, "We had an issue downloading your file. Try again later.")


def test_download_generated_document(
    authorized_client,
    data_standard_case,
    requests_mock,
    mock_s3_files,
):
    mock_s3_files(
        ("123", b"test", {"ContentType": "application/doc"}),
    )

    document_id = uuid.uuid4()
    document_api_url = client._build_absolute_uri(f"/documents/{document_id}")
    requests_mock.get(
        document_api_url,
        json={
            "document": {
                "s3_key": "123",
                "name": "fakefile.doc",
            },
        },
    )

    url = reverse(
        "applications:download_generated_document",
        kwargs={
            "case_pk": data_standard_case["case"]["id"],
            "document_pk": document_id,
        },
    )
    response = authorized_client.get(url)

    assert response.status_code == 200
    assert isinstance(response, StreamingHttpResponse)
    assert response.headers["Content-Type"] == "application/doc"
    assert response.headers["Content-Disposition"] == 'attachment; filename="fakefile.doc"'
    assert b"".join(response.streaming_content) == b"test"
