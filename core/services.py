from s3chunkuploader.file_handler import s3_client

from django.http import StreamingHttpResponse
from django.conf import settings


def generate_file(result):
    for chunk in iter(lambda: result["Body"].read(settings.STREAMING_CHUNK_SIZE), b""):
        yield chunk


def download_document_from_s3(s3_key, original_file_name):
    s3 = s3_client()
    s3_response = s3.get_object(Bucket=settings.AWS_STORAGE_BUCKET_NAME, Key=s3_key)
    _kwargs = {}
    if s3_response.get("ContentType"):
        _kwargs["content_type"] = s3_response["ContentType"]
    response = StreamingHttpResponse(generate_file(s3_response), **_kwargs)
    response["Content-Disposition"] = f'attachment; filename="{original_file_name}"'
    return response
