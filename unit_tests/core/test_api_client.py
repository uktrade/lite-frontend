import pytest
import requests

from requests.models import Response

from unittest.mock import Mock

from mohawk import (
    Receiver,
    Sender,
)
from mohawk.util import (
    prepare_header_val,
    utc_now,
)

from core import client
from core.client import (
    perform_request,
    verify_hawk_response,
)


def test_zipkin_headers(settings):
    request = Mock(headers={"x-b3-traceid": "123", "x-b3-spanid": "456"}, session={})
    request.requests_session = Mock()
    request.requests_session.request = Mock()
    client.get(request, "/foo/")
    request.requests_session.request.assert_called_once_with(
        headers={
            "content-type": "application/json",
            "ORGANISATION-ID": "None",
            "x-b3-traceid": "123",
            "x-b3-spanid": "456",
        },
        json={},
        method="GET",
        url=f"{settings.LITE_API_URL}/foo/",
        stream=False,
    )


def test_verify_hawk_response_no_server_authorization_header():
    response = Response()
    sender = Sender(
        {"id": "HAWK_ID", "key": "HAWK_KEY", "algorithm": "sha256"},
        "http://example.com",
        "GET",
        content_type="application/json",
        content='{"test": "test"}',
    )
    with pytest.raises(RuntimeError):
        verify_hawk_response(response, sender)


def test_verify_hawk_response():
    sender = Sender(
        {"id": "HAWK_ID", "key": "HAWK_KEY", "algorithm": "sha256"},
        "http://example.com/request/",
        "GET",
        content_type="application/json",
        content='{"request": "test"}',
    )

    receiver = Receiver(
        lambda x: {"id": "HAWK_ID", "key": "HAWK_KEY", "algorithm": "sha256"},
        sender.request_header,
        "http://example.com/request/",
        "GET",
        content_type="application/json",
        content='{"request": "test"}',
    )

    response = Response()
    response.headers["server-authorization"] = receiver.respond(
        '{"response": "test"}',
        content_type="application/json",
    )
    response.headers["content-type"] = "application/json"
    response.status_code = 200
    response._content = '{"response": "test"}'

    assert verify_hawk_response(response, sender) is None


def test_verify_hawk_response_streaming_content():
    sender = Sender(
        {"id": "HAWK_ID", "key": "HAWK_KEY", "algorithm": "sha256"},
        "http://example.com/request/",
        "GET",
        content_type="application/json",
        content='{"request": "test"}',
    )

    receiver = Receiver(
        lambda x: {"id": "HAWK_ID", "key": "HAWK_KEY", "algorithm": "sha256"},
        sender.request_header,
        "http://example.com/request/",
        "GET",
        content_type="application/json",
        content='{"request": "test"}',
    )

    response = Response()
    response.headers["server-authorization"] = receiver.respond(
        'attachment; filename="filename.jpg"',
        content_type="application/octet-stream",
    )
    response.headers["content-type"] = "application/octet-stream"
    response.headers["content-disposition"] = 'attachment; filename="filename.jpg"'
    response.status_code = 200
    response._content = b"test"

    assert verify_hawk_response(response, sender, stream=True) is None


def test_perform_request(settings, rf, client, requests_mock):
    settings.HAWK_AUTHENTICATION_ENABLED = True
    settings.LITE_HAWK_ID = "LITE_HAWK_ID"
    settings.LITE_HAWK_KEY = "LITE_HAWK_KEY"
    settings.LITE_API_URL = "http://api"

    request = rf.get("/")
    request.session = client.session
    request.requests_session = requests.Session()

    def text_callback(request, context):
        receiver = Receiver(
            lambda x: {"id": "LITE_HAWK_ID", "key": "LITE_HAWK_KEY", "algorithm": "sha256"},
            request.headers["hawk-authentication"],
            request.url,
            request.method,
            content_type=request.headers["content-type"],
            content=request.text,
        )
        context.status_code = 200
        response_header = receiver.respond(
            '{"response": "test"}',
            content_type="application/json",
        )
        # The following mimics how our API sets the header appropriately
        response_header = '{header}, nonce="{nonce}"'.format(
            header=response_header, nonce=prepare_header_val(receiver.parsed_header["nonce"])
        )
        response_header = '{header}, ts="{nonce}"'.format(
            header=response_header, nonce=prepare_header_val(str(utc_now()))
        )
        context.headers["server-authorization"] = response_header
        context.headers["content-type"] = "application/json"
        return '{"response": "test"}'

    requests_mock.get(
        "/test/",
        text=text_callback,
    )

    response = perform_request("GET", request, "/test/")
    assert response.status_code == 200
    assert response.text == '{"response": "test"}'
