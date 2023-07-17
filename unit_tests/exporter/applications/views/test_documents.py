import uuid

from functools import reduce

from django.http import StreamingHttpResponse
from django.urls import reverse

from core import client


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
    assert reduce(lambda x, y: x + y, response.streaming_content) == b"test"
