import re


class RegistrationSteps:
    REGISTRATION_TYPE = "REGISTRATION_TYPE"
    UK_BASED = "UK_BASED"
    REGISTRATION_DETAILS = "REGISTRATION_DETAILS"
    ADDRESS_DETAILS = "ADDRESS_DETAILS"
    REGISTRATION_CONFIRMATION = "REGISTRATION_CONFIRMATION"


class Validation:
    UK_EORI_VALIDATION_REGEX = r"^(GB|XI)([0-9]{12}|[0-9]{15})$"
    UK_EORI_MAX_LENGTH = 17
    UK_EORI_MIN_LENGTH = 14
    LETTERS_AND_NUMBERS_ONLY = r"^[a-zA-Z0-9]+$"
    # Matches GB followed by 9/12 digits or GB followed by GD/HA and 3 digits
    UK_VAT_VALIDATION_REGEX = r"^(GB|XI)?([0-9]{9}([0-9]{3})?|(GD|HA)[0-9]{3})$"
    UK_VAT_MAX_LENGTH = 11
    UK_VAT_MIN_LENGTH = 9
    SIC_LENGTH = 5
    LENGTH_REGISTRATION_NUMBER = "Registration numbers are 8 numbers long"

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
