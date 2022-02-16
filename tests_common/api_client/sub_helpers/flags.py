from caseworker.flags.enums import FlagLevel


class Flags:
    def __init__(self, api_client, request_data, **kwargs):
        super().__init__(**kwargs)
        self.api_client = api_client
        self.request_data = request_data

    def add_flag(self, flag_name, level, blocks_finalising=False):
        self.api_client.context["flag_name"] = flag_name
        data = self.request_data["flag"]
        data["name"] = flag_name
        data["level"] = level
        data["blocks_finalising"] = blocks_finalising
        flag = self.api_client.make_request(
            method="POST",
            url="/flags/",
            headers=self.api_client.gov_headers,
            body=data,
        ).json()
        self.api_client.add_to_context("flag_id", flag["id"])
        return flag

    def get_list_of_flags(self):
        flags = self.api_client.make_request(
            method="GET",
            url="/flags/?disable_pagination=True",
            headers=self.api_client.gov_headers,
        ).json()
        return flags

    def assign_case_flags(self, case_pk, flags):
        data = {
            "level": FlagLevel.CASES,
            "objects": [case_pk],
            "flags": flags,
        }
        self.api_client.make_request(
            method="PUT",
            url="/flags/assign/",
            headers=self.api_client.gov_headers,
            body=data,
        )

    def assign_destination_flags(self, dest_pk, flags):

        if not isinstance(dest_pk, list):
            dest_pk = [dest_pk]

        data = {
            "level": FlagLevel.DESTINATIONS,
            "objects": dest_pk,
            "flags": flags,
        }
        self.api_client.make_request(
            method="PUT",
            url="/flags/assign/",
            headers=self.api_client.gov_headers,
            body=data,
        )
