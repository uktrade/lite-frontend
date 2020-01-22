from .seed_class import SeedClass
from ..make_requests import make_request


class Organisation(SeedClass):
    def setup_org(self):
        organisation = self.find_org_by_name(self.request_data["organisation"]["name"])

        if not organisation:
            organisation = self.add_org("organisation")
            org_id = organisation["id"]
        else:
            org_id = organisation["id"]
            user = self.find_test_user_in_org(org_id)
            if not user:
                self.add_user_to_exporter_org(org_id)

        self.add_to_context("org_id", org_id)
        self.add_to_context("org_name", self.request_data["organisation"]["name"])
        self.add_to_context("primary_site_id", self.get_org_primary_site_id(org_id))
        self.add_to_context("first_name", self.request_data["organisation"]["user"]["first_name"])
        self.add_to_context("last_name", self.request_data["organisation"]["user"]["last_name"])

    def setup_org_for_switching_organisations(self):
        organisation = self.find_org_by_name(self.request_data["organisation_for_switching_organisations"]["name"])

        if not organisation:
            organisation = self.add_org("organisation_for_switching_organisations")
            org_id = organisation["id"]
        else:
            org_id = organisation["id"]
            user = self.find_test_user_in_org(org_id)
            if not user:
                self.add_user_to_exporter_org(org_id)

        self.add_to_context(
            "org_name_for_switching_organisations",
            self.request_data["organisation_for_switching_organisations"]["name"],
        )
        self.add_to_context(
            "hmrc_org_id", org_id,
        )

    def add_user_to_exporter_org(self, org_id):
        data = self.request_data["export_user"]
        return make_request(
            "POST", base_url=self.base_url, url="/organisations/" + org_id + "/users/", body=data,
            headers=self.gov_headers,
        ).json()

    def find_org_by_name(self, org_name):
        organisations = make_request(
            "GET", base_url=self.base_url, url="/organisations/?search_term=" + org_name, headers=self.gov_headers,
        ).json()["results"]
        organisation = next((item for item in organisations if item["name"] == org_name), None)
        return organisation

    def find_test_user_in_org(self, org_id):
        users = make_request(
            "GET", base_url=self.base_url, url="/organisations/" + org_id + "/users/", headers=self.gov_headers,
        ).json()["users"]
        user = next((item for item in users if item["email"] == self.request_data["export_user"]["email"]), None)
        return user

    def add_org(self, key):
        data = self.request_data[key]
        return make_request(
            "POST", base_url=self.base_url, url="/organisations/", body=data, headers=self.gov_headers,
        ).json()

    def get_org_primary_site_id(self, org_id):
        organisation = make_request(
            "GET", base_url=self.base_url, url="/organisations/" + org_id, headers=self.gov_headers,
        ).json()
        return organisation["primary_site"]["id"]
