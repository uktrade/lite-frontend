import re
import phonenumbers

from django.core.exceptions import ValidationError

from .constants import Validation


def validate_vat(value):
    if value:
        stripped_vat = re.sub(r"[^A-Z0-9]", "", value)
        if len(stripped_vat) < Validation.UK_VAT_MIN_LENGTH:
            raise ValidationError("Standard UK VAT numbers are 9 digits long")
        elif len(stripped_vat) > Validation.UK_VAT_MAX_LENGTH:
            raise ValidationError("Standard UK VAT numbers are 9 digits long")
        elif not re.match(Validation.UK_VAT_VALIDATION_REGEX, stripped_vat):
            raise ValidationError("Invalid UK VAT number")
        return stripped_vat


def validate_eori(value):
    if value:
        eori = re.sub(r"[^A-Z0-9]", "", value)
        if len(eori) > Validation.UK_EORI_MAX_LENGTH:
            raise ValidationError("EORI numbers are 17 characters or less")
        elif not re.match(Validation.UK_EORI_VALIDATION_REGEX, eori):
            raise ValidationError("Invalid UK EORI number")


def validate_phone(value):
    try:
        phone_number = phonenumbers.parse(value, "GB")
        if not phonenumbers.is_valid_number(phone_number):
            raise ValidationError("Invalid telephone number")
    except phonenumbers.phonenumberutil.NumberParseException:
        raise ValidationError("Invalid telephone number")


def validate_sic_number(value):
    if value:
        if not value.isdigit():
            raise ValidationError(Validation.ONLY_ENTER_NUMBERS)
        int_value = int(value)
        if int_value < 1110 or int_value > 99999:
            raise ValidationError(Validation.INVALID_SIC)
        if len(value) != 5:
            raise ValidationError(Validation.LENGTH_SIC)
    return value


def validate_registration(value):
    if value:
        if len(value) != 8:
            raise ValidationError(Validation.LENGTH_REGISTRATION_NUMBER)
        if not value[2:].isdigit():
            raise ValidationError(Validation.LENGTH_REGISTRATION_NUMBER)
    return value
