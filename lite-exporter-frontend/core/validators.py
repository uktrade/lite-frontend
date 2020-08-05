from http import HTTPStatus

from lite_content.lite_exporter_frontend.core import RegisterAnOrganisation


def validate_register_organisation_triage(_, json):
    errors = {}

    if not json.get("type"):
        errors["type"] = [RegisterAnOrganisation.CommercialOrIndividual.ERROR]

    if not json.get("location"):
        errors["location"] = [RegisterAnOrganisation.WhereIsYourOrganisationBased.ERROR]

    if errors:
        return {"errors": errors}, HTTPStatus.BAD_REQUEST

    return json, HTTPStatus.OK
