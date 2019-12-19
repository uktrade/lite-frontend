class PartyForm:
    class Options:
        GOVERNMENT = "Government organisation"
        COMMERCIAL = "Commercial organisation"
        INDIVIDUAL = "An individual"
        OTHER = "Other"


class EndUserForm:
    TITLE = "Select the type of end user"
    BUTTON = "Continue"
    NAME_FORM_TITLE = "Name"
    WEBSITE_FORM_TITLE = "Website address (optional)"
    ADDRESS_FORM_TITLE = "Address"
    SUBMIT_BUTTON = "Save and continue"


class UltimateEndUserForm:
    TITLE = "Select the type of ultimate recipient"
    BUTTON = "Continue"
    NAME_FORM_TITLE = "Name"
    WEBSITE_FORM_TITLE = "Website address (optional)"
    ADDRESS_FORM_TITLE = "Address"
    SUBMIT_BUTTON = "Save and continue"


class ConsigneeForm:
    TITLE = "Select the type of consignee"
    BUTTON = "Continue"
    NAME_FORM_TITLE = "Name"
    WEBSITE_FORM_TITLE = "Website address (optional)"
    ADDRESS_FORM_TITLE = "Address"
    SUBMIT_BUTTON = "Save and continue"


class ThirdPartyForm:
    class Options:
        AGENT = "Agent or broker"
        ADDITIONAL_END_USER = "End user"
        INTERMEDIATE_CONSIGNEE = "Intermediate consignee"
        SUBMITTER = "Authorised submitter"
        CONSULTANT = "Consultant"
        CONTACT = "Contact"
        EXPORTER = "Exporter"

    TITLE = "Select the type of third party"
    BUTTON = "Save and continue"
    NAME_FORM_TITLE = "Name"
    WEBSITE_FORM_TITLE = "Website address (optional)"
    ADDRESS_FORM_TITLE = "Address"
    SUBMIT_BUTTON = "Save and continue"


class GeneratedDocuments:
    TAB = "ECJU Documents"
    NO_DOCUMENTS = "There are currently no documents from ECJU."

    class Table:
        NAME_COLUMN = "Name"
        DATE_COLUMN = "Date"
        DOWNLOAD_LINK = "Download"


class ApplicationSummaryPage:
    REFERENCE_NAME = "Reference"
    TYPE = "Licence type"
    EXPORT_TYPE = "Export type"
    STATUS = "Status"
    LAST_UPDATED_AT = "Last updated"
    CREATED_AT = "Created at"
    SUBMITTED_AT = "Submitted at"
    END_USER = "End user"
    ULTIMATE_END_USERS = "Ultimate recipient"
    CONSIGNEE = "Consignee"
    THIRD_PARTIES = "Third parties"
    GOODS_LOCATIONS = "Product locations"
    SUPPORTING_DOCUMENTATION = "Supporting documentation"
    GOODS = "Products"
    COUNTRIES = "Countries"
    ON_BEHALF_OF = "On behalf of"
    OPTIONAL_NOTE = "Optional note"


class ApplicationsSummaryPage:
    REFERENCE_NAME = "Reference"
    TYPE = "Licence type"
    EXPORT_TYPE = "Export type"
    STATUS = "Status"
    LAST_UPDATED_AT = "Last updated"
    CREATED_AT = "Created at"
    SUBMITTED_AT = "Submitted at"