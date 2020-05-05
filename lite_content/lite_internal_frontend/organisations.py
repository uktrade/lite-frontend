class OrganisationsPage:
    TITLE = "Organisations"
    ADD_BUTTON = "Add an organisation"
    ADD_HMRC_BUTTON = "Add an HMRC organisation"
    ACTIVE_FILTER_NO_ORGANISATIONS = "No organisations match your filters"

    class Tabs:
        ACTIVE = "Active"
        IN_REVIEW = "In review"
        REJECTED = "Rejected"

    class Table:
        NAME = "Name"
        TYPE = "Type"
        EORI_NUMBER = "EORI number"
        SIC_NUMBER = "SIC code"
        VAT_NUMBER = "VAT number"
        STATUS = "Status"
        EDIT = "Edit"

    class Filters:
        NAME = "name"
        TYPE = "organisation type"

        class Types:
            INDIVIDUAL = "Individual"
            COMMERCIAL = "Commercial"
            HMRC = "HMRC"


class OrganisationPage:
    BACK_LINK = "Back to " + OrganisationsPage.TITLE.lower()
    NO_FLAGS_NOTICE = "There aren't any flags"
    REVIEW_BUTTON = "Review"

    class Details:
        TITLE = "Details"
        EDIT_BUTTON = "Edit"

        class SummaryList:
            PRIMARY_SITE = "Primary site"
            FIRST_AND_LAST_NAME = "First and last name"
            NAME = "Name"
            EORI_NUMBER = "EORI number"
            SIC_NUMBER = "SIC code"
            VAT_NUMBER = "UK VAT number"
            COMPANY_REG_NUMBER = "Company registration number"
            CREATED_AT = "Created at"
            ADDRESS = "Address"
            STATUS = "Status"
            TYPE = "Type"
            FLAGS = "Flags"

    class Sites:
        TITLE = "Sites"

        class Table:
            NAME = "Name"
            ADDRESS = "Address"

    class Members:
        TITLE = "Members"

        class Table:
            NAME = "Name"
            EMAIL = "Email"
            ROLE = "Role"


class RegisterAnOrganisation:
    BACK_LINK = "Back to " + OrganisationsPage.TITLE.lower()
    COMMERCIAL_TITLE = "Register an organisation"
    INDIVIDUAL_TITLE = "Register a private individual"
    CREATE_DEFAULT_SITE = "Create a default site for this exporter"
    DEFAULT_USER = "This will be the default user for this organisation."
    EMAIL = "Email"
    NAME_OF_SITE = "Name of site"

    class CommercialOrIndividual:
        TITLE = "Commercial or private individual?"
        DESCRIPTION = ""
        COMMERCIAL_TITLE = "Commercial"
        COMMERCIAL_DESCRIPTION = ""
        INDIVIDUAL_TITLE = "Individual"
        INDIVIDUAL_DESCRIPTION = ""
        ERROR = "Select the type of organisation you're registering for"

    class WhereIsTheExporterBased:
        TITLE = "Where is the exporter based?"
        DESCRIPTION = ""
        IN_THE_UK_TITLE = "In the United Kingdom"
        IN_THE_UK_DESCRIPTION = ""
        ABROAD_TITLE = "Outside of the United Kingdom"
        ABROAD_DESCRIPTION = ""
        ERROR = "Select a location"

    class Name:
        TITLE = "Organisation name"
        DESCRIPTION = ""

    class IndividualName:
        TITLE = "First and last name"
        DESCRIPTION = ""

    class EORINumber:
        TITLE = "European Union registration and identification number (EORI)"
        DESCRIPTION = ""

    class RegistrationNumber:
        TITLE = "Company registration number (CRN)"
        DESCRIPTION = "8 numbers, or 2 letters followed by 6 numbers."

    class UkVatNumber:
        TITLE = "UK VAT number"
        DESCRIPTION = "9 digits long, with the first 2 letters indicating the country code of the registered business."

    class SicNumber:
        TITLE = "Standard industrial classification (SIC) code"
        DESCRIPTION = "Classifies industries by a 4 digit code."


class EditOrganisationPage:
    BACK_LINK = "Back to organisation"
    TITLE = "Edit organisation"
    SUBMIT_BUTTON = "Save"


class EditCommercialOrganisationPage(EditOrganisationPage):
    class Name:
        TITLE = "Organisation name"
        DESCRIPTION = ""

    class IndividualName:
        TITLE = "First and last name"
        DESCRIPTION = ""

    class EORINumber:
        TITLE = "European Union registration and identification number (EORI)"
        DESCRIPTION = ""

    class RegistrationNumber:
        TITLE = "Company registration number (CRN)"
        DESCRIPTION = "8 numbers, or 2 letters followed by 6 numbers."

    class VATNumber:
        TITLE = "UK VAT number"
        DESCRIPTION = "9 digits long, with the first 2 letters indicating the country code of the registered business."

    class SICNumber:
        TITLE = "Standard industrial classification (SIC) code"
        DESCRIPTION = "Classifies industries by a 4 digit code."


class EditIndividualOrganisationPage(EditOrganisationPage):
    class Name:
        TITLE = "First and last name"
        DESCRIPTION = ""

    class EORINumber:
        TITLE = "European Union registration and identification number (EORI)"
        DESCRIPTION = ""

    class VATNumber:
        TITLE = "UK VAT number"
        DESCRIPTION = "9 digits long, with the first 2 letters indicating the country code of the registered business."


class ReviewOrganisationPage:
    TITLE = "Review Organisation"
    DECISION_TITLE = "Final decision"
    APPROVE_OPTION = "Approve"
    REJECT_OPTION = "Reject"
    WARNING_BANNER = "There are existing organisations with matching: "

    class Summary:
        NAME = "Name"
        TYPE = "Type"
        EORI = "EORI Number"
        SIC = "SIC Code"
        VAT = "VAT Number"
        REGISTRATION = "Registration Number"
        SITE_NAME = "Primary Site Name"
        SITE_ADDRESS = "Primary Site Address"
