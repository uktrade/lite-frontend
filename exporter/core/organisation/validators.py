import phonenumbers

from django.core.exceptions import ValidationError

from .constants import Validation


def validate_phone(value):
    try:
        phone_number = phonenumbers.parse(value, "GB")
        if not phonenumbers.is_valid_number(phone_number):
            raise ValidationError(Validation.INVALID_PHONE_NUMBERS_ERROR_MESSAGE)
    except phonenumbers.phonenumberutil.NumberParseException:
        raise ValidationError(Validation.INVALID_PHONE_NUMBERS_ERROR_MESSAGE)
