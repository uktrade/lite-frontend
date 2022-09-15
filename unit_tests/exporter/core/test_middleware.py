import pytest

from django.http import HttpResponse

from core.exceptions import ServiceError

from exporter.core.middleware import ServiceErrorHandler


def test_service_error_handler_non_service_error_exception(rf, mocker):
    get_response = mocker.MagicMock()
    service_error_handler = ServiceErrorHandler(get_response)

    request = rf.get("/")
    not_service_error = Exception()
    assert service_error_handler.process_exception(request, not_service_error) is None


def test_service_error_handler_service_error(rf, mocker, caplog, settings):
    settings.DEBUG = False
    get_response = mocker.MagicMock()
    service_error_handler = ServiceErrorHandler(get_response)

    request = rf.get("/")
    response = HttpResponse("OK")
    mock_error_page = mocker.patch("exporter.core.middleware.error_page")
    mock_error_page.return_value = response

    service_error = ServiceError(
        "Exception message",
        500,
        "Bad request",
        "Logger message",
        "Error message",
    )
    handler_response = service_error_handler.process_exception(request, service_error)

    assert handler_response == response
    assert ("ERROR", "Logger message") in [(r.levelname, r.msg) for r in caplog.records]
    mock_error_page.assert_called_with(request, "Error message")


def test_service_error_handler_service_error_with_debug(rf, mocker, caplog, settings):
    settings.DEBUG = True
    get_response = mocker.MagicMock()
    service_error_handler = ServiceErrorHandler(get_response)

    request = rf.get("/")
    response = HttpResponse("OK")
    mock_error_page = mocker.patch("exporter.core.middleware.error_page")
    mock_error_page.return_value = response

    service_error = ServiceError(
        "Exception message",
        500,
        "Bad request",
        "Logger message",
        "Error message",
    )

    with pytest.raises(ServiceError) as exception_info:
        service_error_handler.process_exception(request, service_error)

    assert exception_info.value == service_error
    assert ("ERROR", "Logger message") in [(r.levelname, r.msg) for r in caplog.records]
