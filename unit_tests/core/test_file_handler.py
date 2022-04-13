from unittest import mock
from os import path

import pytest
from core.file_handler import SafeS3FileUploadHandler, UploadFailed


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
        with pytest.raises(UploadFailed, match="Unsupported file type: application/zip"):
            mock_handler.receive_data_chunk(content, 0)


def test_invalid_file_mime_type_upload(mock_handler):
    with open(f"{TEST_FILES_PATH}/invalid_mime.txt", "rb") as f:
        content = f.read()
        with pytest.raises(UploadFailed, match="Unsupported file type: application/zip"):
            mock_handler.receive_data_chunk(content, 0)
