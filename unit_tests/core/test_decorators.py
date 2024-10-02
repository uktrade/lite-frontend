import pytest

from http import HTTPStatus

from requests.exceptions import HTTPError

from django.http import (
    HttpResponse,
    Http404,
)

from core.decorators import expect_status
from core.exceptions import ServiceError


def test_expect_status_success():
    response = HttpResponse()

    @expect_status(
        HTTPStatus.OK,
        "Will not error",
        "Will not error",
    )
    def success():
        return response, response.status_code

    returned_response, returned_status_code = success()

    assert returned_response == response
    assert returned_status_code == response.status_code
    assert returned_status_code == HTTPStatus.OK


def test_expect_status_handles_http_error():
    response = HttpResponse()
    response.status_code = HTTPStatus.INTERNAL_SERVER_ERROR

    @expect_status(
        HTTPStatus.OK,
        "Logger - Raises",
        "Error - Raises",
    )
    def http_error():
        raise HTTPError(response=response)

    with pytest.raises(ServiceError) as e:
        http_error()

    exception = e.value
    assert exception.status_code == HTTPStatus.INTERNAL_SERVER_ERROR
    assert exception.response == response
    assert exception.log_message == "Logger - Raises - response was: %s - %s"
    assert exception.user_message == "Error - Raises"


def test_expect_status_reraises_404():
    response = HttpResponse()
    response.status_code = HTTPStatus.NOT_FOUND

    @expect_status(
        HTTPStatus.OK,
        "Logger - 404",
        "Error - 404",
        reraise_404=True,
    )
    def returns_404():
        return response, response.status_code

    with pytest.raises(Http404):
        returns_404()


def test_expect_status_handles_wrong_status_code():
    response = HttpResponse()
    response.status_code = HTTPStatus.INTERNAL_SERVER_ERROR

    @expect_status(
        HTTPStatus.OK,
        "Logger - Wrong status code",
        "Error - Wrong status code",
    )
    def wrong_status_code():
        return response, response.status_code

    with pytest.raises(ServiceError) as e:
        wrong_status_code()

    exception = e.value
    assert exception.status_code == HTTPStatus.INTERNAL_SERVER_ERROR
    assert exception.response == response
    assert exception.log_message == "Logger - Wrong status code - response was: %s - %s"
    assert exception.user_message == "Error - Wrong status code"
