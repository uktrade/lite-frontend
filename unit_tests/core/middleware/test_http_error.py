from requests import HTTPError
from requests.models import Response
from unittest import mock
from core.middleware import HttpErrorHandlerMiddleware
import pytest

import logging


def test_http_error_handler_non_http_error_exception(rf, mocker, caplog):
    get_response = mocker.MagicMock()
    http_error_handler = HttpErrorHandlerMiddleware(get_response)

    request = rf.get("/")
    not_http_error = Exception()
    assert http_error_handler.process_exception(request, not_http_error) is None
    assert not caplog.records


@mock.patch("core.middleware.error_page")
@pytest.mark.parametrize(
    "content, returned_value, error_log",
    (
        (b'{"errors": "this is an error"}', "Error Page", '{"errors": "this is an error"}'),
        (b'{"error": "this is an error"}', None, '{"error": "this is an error"}'),
        (b'"this is an error"', None, '"this is an error"'),
        (b"this is an error", None, "this is an error"),
    ),
)
def test_http_error_handler_with_http_errors(mock_error_page, rf, mocker, caplog, content, returned_value, error_log):
    get_response = mocker.MagicMock()
    http_error_handler = HttpErrorHandlerMiddleware(get_response)

    mock_error_page.return_value = "Error Page"

    response = Response()
    response.status_code = 400
    response._content = content

    http_error = HTTPError(response=response)
    request = rf.get("/")
    caplog.set_level(logging.INFO)
    assert http_error_handler.process_exception(request, http_error) is returned_value
    assert ("INFO", error_log) in [(r.levelname, r.msg) for r in caplog.records]
