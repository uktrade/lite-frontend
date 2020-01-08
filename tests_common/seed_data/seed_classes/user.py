from .seed_class import SeedClass
from ..make_requests import make_request


class User(SeedClass):
    def add_user(self, data, url, token_name, user_type):
        response = make_request("POST", base_url=self.base_url, url=url, body=data, headers=self.gov_headers).json()
        self.add_to_context(token_name, response["token"])
        self.add_to_context(user_type + "_id", response["lite_api_user_id"])

    def auth_gov_user(self):
        self.add_user(self.request_data["gov_user"], "/gov-users/authenticate/", "gov_user_token", "gov_user")
        self.gov_headers["gov-user-token"] = self.context["gov_user_token"]

    def auth_export_user(self, org_id=None):
        if not org_id:
            org_id = self.context["org_id"]
        self.add_user(self.request_data["export_user"], "/users/authenticate/", "export_user_token", "exporter_user")
        self.export_headers["exporter-user-token"] = self.context["export_user_token"]
        self.export_headers["organisation-id"] = org_id
        self.add_to_context("exporter_headers", self.export_headers)
