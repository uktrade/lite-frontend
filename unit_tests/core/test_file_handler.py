import os
import pytest

from django import forms
from django.http import HttpResponse
from django.urls import path, reverse
from django.views import View
from django.views.generic import FormView

from core.file_handler import (
    UnacceptableMimeTypeError,
    UnacceptableMimeTypeFile,
    s3_client,
    S3Wrapper,
    validate_mime_type,
)


TEST_FILES_PATH = os.path.join(os.path.dirname(__file__), "test_file_handler_files")


class FileForm(forms.Form):
    upload_file = forms.FileField(
        validators=[
            validate_mime_type,
        ]
    )


class OKView(View):
    def get(self, request, *args, **kwargs):
        return HttpResponse("OK")


class FileUploadFormView(FormView):
    form_class = FileForm

    def form_invalid(self, form):
        response = HttpResponse("Not OK")
        response.form = form
        return response

    def get_success_url(self):
        return reverse("ok")


urlpatterns = [
    path("file-upload/", FileUploadFormView.as_view(), name="file-upload"),
    path("ok/", OKView.as_view(), name="ok"),
]


@pytest.fixture()
def file_upload_handler_settings(settings):
    settings.FILE_UPLOAD_HANDLERS = ["core.file_handler.SafeS3FileUploadHandler"]
    settings.ACCEPTED_FILE_UPLOAD_MIME_TYPES = "text/plain"
    settings.MIDDLEWARE = []


@pytest.mark.urls(__name__)
def test_valid_file(file_upload_handler_settings, client):
    with open(f"{TEST_FILES_PATH}/valid.txt", "rb") as f:
        response = client.post(reverse("file-upload"), {"upload_file": f})

    assert response.status_code == 302
    assert response.url == reverse("ok")


@pytest.mark.urls(__name__)
def test_invalid_file_type(file_upload_handler_settings, client):
    with open(f"{TEST_FILES_PATH}/invalid_type.zip", "rb") as f:
        response = client.post(reverse("file-upload"), {"upload_file": f})

    assert not response.form.is_valid()
    assert response.form.errors == {"upload_file": ["The selected file must be a DOCX, DOC, PDF, PNG, JPEG or ODT"]}


@pytest.mark.urls(__name__)
def test_invalid_mime_type(file_upload_handler_settings, client):
    with open(f"{TEST_FILES_PATH}/invalid_mime.txt", "rb") as f:
        response = client.post(reverse("file-upload"), {"upload_file": f})

    assert not response.form.is_valid()
    assert response.form.errors == {"upload_file": ["The selected file must be a DOCX, DOC, PDF, PNG, JPEG or ODT"]}


@pytest.mark.parametrize("func_name", ["open", "chunks", "multiple_chunks", "__iter__", "__enter__", "obj"])
def test_unacceptable_mime_type_file_function_raises_errors(func_name):
    unacceptable_mime_file = UnacceptableMimeTypeFile("bad_file")

    with pytest.raises(UnacceptableMimeTypeError):
        func = getattr(unacceptable_mime_file, func_name)
        func()


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
