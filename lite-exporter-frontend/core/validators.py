from http import HTTPStatus


def validate_register_organisation_triage(_, json):
    if json.get("type"):
        return json, HTTPStatus.OK

    return (
        {"errors": {"type": ["Select the type of organisation you're registering for"]}},
        HTTPStatus.BAD_REQUEST,
    )
