import magic
from boto3 import client as boto3_client
from django.conf import settings
from django.core.exceptions import PermissionDenied
from django_chunk_upload_handlers.s3 import (
    AWS_ACCESS_KEY_ID,
    AWS_REGION,
    AWS_S3_ENDPOINT_URL,
    AWS_SECRET_ACCESS_KEY,
    S3FileUploadHandler,
)

s3_client = boto3_client(
    "s3",
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    region_name=AWS_REGION,
    endpoint_url=AWS_S3_ENDPOINT_URL,
)


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
                raise UploadFailed(PermissionDenied("Unsupported file type"))
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


class UploadFailed(Exception):
    pass
