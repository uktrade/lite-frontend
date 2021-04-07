from unittest import mock

import pytest
from rest_framework import status
from rest_framework.response import Response

from core import middleware


def test_no_cache_middleware(rf):
    request = rf.get("/")
    get_response = mock.Mock(return_value=Response())
    instance = middleware.NoCacheMiddleware(get_response)
    response = instance(request)
    assert response["Cache-Control"] == "max-age=0, no-cache, no-store, must-revalidate"


@pytest.mark.parametrize(
    "url,response_code",
    [
        ("?return_to=hello", status.HTTP_200_OK),
        ("?return_to=hello/", status.HTTP_200_OK),
        ("?return_to=/hello", status.HTTP_200_OK),
        ("?return_to=/hello/", status.HTTP_200_OK),
        ("?return_to=http://example.com", status.HTTP_400_BAD_REQUEST),
        ("?return_to=http://example.com/", status.HTTP_400_BAD_REQUEST),
        ("?return_to=https://example.com/", status.HTTP_400_BAD_REQUEST),
        ('?return_to=javascript:alert("hello!")', status.HTTP_400_BAD_REQUEST),
        # Protocol-relative URL
        ("?return_to=////example.com", status.HTTP_400_BAD_REQUEST),
        ("?return_to=///example.com", status.HTTP_400_BAD_REQUEST),
        ("?return_to=//example.com", status.HTTP_400_BAD_REQUEST),
    ],
)
def test_validate_return_to_middleware(rf, url, response_code):
    request = rf.get(url)
    get_response = mock.Mock(return_value=Response())
    response = middleware.ValidateReturnToMiddleware(get_response)(request)
    assert response.status_code == response_code
