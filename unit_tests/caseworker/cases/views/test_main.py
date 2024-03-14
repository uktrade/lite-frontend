import io
import pytest
import uuid

from django.http import StreamingHttpResponse
from django.urls import reverse

from core import client
from core.exceptions import ServiceError


def test_document_download(
    authorized_client,
    mock_queue,
    queue_pk,
    data_standard_case,
    requests_mock,
):
    document_id = uuid.uuid4()
    requests_mock.get(
        url=client._build_absolute_uri(f"/documents/stream/{document_id}/"),
        body=io.BytesIO(b"test"),
        headers={
            "Content-Type": "application/doc",
            "Content-Disposition": 'attachment; filename="fakefile.doc"',
        },
    )

    url = reverse(
        "cases:document",
        kwargs={
            "queue_pk": queue_pk,
            "pk": data_standard_case["case"]["id"],
            "file_pk": document_id,
        },
    )
    response = authorized_client.get(url)

    assert response.status_code == 200
    assert isinstance(response, StreamingHttpResponse)
    assert response.headers["Content-Type"] == "application/doc"
    assert response.headers["Content-Disposition"] == 'attachment; filename="fakefile.doc"'
    assert b"".join(response.streaming_content) == b"test"


def test_document_download_no_response(
    authorized_client,
    mock_queue,
    queue_pk,
    data_standard_case,
    requests_mock,
):
    document_id = uuid.uuid4()
    requests_mock.get(
        url=client._build_absolute_uri(f"/documents/stream/{document_id}/"),
        status_code=404,
    )

    url = reverse(
        "cases:document",
        kwargs={
            "queue_pk": queue_pk,
            "pk": data_standard_case["case"]["id"],
            "file_pk": document_id,
        },
    )

    with pytest.raises(ServiceError) as ex:
        authorized_client.get(url)

    assert ex.value.status_code == 404
    assert ex.value.user_message == "Unexpected error downloading document"
