from faker import Faker

from ...tools.helpers import strip_special_characters, get_current_date_time

fake = Faker()


class Organisations:
    def __init__(self, api_client, request_data, **kwargs):
        super().__init__(**kwargs)
        self.api_client = api_client
        self.request_data = request_data

    def setup_org(self):
        organisation = self.find_org_by_name(self.request_data["organisation"]["name"])

        if not organisation:
            organisation = self.add_org("organisation")
            org_id = organisation["id"]
        else:
            org_id = organisation["id"]
            user = self.find_test_user_in_org(org_id)
            if not user:
                self.add_test_user_to_exporter_org(org_id)

        self.api_client.add_to_context("org_id", org_id)
        self.api_client.add_to_context("org_name", self.request_data["organisation"]["name"])
        self.api_client.add_to_context("primary_site_id", self.get_org_primary_site_id(org_id))
        self.api_client.add_to_context("first_name", self.request_data["organisation"]["user"]["first_name"])
        self.api_client.add_to_context("last_name", self.request_data["organisation"]["user"]["last_name"])

    def setup_org_for_switching_organisations(self):
        organisation = self.find_org_by_name(self.request_data["organisation_for_switching_organisations"]["name"])

        if not organisation:
            organisation = self.add_org("organisation_for_switching_organisations")
            org_id = organisation["id"]
        else:
            org_id = organisation["id"]
            user = self.find_test_user_in_org(org_id)
            if not user:
                self.add_test_user_to_exporter_org(org_id)

        self.api_client.add_to_context(
            "org_name_for_switching_organisations",
            self.request_data["organisation_for_switching_organisations"]["name"],
        )
        self.api_client.add_to_context(
            "hmrc_org_id",
            org_id,
        )
        self.api_client.add_to_context("hmrc_primary_site_id", self.get_org_primary_site_id(org_id))

    def add_test_user_to_exporter_org(self, org_id):
        data = self.request_data["export_user"]
        return self.api_client.make_request(
            method="POST",
            url=f"/organisations/{org_id}/users/",
            body=data,
            headers=self.api_client.gov_headers,
        ).json()

    def find_org_by_name(self, org_name):
        organisations = self.api_client.make_request(
            method="GET",
            url="/organisations/?search_term=" + org_name,
            headers=self.api_client.gov_headers,
        ).json()["results"]
        organisation = next((item for item in organisations if item["name"] == org_name), None)
        return organisation

    def find_test_user_in_org(self, org_id):
        users = self.api_client.make_request(
            method="GET",
            url=f"/organisations/{org_id}/users/?disable_pagination=True",
            headers=self.api_client.gov_headers,
        ).json()
        user = next((item for item in users if item["email"] == self.request_data["export_user"]["email"]), None)
        return user

    def add_org(self, key):
        return self.api_client.make_request(
            method="POST",
            url="/organisations/",
            body=self.request_data[key],
            headers=self.api_client.gov_headers,
        ).json()

    def anonymous_user_create_org(self, data):
        return self.api_client.make_request(
            method="POST",
            url="/organisations/",
            body=data,
            headers=self.api_client.anonymous_headers,
        ).json()

    def get_org_primary_site_id(self, org_id):
        organisation = self.api_client.make_request(
            method="GET",
            url="/organisations/" + org_id,
            headers=self.api_client.gov_headers,
        ).json()
        return organisation["primary_site"]["id"]

    def add_site(self, organisation_id=None, data=None):
        organisation_id = organisation_id or self.request_data["organisation"]["id"]
        if not data:
            data = {
                "name": strip_special_characters(fake.company()) + get_current_date_time(),
                "address": {
                    "address_line_1": fake.street_address(),
                    "city": fake.city(),
                    "postcode": fake.postcode(),
                    "region": fake.state(),
                    "country": "GB",
                },
            }
        return self.api_client.make_request(
            method="POST",
            url=f"/organisations/{organisation_id}/sites/",
            headers=self.api_client.exporter_headers,
            body=data,
        ).json()["site"]

    def add_external_site(self, data, organisation_id=None):
        organisation_id = organisation_id or self.request_data["organisation"]["id"]

        return self.api_client.make_request(
            method="POST",
            url=f"/organisations/{organisation_id}/external_locations/",
            headers=self.api_client.exporter_headers,
            body=data,
        ).json()["external_location"]
