import phonenumbers

from django.core.exceptions import ValidationError

from .constants import Validation


def validate_vat(value):
    errors = []
    if value:
        errors.extend(key for key, func in Validation.validate_vat_number_functions.items() if func(value))
        if errors:
            raise ValidationError(errors)


def validate_eori(value):
    errors = []
    if value:
        errors.extend(key for key, func in Validation.validate_eori_number_functions.items() if func(value))
        if errors:
            raise ValidationError(errors)


def validate_phone(value):
    try:
        phone_number = phonenumbers.parse(value, "GB")
        if not phonenumbers.is_valid_number(phone_number):
            raise ValidationError("Invalid telephone number")
    except phonenumbers.phonenumberutil.NumberParseException:
        raise ValidationError("Invalid telephone number")


def validate_sic_number(value):
    errors = []
    if value:
        if not value.isdigit():
            errors.append("SIC code can only include numbers")
        if len(value) != Validation.SIC_LENGTH:
            errors.append("Enter a SIC code that is 5 numbers long, like 12345")
        if errors:
            raise ValidationError(errors)


def validate_registration(value):
    if value:
        if len(value) != 8:
            raise ValidationError(Validation.LENGTH_REGISTRATION_NUMBER)
        if not value[2:].isdigit():
            raise ValidationError(Validation.LENGTH_REGISTRATION_NUMBER)
    return value
