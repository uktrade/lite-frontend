from requests import request


class ApiClient:
    gov_headers = {"content-type": "application/json"}
    exporter_headers = {"content-type": "application/json"}
    headers_initialised = False

    def __init__(self, base_url, request_data, context):
        self.base_url = base_url
        self.request_data = request_data
        self.context = context

    def add_to_context(self, name, value):
        self.context[name] = value

    def auth_gov_user(self):
        ApiClient.gov_headers["gov-user-token"] = self._auth_user(
            self.request_data["gov_user"], "/gov-users/authenticate/", "gov_user"
        )

    def auth_exporter_user(self, org_id=None):
        ApiClient.exporter_headers["organisation-id"] = org_id or self.context["org_id"]
        ApiClient.exporter_headers["exporter-user-token"] = self._auth_user(
            self.request_data["export_user"], "/users/authenticate/", "exporter_user"
        )

    def make_request(self, method, url, headers, body=None, files=None):
        if body:
            response = request(method, self.base_url + url, json=body, headers=headers, files=files)
        else:
            response = request(method, self.base_url + url, headers=headers)

        if not response.ok:
            raise Exception("bad response: " + response.text)

        return response

    def _auth_user(self, data, url, user_type):
        response = self.make_request(method="POST", url=url, body=data, headers=ApiClient.gov_headers).json()
        self.add_to_context(user_type + "_id", response["lite_api_user_id"])
        return response["token"]
