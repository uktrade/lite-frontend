import phonenumbers
import re

from django.core.exceptions import ValidationError

from .constants import Validation


def validate_vat(value):

    validate_vat_number_functions = {
        "UK VAT number can only include numbers and letters": lambda v: not re.match(
            Validation.LETTERS_AND_NUMBERS_ONLY, v
        ),
        "UK VAT number is too short": lambda v: len(re.sub(r"[^A-Z0-9]", "", v)) < Validation.UK_VAT_MIN_LENGTH,
        "UK VAT number is too long": lambda v: len(re.sub(r"[^A-Z0-9]", "", v)) > Validation.UK_VAT_MAX_LENGTH,
        "Enter a UK VAT number in the correct format": lambda v: not re.match(
            Validation.UK_VAT_VALIDATION_REGEX, re.sub(r"[^A-Z0-9]", "", v)
        ),
    }

    errors = []
    if value:
        errors.extend(error_message for error_message, func in validate_vat_number_functions.items() if func(value))
        if errors:
            raise ValidationError(errors)


def validate_eori(value):

    validate_eori_number_functions = {
        "EORI number can only include numbers and letters": lambda v: not re.match(
            Validation.LETTERS_AND_NUMBERS_ONLY, v
        ),
        "EORI number is too long": lambda v: len(re.sub(r"[^A-Z0-9]", "", v)) > Validation.UK_EORI_MAX_LENGTH,
        "EORI number is too short": lambda v: len(re.sub(r"[^A-Z0-9]", "", v)) < Validation.UK_EORI_MIN_LENGTH,
        "Country code can only be GB or XI": lambda v: not (
            re.sub(r"[^A-Z0-9]", "", v).startswith("GB") or re.sub(r"[^A-Z0-9]", "", v).startswith("XI")
        ),
        "Enter an EORI number in the correct format": lambda v: not re.match(
            Validation.UK_EORI_VALIDATION_REGEX, re.sub(r"[^A-Z0-9]", "", v)
        ),
    }

    errors = []
    if value:
        errors.extend(error_message for error_message, func in validate_eori_number_functions.items() if func(value))
        if errors:
            raise ValidationError(errors)


def validate_phone(value):
    errors = []
    try:
        phone_number = phonenumbers.parse(value, "GB")
        if not phonenumbers.is_valid_number(phone_number):
            errors.extend("Invalid telephone number")
    except phonenumbers.phonenumberutil.NumberParseException:
        errors.extend("Invalid telephone number")

    if errors:
        raise ValidationError(errors)


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
