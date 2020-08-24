from core.auth.utils import get_client

from django.utils.functional import SimpleLazyObject


def get_authbroker_client(request):
    if not hasattr(request, "_cached_client"):
        request._cached_client = get_client(request)
    return request._cached_client


class AuthbrokerClientMiddleware:
    def __init__(self, get_response=None):
        self.get_response = get_response

    def __call__(self, request):
        request.authbroker_client = SimpleLazyObject(lambda: get_authbroker_client(request))
        return self.get_response(request)
