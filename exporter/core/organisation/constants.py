class RegistrationSteps:
    REGISTRATION_TYPE = "REGISTRATION_TYPE"
    UK_BASED = "UK_BASED"
    REGISTRATION_DETAILS = "REGISTRATION_DETAILS"
    ADDRESS_DETAILS = "ADDRESS_DETAILS"
    REGISTRATION_CONFIRMATION = "REGISTRATION_CONFIRMATION"


class Validation:
    STRIPPED_VALUE = r"[^A-Z0-9]"
    UK_EORI_VALIDATION_REGEX = r"^(GB|XI)([0-9]{12}|[0-9]{15})$"
    LETTERS_AND_NUMBERS_ONLY = r"^[a-zA-Z0-9]+$"
    # Matches GB followed by 9/12 digits or GB followed by GD/HA and 3 digits
    UK_VAT_VALIDATION_REGEX = r"^(GB|XI)?([0-9]{9}([0-9]{3})?|(GD|HA)[0-9]{3})$"
    UK_EORI_STARTING_LETTERS_REGEX = r"^(GB|XI)"
    SIC_NUMBERs_ONLY_REGEX = r"^\d+$"

    UK_EORI_MAX_LENGTH = 17
    UK_EORI_MIN_LENGTH = 14
    UK_VAT_MAX_LENGTH = 11
    UK_VAT_MIN_LENGTH = 9
    SIC_LENGTH = 5

    UK_EORI_STARTING_LETTERS_ERROR_MESSAGE = "Country code can only be GB or XI"
    UK_EORI_VALIDATION_ERROR_MESSAGE = "Enter an EORI number in the correct format"
    UK_EORI_MAX_LENGTH_ERROR_MESSAGE = "EORI number is too long"
    UK_EORI_MIN_LENGTH_ERROR_MESSAGE = "EORI number is too short"
    UK_EORI_LETTERS_AND_NUMBERS_ERROR_MESSAGE = "EORI number can only include numbers and letters"

    UK_VAT_LETTERS_AND_NUMBERS_ERROR_MESSAGE = "UK VAT number can only include numbers and letters"
    UK_VAT_MIN_LENGTH_ERROR_MESSAGE = "UK VAT number is too short"
    UK_VAT_MAX_LENGTH_ERROR_MESSAGE = "UK VAT number is too long"
    UK_VAT_VALIDATION_ERROR_MESSAGE = "Enter a UK VAT number in the correct format"

    SIC_NUMBERS_ONLY_ERROR_MESSAGE = "SIC code can only include numbers"
    SIC_NUMBER_LENGTH_ERROR_MESSAGE = "Enter a SIC code that is 5 numbers long, like 12345"

    INVALID_PHONE_NUMBERS_ERROR_MESSAGE = "Invalid telephone number"

    LENGTH_REGISTRATION_NUMBER = "Registration numbers are 8 numbers long"
