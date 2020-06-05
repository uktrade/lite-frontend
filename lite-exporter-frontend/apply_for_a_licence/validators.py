from http import HTTPStatus

from lite_content.lite_exporter_frontend.applications import OpenGeneralLicenceQuestions


def validate_opening_question(_, json):
    if json.get("licence_type"):
        return json, HTTPStatus.OK

    return (
        {"errors": {"licence_type": ["Select the type of licence or clearance you need"]}},
        HTTPStatus.BAD_REQUEST,
    )


def validate_open_general_licences(_, json):
    if not json.get("control_list_entry"):
        return (
            {"errors": {"control_list_entry": [OpenGeneralLicenceQuestions.ControlListEntry.ERROR]}},
            HTTPStatus.BAD_REQUEST,
        )

    if not json.get("country"):
        return ({"errors": {"country": [OpenGeneralLicenceQuestions.Country.ERROR]}}, HTTPStatus.BAD_REQUEST)

    if not hasattr(json.get("open_general_licence"), "__len__"):
        return (
            {"errors": {"open_general_licence": [OpenGeneralLicenceQuestions.OpenGeneralLicences.ERROR]}},
            HTTPStatus.BAD_REQUEST,
        )

    return json, HTTPStatus.OK
