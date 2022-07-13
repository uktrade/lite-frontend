import logging
from ipware import get_client_ip as ipware_get_client_ip
from django.conf import settings

logger = logging.getLogger(__file__)


def get_client_ip(request):
    ip, _ = ipware_get_client_ip(request)
    return ip or None
