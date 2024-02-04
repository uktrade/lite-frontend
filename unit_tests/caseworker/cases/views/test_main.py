import uuid

from django.http import StreamingHttpResponse
from django.urls import reverse

from core import client


def test_document_download(
    authorized_client,
    mock_queue,
    queue_pk,
    data_standard_case,
    requests_mock,
    mock_s3_files,
):
    mock_s3_files(
        ("123", b"test", {"ContentType": "application/doc"}),
    )

    document_id = uuid.uuid4()
    requests_mock.get(
        client._build_absolute_uri(f"/documents/{document_id}"),
        json={
            "document": {
                "s3_key": "123",
                "name": "fakefile.doc",
            },
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
