import boto3
import logging
import magic

from django.conf import settings
from django.core.files.uploadhandler import UploadFileException
from django.http import StreamingHttpResponse

from django_chunk_upload_handlers.s3 import S3FileUploadHandler


logger = logging.getLogger(__name__)


class S3Wrapper:
    """
    A wrapper around the S3 client ensuring only one client is instantiated and reused.
    """

    _s3_client = None

    @classmethod
    def get_client(cls):
        if not cls._s3_client:
            logger.debug("Instantiating S3 client")
            extra_kwargs = {}
            if settings.AWS_S3_ENDPOINT_URL:
                extra_kwargs["endpoint_url"] = settings.AWS_S3_ENDPOINT_URL

            cls._s3_client = boto3.client(
                "s3",
                aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
                region_name=settings.AWS_REGION,
                **extra_kwargs,
            )

        return cls._s3_client


def s3_client():
    """
    A handy method to get a reusable S3 client
    """
    return S3Wrapper.get_client()


class SafeS3FileUploadHandler(S3FileUploadHandler):
    """
    S3FileUploadHandler with mime-type validation.
    """

    ACCEPTED_FILE_UPLOAD_MIME_TYPES = settings.ACCEPTED_FILE_UPLOAD_MIME_TYPES

    def receive_data_chunk(self, raw_data, start):
        """
        Receive a single file chunk from the browser, validate the
        file type for the first chunk and leave the rest to super.
        """
        # For the first chunk
        if start == 0:
            mime = magic.from_buffer(raw_data, mime=True)
            if mime not in self.ACCEPTED_FILE_UPLOAD_MIME_TYPES:
                self.abort()
                raise UnacceptableMimeTypeError(f"Unsupported file type: {mime}")
        super().receive_data_chunk(raw_data, start)

    def file_complete(self, *args, **kwargs):
        """Override `file_complete` to ensure that all necessary attributes
        are set on the file object.

        Some frameworks, e.g. formtools' SessionWizardView will fall over
        if these attributes aren't present.
        """
        file = super().file_complete(*args, **kwargs)
        file.charset = self.charset

        return file


class UploadFailed(UploadFileException):
    pass


class UnacceptableMimeTypeError(UploadFailed):
    pass


def generate_file(result):
    for chunk in iter(lambda: result["Body"].read(settings.STREAMING_CHUNK_SIZE), b""):
        yield chunk


def download_document_from_s3(s3_key, original_file_name):
    s3_response = s3_client().get_object(Bucket=settings.AWS_STORAGE_BUCKET_NAME, Key=s3_key)
    _kwargs = {}
    if s3_response.get("ContentType"):
        _kwargs["content_type"] = s3_response["ContentType"]
    response = StreamingHttpResponse(generate_file(s3_response), **_kwargs)
    response["Content-Disposition"] = f'attachment; filename="{original_file_name}"'
    return response
