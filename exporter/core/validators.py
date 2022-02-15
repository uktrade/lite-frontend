from http import HTTPStatus
from datetime import date
from django.utils import timezone
from dateutil.relativedelta import relativedelta

from exporter.applications.helpers.date_fields import format_date
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


def validate_expiry_date(request, field_name):
    """Validate that the section certificate expiry date is
    not in the past or > 5y in the future.
    """
    iso_date = format_date(request.POST, field_name)
    # Absence of ISO date is dealt with by the API
    if not iso_date:
        return ["Enter the certificate expiry date and include a day, month and year"]

    expiry_date = date.fromisoformat(iso_date)
    today = timezone.now().date()
    # Date of expiry has to be in the future
    if expiry_date < today:
        return ["Expiry date must be in the future"]
    else:
        if relativedelta(expiry_date, today).years >= 5:
            return ["Expiry date is too far in the future"]
