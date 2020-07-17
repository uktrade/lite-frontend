import json
import logging

import requests
from django.contrib.auth.models import AnonymousUser
from django.core.cache import cache
from django.core.exceptions import PermissionDenied
from mohawk import Sender
from mohawk.exc import AlreadyProcessed

from conf import settings
from conf.settings import HAWK_AUTHENTICATION_ENABLED, env


def get(request, appended_address):
    url = _build_absolute_uri(appended_address.replace(" ", "%20"))

    if HAWK_AUTHENTICATION_ENABLED:
        sender = _get_hawk_sender(url, "GET", "application/json", "")

        response = requests.get(url=url, headers=_get_headers(request, sender))

        _verify_api_response(response, sender)
    else:
        response = requests.get(url=url, headers=_get_headers(request, content_type="application/json"))

    return response


def post(request, appended_address, request_data):
    url = _build_absolute_uri(appended_address)

    if HAWK_AUTHENTICATION_ENABLED:
        sender = _get_hawk_sender(url, "POST", "application/json", json.dumps(request_data))

        response = requests.post(url=url, headers=_get_headers(request, sender), json=request_data)

        _verify_api_response(response, sender)
    else:
        response = requests.post(
            url=url, headers=_get_headers(request, content_type="application/json"), json=request_data
        )

    return response


def put(request, appended_address, request_data):
    url = _build_absolute_uri(appended_address)

    if HAWK_AUTHENTICATION_ENABLED:
        sender = _get_hawk_sender(url, "PUT", "application/json", json.dumps(request_data))

        response = requests.put(url=url, headers=_get_headers(request, sender), json=request_data)

        _verify_api_response(response, sender)
    else:
        response = requests.put(
            url=url, headers=_get_headers(request, content_type="application/json"), json=request_data
        )

    return response


def patch(request, appended_address, request_data):
    url = _build_absolute_uri(appended_address)

    if HAWK_AUTHENTICATION_ENABLED:
        sender = _get_hawk_sender(url, "PATCH", "application/json", json.dumps(request_data))

        response = requests.patch(url=url, headers=_get_headers(request, sender), json=request_data)

        _verify_api_response(response, sender)
    else:
        response = requests.patch(
            url=url, headers=_get_headers(request, content_type="application/json"), json=request_data
        )

    return response


def delete(request, appended_address):
    url = _build_absolute_uri(appended_address)

    if HAWK_AUTHENTICATION_ENABLED:
        sender = _get_hawk_sender(url, "DELETE", "text/plain", "")

        response = requests.delete(url=url, headers=_get_headers(request, sender))

        _verify_api_response(response, sender)
    else:
        response = requests.delete(url=url, headers=_get_headers(request, content_type="text/plain"))

    return response


def _build_absolute_uri(appended_address):
    url = env("LITE_API_URL") + appended_address

    if not url.endswith("/") and "?" not in url:
        url = url + "/"

    return url


def _get_headers(request, sender=None, content_type=None):
    headers = {"X-Correlation-Id": str(request.correlation if hasattr(request, "correlation") else "")}

    if sender:
        headers["content-type"] = sender.req_resource.content_type
        headers["hawk-authentication"] = sender.request_header

    if content_type:
        headers["content-type"] = content_type

    if not isinstance(request.user, AnonymousUser):
        headers["GOV-USER-TOKEN"] = str(request.user.user_token)

    return headers


def _get_hawk_sender(url, method, content_type, content):
    return Sender(
        {"id": "internal-frontend", "key": env("LITE_INTERNAL_HAWK_KEY"), "algorithm": "sha256"},
        url,
        method,
        content_type=content_type,
        content=content,
        seen_nonce=_seen_nonce,
    )


def _seen_nonce(access_key_id, nonce, timestamp):
    """
    Returns if the passed access_key_id/nonce combination has been
    used before
    """

    cache_key = f"hawk:{access_key_id}:{nonce}"

    # cache.add only adds key if it isn't present
    seen_cache_key = not cache.add(cache_key, True, timeout=settings.HAWK_RECEIVER_NONCE_EXPIRY_SECONDS)

    if seen_cache_key:
        raise AlreadyProcessed(f"Already seen nonce {nonce}")

    return seen_cache_key


def _verify_api_response(response, sender):
    try:
        sender.accept_response(
            response.headers["server-authorization"],
            content=response.content,
            content_type=response.headers["Content-Type"],
        )
    except Exception as exc:  # noqa
        if "server-authorization" not in response.headers:
            logging.error(
                "No server_authorization header found in response from the LITE API - probable API HAWK auth failure"
            )
        else:
            logging.error("Unhandled exception %s: %s" % (type(exc).__name__, exc))
        raise PermissionDenied("We were unable to authenticate your client")
