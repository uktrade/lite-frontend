class OrganisationsPage:
    TITLE = "Organisations"
    ADD_BUTTON = "Add an organisation"
    ACTIVE_FILTER_NO_ORGANISATIONS = "No organisations match your filters"

    class Table:
        NAME = "Name"
        TYPE = "Type"
        EORI_NUMBER = "EORI number"
        SIC_NUMBER = "SIC number"
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
    class Actions:
        BACK_TO_HMRC = "Back to hmrc organisations"
        BACK_TO_ORGS = "Back to organisations"
        EDIT = "Edit"

    class Fields:
        EORI_NUMBER = "EORI number"
        SIC_NUMBER = "SIC number"
        VAT_NUMBER = "VAT number"
        COMPANY_REG_NUMBER = "Company registration number"
        CREATED_AT = "Created at"
        ADDRESS = "Address"
        STATUS = "Status"
        TYPE = "Type"

    class Sites:
        NAME = "Name"
        ADDRESS = "Address"
        NO_SITES = "This organisation doesn't have any sites."
