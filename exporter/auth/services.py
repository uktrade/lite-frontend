from core import client
import logging
from core.ip_filter import get_client_ip
from requests.exceptions import HTTPError

logger = logging.getLogger(__name__)


def authenticate_exporter_user(request, json):
    try:
        response = client.post(request, "/users/authenticate/", json)
        response.raise_for_status()
    except HTTPError as ex:
        logger.warning(
            "Authentication:Service: Authenticating user failed profile : %s client_ip: %s : %s",
            json,
            get_client_ip(request),
            str(ex),
        )
    return response.json(), response.status_code
