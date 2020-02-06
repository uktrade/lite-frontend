from ...api_client.api_client import ApiClient


class Users:
    def __init__(self, api_client, request_data, **kwargs):
        super().__init__(**kwargs)
        self.api_client = api_client
        self.request_data = request_data

    def add_user(self, data, url, token_name, user_type):
        response = self.api_client.make_request(method="POST", url=url, body=data, headers=ApiClient.gov_headers).json()
        self.api_client.add_to_context(token_name, response["token"])
        self.api_client.add_to_context(user_type + "_id", response["lite_api_user_id"])
