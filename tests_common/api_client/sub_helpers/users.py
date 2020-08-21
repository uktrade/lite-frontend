import base64
import os

from directory_sso_api_client.client import sso_api_client


AUTH_USER_NAME = os.environ.get("AUTH_USER_NAME")
AUTH_USER_PASSWORD = os.environ.get("AUTH_USER_PASSWORD")
BASIC_AUTH_ENABLED = os.environ.get("BASIC_AUTH_ENABLED")


class BasicAuthenticator:
    def __init__(self, username: str, password: str):
        credentials = f"{username}:{password}"
        encoded_credentials = base64.b64encode(credentials.encode("ascii"))
        self.headers = {"Authorization": f"Basic {encoded_credentials.decode('ascii')}"}


def create_great_sso_user():
    if BASIC_AUTH_ENABLED == "True":
        auth_user_name = AUTH_USER_NAME
        auth_user_password = AUTH_USER_PASSWORD
        authenticator = BasicAuthenticator(auth_user_name, auth_user_password)
    else:
        authenticator = None

    response_create = sso_api_client.post("/testapi/test-users/", authenticator=authenticator)
    response_create.raise_for_status()
    parsed = response_create.json()

    response_update = sso_api_client.patch(
        url=f"testapi/user-by-email/{parsed['email']}/", data={"is_verified": True}, authenticator=authenticator
    )
    response_update.raise_for_status()

    return parsed
