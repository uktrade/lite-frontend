# pragma: no cover

import concurrent.futures
import logging
import pathlib
import uuid

from concurrent.futures import wait

from boto3 import client as boto3_client

from storages.backends.s3boto3 import (
    S3Boto3Storage,
    S3Boto3StorageFile,
)

from django.conf import settings
from django.core.files.uploadhandler import FileUploadHandler
from django.utils import timezone

from django_chunk_upload_handlers.s3 import ThreadedS3ChunkUploader
from django_chunk_upload_handlers.clam_av import FileWithVirus, VirusFoundInFileException


logger = logging.getLogger(__name__)


# We should just be able to use this directly from django_chunk_upload_handlers
# but this library currently does some setup around Django settings at the
# module level which means we can't swap them out during tests.
# This rectifies that by loading the settings at runtime so that they can be
# correctly overriden.
class S3FileUploadHandler(FileUploadHandler):
    def new_file(self, *args, **kwargs):
        super().new_file(*args, **kwargs)

        S3_ROOT_DIRECTORY = getattr(settings, "CHUNK_UPLOADER_S3_ROOT_DIRECTORY", "")

        extension = pathlib.Path(self.file_name).suffix
        time_stamp = f'{timezone.now().strftime("%Y%m%d%H%M%S")}'
        self.new_file_name = f"{S3_ROOT_DIRECTORY}{self.file_name.replace(extension, '')}_{time_stamp}{extension}"

        extra_kwargs = {}
        if settings.AWS_S3_ENDPOINT_URL:
            extra_kwargs["endpoint_url"] = settings.AWS_S3_ENDPOINT_URL

        self.s3_client = boto3_client(
            "s3",
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
            region_name=settings.AWS_REGION,
            **extra_kwargs,
        )

        self.parts = []
        self.part_number = 1
        self.s3_key = f"chunk_upload_{str(uuid.uuid4())}"

        self.multipart = self.s3_client.create_multipart_upload(
            Bucket=settings.AWS_STORAGE_BUCKET_NAME,
            Key=self.s3_key,
            ContentType=self.content_type,
        )

        self.upload_id = self.multipart["UploadId"]
        self.executor = ThreadedS3ChunkUploader(
            self.s3_client,
            settings.AWS_STORAGE_BUCKET_NAME,
            key=self.s3_key,
            upload_id=self.upload_id,
        )

    def receive_data_chunk(self, raw_data, start):
        try:
            self.executor.add(raw_data)
        except Exception as exc:  # noqa
            logger.error("Aborting S3 upload", exc_info=exc)
            self.abort()

        return raw_data

    def file_complete(self, file_size):
        self.executor.add(None)

        # Wait for all threads to complete
        wait(self.executor.futures, return_when=concurrent.futures.ALL_COMPLETED)

        parts = self.executor.get_parts()

        self.s3_client.complete_multipart_upload(
            Bucket=settings.AWS_STORAGE_BUCKET_NAME,
            Key=self.s3_key,
            UploadId=self.upload_id,
            MultipartUpload={"Parts": parts},
        )

        self.s3_client.copy_object(
            Bucket=settings.AWS_STORAGE_BUCKET_NAME,
            CopySource=f"{settings.AWS_STORAGE_BUCKET_NAME}/{self.s3_key}",
            Key=self.new_file_name,
            ContentType=self.content_type,
        )

        self.s3_client.delete_object(
            Bucket=settings.AWS_STORAGE_BUCKET_NAME,
            Key=self.s3_key,
        )

        if "clam_av_results" in self.content_type_extra:
            for result in self.content_type_extra["clam_av_results"]:
                if result["file_name"] == self.file_name:
                    # Set AV headers
                    if result["av_passed"]:
                        self.s3_client.copy_object(
                            Bucket=settings.AWS_STORAGE_BUCKET_NAME,
                            CopySource=f"{settings.AWS_STORAGE_BUCKET_NAME}/{self.new_file_name}",
                            Key=self.new_file_name,
                            Metadata={
                                "av-scanned-at": result["scanned_at"].strftime("%Y-%m-%d %H:%M:%S"),
                                "av-passed": "True",
                            },
                            ContentType=self.content_type,
                            MetadataDirective="REPLACE",
                        )
                    else:
                        # Remove file with virus from S3
                        self.s3_client.delete_object(
                            Bucket=settings.AWS_STORAGE_BUCKET_NAME,
                            Key=self.new_file_name,
                        )

                        if settings.CHUNK_UPLOADER_RAISE_EXCEPTION_ON_VIRUS_FOUND:
                            raise VirusFoundInFileException()
                        else:
                            return FileWithVirus(field_name=self.field_name)

        storage = S3Boto3Storage()
        file = S3Boto3StorageFile(self.new_file_name, "rb", storage)
        file.content_type = self.content_type
        file.original_name = self.file_name

        file.file_size = file_size
        file.close()

        return file

    def abort(self):
        self.s3_client.abort_multipart_upload(
            Bucket=settings.AWS_STORAGE_BUCKET_NAME,
            Key=self.s3_key,
            UploadId=self.upload_id,
        )
