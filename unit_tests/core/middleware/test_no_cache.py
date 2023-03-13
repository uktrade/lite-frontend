from rest_framework.response import Response

from core.middleware import NoCacheMiddleware


def test_no_cache_middleware(rf, mocker):
    request = rf.get("/")
    get_response = mocker.Mock(return_value=Response())
    instance = NoCacheMiddleware(get_response)
    response = instance(request)
    assert response["Cache-Control"] == "max-age=0, no-cache, no-store, must-revalidate, private"
