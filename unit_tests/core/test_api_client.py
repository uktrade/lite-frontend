from unittest.mock import Mock

from core import client


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
