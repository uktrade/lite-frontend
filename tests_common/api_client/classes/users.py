from .api_client import ApiClient


class Users(ApiClient):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def add_user(self, data, url, token_name, user_type):
        response = self.make_request(method="POST", url=url, body=data, headers=ApiClient.gov_headers).json()
        self.add_to_context(token_name, response["token"])
        self.add_to_context(user_type + "_id", response["lite_api_user_id"])
