from functools import partial
import json
import logging

from django.core.cache import cache
from mohawk import Sender
from mohawk.exc import AlreadyProcessed
import sentry_sdk

from django.conf import settings


logger = logging.getLogger(__name__)


def _build_absolute_uri(appended_address):
    url = settings.LITE_API_URL + appended_address

    if not url.endswith("/") and "?" not in url:
        url = url + "/"

    return url


def _get_headers(request, sender=None, content_type=None):
    headers = {}
    if sender:
        headers["content-type"] = sender.req_resource.content_type
        headers["hawk-authentication"] = sender.request_header
    if content_type:
        headers["content-type"] = content_type
    if "user_token" in request.session:
        headers[settings.LITE_API_AUTH_HEADER_NAME] = request.session["user_token"]
    headers["ORGANISATION-ID"] = request.session.get("organisation", "None")
    headers["x-b3-traceid"] = request.headers.get("x-b3-traceid")
    headers["x-b3-spanid"] = request.headers.get("x-b3-spanid")
    return headers


def _get_hawk_sender(url, method, content_type, content):
    return Sender(
        {"id": settings.LITE_HAWK_ID, "key": settings.LITE_HAWK_KEY, "algorithm": "sha256"},
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


def verify_hawk_response(response, sender, stream=False):
    if "server-authorization" not in response.headers:
        sentry_sdk.set_context("response", {"content": response.content})
        raise RuntimeError("Missing server_authorization header. Probable API HAWK auth failure")

    if stream:
        content = response.headers["Content-Disposition"]
    else:
        content = response.content

    sender.accept_response(
        response.headers["server-authorization"],
        content=content,
        content_type=response.headers["Content-Type"],
    )


def perform_request(method, request, appended_address, data=None, stream=False):
    session = request.requests_session  # provided by RequestsSessionMiddleware
    url = _build_absolute_uri(appended_address.replace(" ", "%20"))

    if method in ["GET", "HEAD"]:
        # If we not sending any data then the hawk header should be defined with no content and no header
        content_type = ""
        content = None
        data = None
    else:
        data = data or {}
        content_type = "application/json"
        content = json.dumps(data)

    if settings.HAWK_AUTHENTICATION_ENABLED:
        sender = _get_hawk_sender(url, method, content_type, content)
        headers = _get_headers(request, sender)
    else:
        headers = _get_headers(request, content_type=content_type)

    logger.debug("API request: %s %s %s %s", method, url, headers, data)

    response = session.request(method=method, url=url, headers=headers, json=data, stream=stream)

    if settings.HAWK_AUTHENTICATION_ENABLED:
        verify_hawk_response(response=response, sender=sender, stream=stream)

    return response


get = partial(perform_request, "GET")
head = partial(perform_request, "HEAD")
patch = partial(perform_request, "PATCH")
put = partial(perform_request, "PUT")
post = partial(perform_request, "POST")
delete = partial(perform_request, "DELETE")
