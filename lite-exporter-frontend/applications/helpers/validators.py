from http import HTTPStatus

from applications.forms.location import Locations
from applications.services import set_application_status, delete_application, put_application
from lite_content.lite_exporter_frontend import strings, goods


def validate_withdraw_application(request, pk, json):
    if json.get("choice"):
        if json.get("choice") == "yes":
            return set_application_status(request, pk, "withdrawn")
        return json, HTTPStatus.OK

    return (
        {"errors": {"choice": [strings.applications.ApplicationSummaryPage.Withdraw.WITHDRAW_ERROR]}},
        HTTPStatus.BAD_REQUEST,
    )


def validate_surrender_application_and_update_case_status(request, pk, json):
    confirmation = json.get("choice")
    if confirmation:
        if confirmation == "yes":
            return set_application_status(request, pk, "surrendered")
        else:
            return json, HTTPStatus.OK

    return (
        {"errors": {"choice": [strings.applications.ApplicationSummaryPage.Surrender.WITHDRAW_ERROR]}},
        HTTPStatus.BAD_REQUEST,
    )


def validate_delete_draft(request, pk, json):
    if json.get("choice"):
        if json.get("choice") == "yes":
            return delete_application(request, pk)
        return json, HTTPStatus.OK

    return {"errors": {"choice": [strings.applications.DeleteApplicationPage.DELETE_ERROR]}}, HTTPStatus.BAD_REQUEST


def validate_and_update_goods_location_choice(_request, _pk, json):
    choice = json.get("choice")

    if choice:
        put_application(_request, _pk, {"have_goods_departed": choice == Locations.DEPARTED})
        return json, HTTPStatus.OK

    return {"errors": {"choice": [goods.GoodsLocationForm.ERROR]}}, HTTPStatus.BAD_REQUEST


def validate_external_location_choice(_request, _pk, json):
    if json.get("choice"):
        return json, HTTPStatus.OK

    return {"errors": {"choice": [goods.GoodsLocationForm.ERROR]}}, HTTPStatus.BAD_REQUEST
