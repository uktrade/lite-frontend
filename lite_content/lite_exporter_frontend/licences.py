class LicencesList:
    NO_CONTENT_NOTICE = "No Licences found"
    TITLE = "Licences"
    DOWNLOAD_HIDDEN_TEXT = "Download file"
    BREADCRUMB = "My Licences"

    class Tabs:
        LICENCE = "Licences"
        CLEARANCE = "Clearances"
        NLR = "NLRs"

    class Filters:
        REFERENCE = "Reference"
        CLC = "CLC"
        DESTINATION_COUNTRY = "Country"
        DESTINATION_NAME = "End User"
        ACTIVE = "Current licences & clearances only"

    class Table:
        APPLICATION_COLUMN = "Your Reference"
        LICENCE_COLUMN = "Licence number"
        GOODS_COLUMN = "Product description"
        DESTINATION_COLUMN = "Destination"
        STATUS_COLUMN = "Status"
        DOCUMENTS_COLUMN = "Decision"


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
