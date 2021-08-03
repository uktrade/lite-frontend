from mohawk import Sender
from requests import Session

from django.conf import settings


class ApiClient:
    def __init__(self):
        self.base_url = settings.LITE_HMRC_URL
        self.session = Session()

    def make_request(self, method, url):
        url = self.base_url + url.replace(" ", "%20")

        if not url.endswith("/") and "?" not in url:
            url = url + "/"

        if settings.LITE_HMRC_HAWK_AUTHENTICATION_ENABLED:
            sender = self._get_hawk_sender(url, method)
            response = self.session.request(method, url)
            self._verify_api_response(response, sender)
        else:
            response = self.session.request(method, url)

        if not response.ok:
            raise Exception("bad response at: " + url + "\nwith message: " + response.text)
        return response

    @staticmethod
    def _get_hawk_sender(url, method):
        return Sender(
            credentials={
                "id": "LITE_HMRC_INTEGRATION_HAWK_KEY",
                "key": settings.LITE_HMRC_HAWK_KEY,
                "algorithm": "sha256",
            },
            url=url,
            method=method,
            seen_nonce=lambda x, y, z: False,
            always_hash_content=False,
        )

    @staticmethod
    def _verify_api_response(response, sender):
        try:
            sender.accept_response(
                response.headers["server-authorization"],
                content=response.content,
                content_type=response.headers["Content-Type"],
            )
        except Exception as exc:  # noqa
            if "server-authorization" not in response.headers:
                print(
                    "No server_authorization header found in response from the LITE API - "
                    "probable API HAWK auth failure"
                )
            else:
                print(f"Unhandled exception {type(exc).__name__}: {exc}")
            print("We were unable to authenticate your client")
