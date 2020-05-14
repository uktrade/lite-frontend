import json
import os

from mohawk import Sender
from requests import Session


class ApiClient:
    def __init__(self, base_url, request_data, context):
        self.base_url = base_url
        self.request_data = request_data
        self.context = context
        self.session = Session()
        self.gov_headers = {}
        self.exporter_headers = {}
        self.anonymous_headers = {}
        self.headers_initialised = False

    def auth_basic(self, user_name, user_password):
        self.session.auth = (user_name, user_password)

    def add_to_context(self, name, value):
        self.context[name] = value

    def auth_gov_user(self):
        self.gov_headers["GOV-USER-TOKEN"] = self.auth_user(
            self.request_data["gov_user"], "/gov-users/authenticate/", "gov_user"
        )

    def auth_exporter_user(self, org_id=None):
        self.exporter_headers["ORGANISATION-ID"] = org_id or self.context["org_id"]
        self.exporter_headers["EXPORTER-USER-TOKEN"] = self.auth_user(
            self.request_data["export_user"], "/users/authenticate/", "exporter_user"
        )

    def auth_user(self, data, url, user_type):
        response = self.make_request(method="POST", url=url, body=data, headers=self.gov_headers).json()
        self.add_to_context(user_type + "_id", response["lite_api_user_id"])
        return response["token"]

    def make_request(self, method, url, headers, body=None, files=None):
        url = self.base_url + url.replace(" ", "%20")

        if not url.endswith("/") and "?" not in url:
            url = url + "/"

        content_type = "text/plain" if method == "DELETE" else "application/json"

        if os.environ.get("HAWK_AUTHENTICATION_ENABLED") == "True":
            sender = self._get_hawk_sender(url, method, content_type, json.dumps(body) if body else "")
            headers["hawk-authentication"] = sender.request_header
            headers["content-type"] = sender.req_resource.content_type
            response = self.session.request(method, url, headers=headers, json=body, files=files)
            self._verify_api_response(response, sender)
        else:
            headers["content-type"] = content_type
            response = self.session.request(method, url, headers=headers, json=body, files=files)

        if not response.ok:
            raise Exception("bad response at: " + url + "\nwith message: " + response.text)
        return response

    @staticmethod
    def _get_hawk_sender(url, method, content_type, content):
        return Sender(
            credentials={"id": "lite-e2e", "key": os.environ.get("LITE_E2E_HAWK_KEY"), "algorithm": "sha256"},
            url=url,
            method=method,
            content=content,
            content_type=content_type,
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
