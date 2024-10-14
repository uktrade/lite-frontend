import re
import phonenumbers

from django.core.exceptions import ValidationError

from .constants import Validation


def validate_vat(value):
    errors = []
    if value:
        if not re.match(Validation.LETTERS_AND_NUMBERS_ONLY, value):
            errors.append("UK VAT number can only include numbers and letters")
        stripped_vat = re.sub(r"[^A-Z0-9]", "", value)
        if len(stripped_vat) < Validation.UK_VAT_MIN_LENGTH:
            errors.append("UK VAT number is too short")
        if len(stripped_vat) > Validation.UK_VAT_MAX_LENGTH:
            errors.append("UK VAT number is too long")
        if not re.match(Validation.UK_VAT_VALIDATION_REGEX, stripped_vat):
            errors.append("Enter a UK VAT number in the correct format")


def validate_eori(value):
    errors = []
    if value:
        if not re.match(Validation.LETTERS_AND_NUMBERS_ONLY, value):
            errors.append("EORI number can only include numbers and letters")
        stripped_eori = re.sub(r"[^A-Z0-9]", "", value)
        if len(stripped_eori) > Validation.UK_EORI_MAX_LENGTH:
            errors.append("EORI number is too long")
        if len(stripped_eori) < Validation.UK_EORI_MIN_LENGTH:
            errors.append("EORI number is too short")
        if not (stripped_eori.startswith("GB") or stripped_eori.startswith("XI")):
            errors.append("Country code can only be GB or XI")
        if not re.match(Validation.LETTERS_AND_NUMBERS_ONLY, stripped_eori):
            errors.append("EORI number can only include numbers and letters")
        if not re.match(Validation.UK_EORI_VALIDATION_REGEX, stripped_eori):
            errors.append("Enter an EORI number in the correct format")

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
