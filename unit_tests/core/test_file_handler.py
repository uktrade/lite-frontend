import pytest

from unittest import mock
from os import path

from django.core.files.uploadhandler import UploadFileException

from core.file_handler import (
    s3_client,
    SafeS3FileUploadHandler,
    S3Wrapper,
    UnacceptableMimeTypeError,
)


TEST_FILES_PATH = path.join(path.dirname(__file__), "test_file_handler_files")


@pytest.fixture
def mock_handler():
    with mock.patch("django_chunk_upload_handlers.s3.boto3_client"):
        handler = SafeS3FileUploadHandler()
        handler.new_file(field_name="test", file_name="test", content_type="test/test", content_length=0)
        handler.file = mock.Mock()
        handler.client = mock.Mock()
        handler.executor = mock.Mock()
        handler.bucket_name = "test"
        handler.s3_key = "test"
        handler.upload_id = "test"
        yield handler


def test_valid_file_upload(mock_handler):
    with open(f"{TEST_FILES_PATH}/valid.txt", "rb") as f:
        content = f.read()
        mock_handler.abort = mock.Mock()
        mock_handler.receive_data_chunk(content, 0)
        mock_handler.abort.assert_not_called()
        # set start to be anything but 0
        mock_handler.receive_data_chunk(content, 1)
        mock_handler.abort.assert_not_called()


def test_invalid_file_type_upload(mock_handler):
    with open(f"{TEST_FILES_PATH}/invalid_type.zip", "rb") as f:
        content = f.read()
        mock_handler.abort = mock.Mock()
        with pytest.raises(UnacceptableMimeTypeError, match="Unsupported file type: application/zip") as e:
            mock_handler.receive_data_chunk(content, 0)
        assert isinstance(e.value, UploadFileException)
        mock_handler.abort.assert_called_once()


def test_invalid_file_mime_type_upload(mock_handler):
    with open(f"{TEST_FILES_PATH}/invalid_mime.txt", "rb") as f:
        content = f.read()
        mock_handler.abort = mock.Mock()
        with pytest.raises(UnacceptableMimeTypeError, match="Unsupported file type: application/zip") as e:
            mock_handler.receive_data_chunk(content, 0)
        assert isinstance(e.value, UploadFileException)
        mock_handler.abort.assert_called_once()


def test_s3_wrapper_get_client(settings, mocker):
    settings.AWS_ACCESS_KEY_ID = "aws-access-key-id"
    settings.AWS_SECRET_ACCESS_KEY = "aws-secret-access-key"  # noqa: S105
    settings.AWS_REGION = "aws-region"
    settings.AWS_S3_ENDPOINT_URL = None

    S3Wrapper._s3_client = None

    mock_boto3 = mocker.patch("core.file_handler.boto3")

    client = s3_client()

    mock_boto3.client.assert_called_with(
        "s3",
        aws_access_key_id="aws-access-key-id",
        aws_secret_access_key="aws-secret-access-key",  # noqa: S106
        region_name="aws-region",
    )

    assert client == mock_boto3.client()


def test_s3_wrapper_get_client_with_endpoint_url(settings, mocker):
    settings.AWS_ACCESS_KEY_ID = "aws-access-key-id"
    settings.AWS_SECRET_ACCESS_KEY = "aws-secret-access-key"  # noqa: S105
    settings.AWS_REGION = "aws-region"
    settings.AWS_S3_ENDPOINT_URL = "http://example.com"

    S3Wrapper._s3_client = None

    mock_boto3 = mocker.patch("core.file_handler.boto3")

    client = s3_client()

    mock_boto3.client.assert_called_with(
        "s3",
        aws_access_key_id="aws-access-key-id",
        aws_secret_access_key="aws-secret-access-key",  # noqa: S106
        region_name="aws-region",
        endpoint_url="http://example.com",
    )
    assert client == mock_boto3.client()


def test_s3_wrapper_get_client_acts_as_singleton(settings, mocker):
    settings.AWS_ACCESS_KEY_ID = "aws-access-key-id"
    settings.AWS_SECRET_ACCESS_KEY = "aws-secret-access-key"  # noqa: S105
    settings.AWS_REGION = "aws-region"
    settings.AWS_S3_ENDPOINT_URL = "http://example.com"

    S3Wrapper._s3_client = None

    mock_boto3 = mocker.patch("core.file_handler.boto3")

    client = s3_client()
    mock_boto3.client.assert_called_with(
        "s3",
        aws_access_key_id="aws-access-key-id",
        aws_secret_access_key="aws-secret-access-key",  # noqa: S106
        region_name="aws-region",
        endpoint_url="http://example.com",
    )

    new_client = s3_client()
    mock_boto3.client.assert_called_once()
    assert client == new_client
