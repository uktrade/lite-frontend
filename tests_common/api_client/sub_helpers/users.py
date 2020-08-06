import base64
import os


class Users:
    def __init__(self, api_client, request_data, **kwargs):
        super().__init__(**kwargs)
        self.api_client = api_client
        self.request_data = request_data

    def add_user(self, data, url, token_name, user_type):
        response = self.api_client.make_request(
            method="POST", url=url, body=data, headers=self.api_client.gov_headers
        ).json()
        self.api_client.add_to_context(token_name, response["token"])
        self.api_client.add_to_context(user_type + "_id", response["lite_api_user_id"])


def post_user_to_great_sso():
    from directory_sso_api_client.client import sso_api_client

    class BasicAuthenticator:
        def __init__(self, username: str, password: str):
            credentials = f"{username}:{password}"
            encoded_credentials = base64.b64encode(credentials.encode("ascii"))
            self.headers = {"Authorization": f"Basic {encoded_credentials.decode('ascii')}"}

    basic_authenticator = None
    if os.getenv("TEST_TYPE_BROWSER_STACK", "False") == "True":
        auth_user_name = os.environ.get("AUTH_USER_NAME")
        auth_user_password = os.environ.get("AUTH_USER_PASSWORD")
        basic_authenticator = BasicAuthenticator(auth_user_name, auth_user_password)

    response = sso_api_client.post("/testapi/test-users/", data={}, authenticator=basic_authenticator).json()
    exporter_sso_email = response["email"]
    name = str(response["first_name"]) + " " + str(response["last_name"])
    first_name, last_name = name.split(" ")
    exporter_sso_password = response["password"]
    sso_api_client.patch(
        url=f"testapi/user-by-email/{exporter_sso_email}/",
        data={"is_verified": True},
        authenticator=basic_authenticator,
    )

    return {
        "email": exporter_sso_email,
        "password": exporter_sso_password,
        "first_name": first_name,
        "last_name": last_name,
    }
