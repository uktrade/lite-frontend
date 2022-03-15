from .requests_helper import post, put


def create_organisation(fixture, headers):
    return post("organisations/", {"headers": headers, "json": fixture}).json()


def update_organisation_status(organisation_id, headers):
    put(f"organisations/{organisation_id}/status/", {"json": {"status": "active"}, "headers": headers})


def add_user_to_organisation(organisation_id, fixture, headers):
    post(f"organisations/{organisation_id}/users/", {"json": fixture, "headers": headers})


def add_site_to_organisation(organisation_id, fixture, headers):
    return post(f"organisations/{organisation_id}/sites/", {"json": fixture, "headers": headers}).json()
