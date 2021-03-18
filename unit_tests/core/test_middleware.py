from unittest import mock

from django.http import HttpResponse

from core import middleware


def test_no_cache_middleware(rf):
    request = rf.get("/")
    get_response = mock.Mock(return_value=HttpResponse(""))
    instance = middleware.NoCacheMiddlware(get_response)

    response = instance(request)

    assert response["Cache-Control"] == "max-age=0, no-cache, no-store, must-revalidate"
