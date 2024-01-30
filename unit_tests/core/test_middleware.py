import pytest

from django.http import HttpResponse, HttpResponseForbidden

from core.middleware import ValidateReturnToMiddleware


def test_validation_return_to_middleware_no_return_to_parameter(rf, mocker):
    response = HttpResponse("OK")
    get_response = mocker.MagicMock()
    get_response.return_value = response

    middleware = ValidateReturnToMiddleware(get_response)

    request = rf.get("/")
    middleware_response = middleware(request)

    assert response == middleware_response


def test_validation_return_to_middleware_unparseable_return_to_parameter(rf, mocker):
    response = HttpResponse("OK")
    get_response = mocker.MagicMock()
    get_response.return_value = response

    mock_urlparse = mocker.patch("core.middleware.urlparse")
    mock_urlparse.side_effect = ValueError("Invalid")

    middleware = ValidateReturnToMiddleware(get_response)

    request = rf.get("/?return_to=invalid")
    middleware_response = middleware(request)

    assert isinstance(middleware_response, HttpResponseForbidden)
    assert middleware_response.content == b"Unparseable return_to parameter"


@pytest.mark.parametrize(
    "return_to",
    (
        "http://example.com",
        "http://",
        "//example.com",
    ),
)
def test_validation_return_to_middleware_invalid_return_to_parameter(rf, mocker, return_to):
    response = HttpResponse("OK")
    get_response = mocker.MagicMock()
    get_response.return_value = response

    middleware = ValidateReturnToMiddleware(get_response)

    request = rf.get(f"/?return_to={return_to}")
    middleware_response = middleware(request)

    assert isinstance(middleware_response, HttpResponseForbidden)
    assert middleware_response.content == b"Invalid return_to parameter"
