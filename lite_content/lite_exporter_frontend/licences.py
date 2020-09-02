class LicencesList:
    NO_CONTENT_NOTICE = "No licences found"
    TITLE = "Licences"
    DOWNLOAD_HIDDEN_TEXT = "Download file"
    BREADCRUMB = "My licences"

    class Tabs:
        LICENCE = "OIELs and SIELs"
        OGLS = "OGLs"
        CLEARANCE = "Clearances"
        NLR = "NLRs"

    class Filters:
        REFERENCE = "reference"
        CLC = "control list entry"
        DESTINATION_COUNTRY = "country"
        DESTINATION_NAME = "end user"
        ACTIVE = "Current licences & clearances only"

    class Table:
        REFERENCE_COLUMN = "Reference"
        GOODS_COLUMN = "Products"
        DESTINATION_COLUMN = "Destination"
        STATUS_COLUMN = "Status"
        DOCUMENTS_COLUMN = "Decision"


class OpenGeneralLicencesList:
    WARNING_LINK = "Read [guidance on compliance and enforcement of export controls](https://www.gov.uk/government/publications/compliance-code-of-practice)"
    READ_MORE_LINK = "Read more on GOV.UK"
    SUBTITLE = "site - Registered at /sites - Registered at "
    DETAILS = "Details"
    MORE_INFORMATION = "More information"
    DOCUMENTATION_HELD_AT = "Documentation held at:"
    CONTROL_LIST_ENTRIES = "control list entry/control list entries"
    COUNTRIES = "country/countries"

    class Filters:
        NAME = "name"
        TYPE = "type"
        CONTROL_LIST_ENTRY = "control list entry"
        COUNTRY = "country"
        SITE = "site"
        ONLY_SHOW_ACTIVE = "Only show active"

    class Table:
        CAPTION = "Sites"
        REFERENCE = "Reference"
        SITE = "Site"
        STATUS = "Status"


class OpenGeneralLicenceRegistration:
    TITLE = "Registration complete"
    SECONDARY_TITLE = "You've successfully registered for **{} ({})**"

    class Links:
        VIEW_OGLS_LINK = "View your open general licences"
        APPLY_AGAIN = "Apply for another licence or clearance"
        RETURN_TO_DASHBOARD = "Return to your export control account dashboard"


class LicencePage:
    LICENCE_TITLE = "Licence"
    CLEARANCE_TITLE = "Clearance"
    ERROR = "An error occurred when trying to fetch this licence."

    class Summary:
        REFERENCE = "Your reference"
        LICENCE_DOCUMENT = "Licence"
        DOWNLOAD_LICENCE_DOCUMENT = "Download"
        STATUS = "Status"
        START_DATE = "Start date"
        END_DATE = "End date"
        DESTINATION = "Destination"
        END_USER = "End user"
        ULTIMATE_END_USERS = "Ultimate end users"
        CONSIGNEE = "Consignee"
        THIRD_PARTIES = "Third parties"
        SUPPORTING_DOCUMENTS = "Supporting documents"

    class GoodsTable:
        DETAILS = "Products"
        APPLIED_FOR = "Applied for quantity"
        LICENCED = "Licensed quantity"
        USAGE = "Used quantity"
