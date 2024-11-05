import logging
from ipware import get_client_ip as ipware_get_client_ip

logger = logging.getLogger(__name__)


def get_client_ip(request):
    ip, _ = ipware_get_client_ip(request)
    return ip or None
