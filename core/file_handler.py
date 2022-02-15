import magic

from django.conf import settings
from django.core.exceptions import PermissionDenied
from s3chunkuploader.file_handler import S3FileUploadHandler

from storages.backends.s3boto3 import S3Boto3StorageFile


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
                self.abort(PermissionDenied("Unsupported file type"))
        super().receive_data_chunk(raw_data, start)

    def file_complete(self, *args, **kwargs):
        """Override `file_complete` to ensure that all necessary attributes
        are set on the file object.

        Some frameworks, e.g. formtools' SessionWizardView will fall over
        if these attributes aren't present.
        """
        super().file_complete(*args, **kwargs)

        self.file = S3Boto3StorageFile(self.s3_key, "r", self.storage)
        self.file.original_name = self.file_name
        self.file.content_type = self.content_type
        self.file.charset = self.charset

        return self.file
