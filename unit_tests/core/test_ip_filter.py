from core.ip_filter import get_client_ip
from django.http import HttpRequest


def test_get_client_ip():
    request = HttpRequest()
    request.META = {"REMOTE_ADDR": "192.168.93.2"}
    ip_address = get_client_ip(request)
    assert ip_address == "192.168.93.2"


def test_get_client_ip_ip():
    request = HttpRequest()
    assert get_client_ip(request) is None
