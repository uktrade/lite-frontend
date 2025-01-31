from core.middleware import UploadFailedMiddleware
from core.file_handler import UploadFailed


def test_upload_failed_middleware_general_exception(rf, mocker):
    get_response = mocker.MagicMock()
    upload_failed_middleware = UploadFailedMiddleware(get_response)
    request = rf.get("/")
    not_file_upload_exception = Exception()

    assert upload_failed_middleware.process_exception(request, not_file_upload_exception) is None


def test_upload_failed_middleware_upload_failed_exception(rf, mocker, beautiful_soup):
    get_response = mocker.MagicMock()
    upload_failed_middleware = UploadFailedMiddleware(get_response)
    request = rf.get("/")
    not_file_upload_exception = UploadFailed()

    error_page_reponse = upload_failed_middleware.process_exception(request, not_file_upload_exception)
    soup = beautiful_soup(error_page_reponse.content)

    assert "An error occurred" in soup.title.text.strip()
