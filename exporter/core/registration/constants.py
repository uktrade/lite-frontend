class RegistrationSteps:
    REGISTRATION_TYPE = "REGISTRATION_TYPE"
    UK_BASED = "UK_BASED"
    INDIVIDUAL_DETAILS = "INDIVIDUAL_DETAILS"
    ADDRESS_DETAILS = "ADDRESS_DETAILS"


class Validation:
    UK_EORI_VALIDATION_REGEX = r"^(GB|XI)([0-9]{12}|[0-9]{15})$"
    UK_EORI_MAX_LENGTH = 17
    # Matches GB followed by 9/12 digits or GB followed by GD/HA and 3 digits
    UK_VAT_VALIDATION_REGEX = r"^(GB|XI)?([0-9]{9}([0-9]{3})?|(GD|HA)[0-9]{3})$"
    UK_VAT_MAX_LENGTH = 17
    UK_VAT_MIN_LENGTH = 7
