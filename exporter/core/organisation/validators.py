import phonenumbers
import re

from django.core.exceptions import ValidationError

from .constants import Validation


def validate_vat(value):

    validate_vat_number_functions = {
        Validation.UK_VAT_LETTERS_AND_NUMBERS_ERROR_MESSAGE: lambda v: not re.match(
            Validation.LETTERS_AND_NUMBERS_ONLY, v
        ),
        Validation.UK_VAT_MIN_LENGTH_ERROR_MESSAGE: lambda v: len(re.sub(Validation.STRIPPED_VALUE, "", v))
        < Validation.UK_VAT_MIN_LENGTH,
        Validation.UK_VAT_MAX_LENGTH_ERROR_MESSAGE: lambda v: len(re.sub(Validation.STRIPPED_VALUE, "", v))
        > Validation.UK_VAT_MAX_LENGTH,
        Validation.UK_VAT_VALIDATION_ERROR_MESSAGE: lambda v: not re.match(
            Validation.UK_VAT_VALIDATION_REGEX, re.sub(Validation.STRIPPED_VALUE, "", v)
        ),
    }

    errors = []
    if value:
        errors.extend(error_message for error_message, func in validate_vat_number_functions.items() if func(value))
        if errors:
            raise ValidationError(errors)


def validate_eori(value):

    validate_eori_number_functions = {
        Validation.UK_EORI_LETTERS_AND_NUMBERS_ERROR_MESSAGE: lambda v: not re.match(
            Validation.LETTERS_AND_NUMBERS_ONLY, v
        ),
        Validation.UK_EORI_MAX_LENGTH_ERROR_MESSAGE: lambda v: len(re.sub(Validation.STRIPPED_VALUE, "", v))
        > Validation.UK_EORI_MAX_LENGTH,
        Validation.UK_EORI_MIN_LENGTH_ERROR_MESSAGE: lambda v: len(re.sub(Validation.STRIPPED_VALUE, "", v))
        < Validation.UK_EORI_MIN_LENGTH,
        Validation.UK_EORI_STARTING_LETTERS_ERROR_MESSAGE: lambda v: not (
            re.sub(Validation.STRIPPED_VALUE, "", v).startswith("GB")
            or re.sub(Validation.STRIPPED_VALUE, "", v).startswith("XI")
        ),
        Validation.UK_EORI_VALIDATION_ERROR_MESSAGE: lambda v: not re.match(
            Validation.UK_EORI_VALIDATION_REGEX, re.sub(Validation.STRIPPED_VALUE, "", v)
        ),
    }

    errors = []
    if value:
        errors.extend(error_message for error_message, func in validate_eori_number_functions.items() if func(value))
        if errors:
            raise ValidationError(errors)


def validate_phone(value):
    try:
        phone_number = phonenumbers.parse(value, "GB")
        if not phonenumbers.is_valid_number(phone_number):
            raise ValidationError(Validation.INVALID_PHONE_NUMBERS_ERROR_MESSAGE)
    except phonenumbers.phonenumberutil.NumberParseException:
        raise ValidationError(Validation.INVALID_PHONE_NUMBERS_ERROR_MESSAGE)


def validate_sic_number(value):

    validate_sic_number_functions = {
        Validation.SIC_NUMBERS_ONLY_ERROR_MESSAGE: lambda v: not v.isdigit(),
        Validation.SIC_NUMBER_LENGTH_ERROR_MESSAGE: lambda v: len(v) != Validation.SIC_LENGTH,
    }
    errors = []
    if value:
        errors.extend(error_message for error_message, func in validate_sic_number_functions.items() if func(value))
        if errors:
            raise ValidationError(errors)


def validate_registration(value):
    if value:
        if len(value) != 8:
            raise ValidationError(Validation.LENGTH_REGISTRATION_NUMBER)
        if not value[2:].isdigit():
            raise ValidationError(Validation.LENGTH_REGISTRATION_NUMBER)
    return value
