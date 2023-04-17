import base64
import os


class BasicAuthenticator:
    def __init__(self, username: str, password: str):
        credentials = f"{username}:{password}"
        encoded_credentials = base64.b64encode(credentials.encode("ascii"))
        self.headers = {"Authorization": f"Basic {encoded_credentials.decode('ascii')}"}


def create_govuk_sso_user():
    # we should decide if we would like to create a govuk user, if so it should be here
    first_name, last_name = os.environ.get("TEST_SSO_NAME").split(" ")
    return {
        "email": os.environ.get("EXPORTER_TEST_SSO_EMAIL"),
        "first_name": first_name,
        "last_name": last_name,
        "password": os.environ.get("EXPORTER_TEST_SSO_PASSWORD"),
    }
