import pytest

from rest_framework import status
from rest_framework.response import Response

from core.middleware import ValidateReturnToMiddleware


@pytest.mark.parametrize(
    "url,response_code",
    [
        ("?return_to=hello", status.HTTP_200_OK),
        ("?return_to=hello/", status.HTTP_200_OK),
        ("?return_to=/hello", status.HTTP_200_OK),
        ("?return_to=/hello/", status.HTTP_200_OK),
        ("?return_to=http://example.com", status.HTTP_403_FORBIDDEN),
        ("?return_to=http://example.com/", status.HTTP_403_FORBIDDEN),
        ("?return_to=https://example.com/", status.HTTP_403_FORBIDDEN),
        ('?return_to=javascript:alert("hello!")', status.HTTP_403_FORBIDDEN),
        # Protocol-relative URL
        ("?return_to=////example.com", status.HTTP_403_FORBIDDEN),
        ("?return_to=///example.com", status.HTTP_403_FORBIDDEN),
        ("?return_to=//example.com", status.HTTP_403_FORBIDDEN),
    ],
)
def test_validate_return_to_middleware(rf, url, response_code, mocker):
    request = rf.get(url)
    get_response = mocker.Mock(return_value=Response())
    response = ValidateReturnToMiddleware(get_response)(request)
    assert response.status_code == response_code
