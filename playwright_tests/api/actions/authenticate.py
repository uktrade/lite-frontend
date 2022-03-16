from .requests_helper import post


def gov_auth(fixture):
    return post("gov-users/authenticate/", {"json": fixture}).json()


def export_auth(fixture):
    return post("users/authenticate/", {"json": fixture}).json()
