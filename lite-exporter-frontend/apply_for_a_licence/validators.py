from http import HTTPStatus


def validate_opening_question(_, json):
    if json.get("licence_type"):
        return json, HTTPStatus.OK

    return (
        {"errors": {"licence_type": ["Select the type of licence or clearance you need"]}},
        HTTPStatus.BAD_REQUEST,
    )
