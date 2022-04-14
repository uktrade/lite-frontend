from http import HTTPStatus
from datetime import date
from dateutil.relativedelta import relativedelta

from django.core.exceptions import ValidationError
from django.utils import timezone

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


class FutureDateValidator:
    def __init__(self, message):
        self.message = message

    def __call__(self, value):
        if value <= date.today():
            raise ValidationError(self.message)


class PastDateValidator:
    def __init__(self, message):
        self.message = message

    def __call__(self, value):
        if value > date.today():
            raise ValidationError(self.message)


class RelativeDeltaDateValidator:
    def __init__(self, message, **kwargs):
        self.message = message
        self.relativedelta = relativedelta(**kwargs)

    def __call__(self, value):
        if value > (date.today() + self.relativedelta):
            raise ValidationError(self.message)
