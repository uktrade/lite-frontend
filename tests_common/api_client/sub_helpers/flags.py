class Flags:
    def __init__(self, api_client, request_data, **kwargs):
        super().__init__(**kwargs)
        self.api_client = api_client
        self.request_data = request_data

    def add_flag(self, flag_name, level):
        self.api_client.context["flag_name"] = flag_name
        data = self.request_data["flag"]
        data["name"] = flag_name
        data["level"] = level
        flag = self.api_client.make_request(
            method="POST", url="/flags/", headers=self.api_client.gov_headers, body=data,
        ).json()["flag"]
        self.api_client.add_to_context("flag_id", flag["id"])
