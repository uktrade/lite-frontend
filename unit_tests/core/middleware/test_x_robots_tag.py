from rest_framework import status
from rest_framework.response import Response

from core.middleware import XRobotsTagMiddleware


def test_x_robots_tag_middleware(rf, mocker):
    # Set up mock request and response
    request = rf.get("/")
    get_response = mocker.Mock(return_value=Response())
    # Instantiate and call the middleware
    instance = XRobotsTagMiddleware(get_response)
    # We should get a 200 and the token should be cached
    response = instance(request)
    assert response.status_code == status.HTTP_200_OK
    assert response.headers["x-robots-tag"] == "noindex,nofollow"
