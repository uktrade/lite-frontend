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
        ADDRESS = "Address"

    class Filters:
        NAME = "name"
        TYPE = "organisation type"

        class Types:
            INDIVIDUAL = "Individual"
            COMMERCIAL = "Commercial"
            HMRC = "HMRC"
