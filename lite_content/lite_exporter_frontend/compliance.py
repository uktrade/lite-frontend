class OpenReturnsHelpPage:
    TITLE = "Before you start"
    BACK = "Back to hub"
    DESCRIPTION = (
        "Submit open licence returns using a CSV file that follows this [template and guidance]"
        "(https://assets.publishing.service.gov.uk/government/uploads/system/uploads/attachment_data/file/385687/14-1290-open-licence-returns.pdf).<br>"
        " You must submit open licence returns for:<br> - Open Individual Export Licences (OIELs)<br>"
        "- Open Individual Trade Control Licences (OITCLs)<br> - Open General Export Licences (OGELs)<br> - Open General Trade Control Licences (OGTCLs)"
    )
    BUTTON = "Next"


class OpenReturnsList:
    TITLE = "Open licence returns"
    SUBMIT_RETURN_BUTTON = "Submit a return"
    FILENAME_COLUMN = "Filename"
    YEAR_COLUMN = "Year of return"
    ADDED_COLUMN = "Added"


class OpenReturnsForm:
    class Year:
        TITLE = "Select the reporting year"
        DESCRIPTION = ""
        FIELD_TITLE = ""
        FIELD_DESCRIPTION = ""
        BUTTON = "Continue"
        ERROR = "Select the reporting year"
        NO_CONTENT_NOTICE = "There are no open licence returns."

    class Upload:
        TITLE = "Attach the open licence return"
        DESCRIPTION = "The file must be smaller than 1MB"
        BUTTON = "Submit"
        NO_FILE_ERROR = "Attach the open licence return file"
        MULTIPLE_FILES_ERROR = "You can only select 1 file at the same time"
        SIZE_ERROR = "The attached file must be smaller than 1MB"
        READ_ERROR = "The attached file must be a CSV"

        class ExampleTable:
            HEADING = "##Your file needs to look like the following example\n Save your file as a CSV"
            LICENCE_COLUMN = "Licence number"
            DESTINATION_COLUMN = "Destination"
            END_USER_COLUMN = "End user type"
            USAGE_COLUMN = "Usage count"
            PERIOD_COLUMN = "Period"
            LICENCE_EXAMPLE = "GBOXX20XX/XXXXX"
            DESTINATION_EXAMPLE = "Dest."
            END_USER_EXAMPLE_COLUMN = "Commercial"
            USAGE_EXAMPLE = "123"
            PERIOD_EXAMPLE = "31-DEC-YY"

    class Success:
        TITLE = "Open licence return submitted"
        DESCRIPTION = ""
        OPEN_LICENCE_RETURNS_LINK = "View open licence returns"
        HOME_LINK = "Return to your export control account dashboard"


class ComplianceSiteCaseList:
    TITLE = "Compliance"
    NONE_NOTICE = "There are no compliance's required for your organisation"

    class Table:
        REFERENCE = "Reference number"
        SITE = "Site name"
        ADDRESS = "Address"
        NEXT_VISIT = "Next visit"


class ComplianceSiteCase:
    BACK_LINK = "Back to compliance list"
    PRIMARY_SITE = "This is your organisation's registered office address"

    class Tabs:
        DETAILS = "Details"
        ECJU_QUERIES = "ECJU queries"
        VISITS = "Visits"
        NOTES = "Notes"
        GENERATED_DOCUMENTS = "Generated documents"

    class Summary:
        VISIT_DATE = "Visit Date"
        SITE_NAME = "Site Name"
        STREET = "Building and street"
        CITY = "Town or city"
        COUNTY = "County or state"
        POSTCODE = "Postcode"
        COUNTRY = "Country"

    class Visits:
        REFERENCE = "Reference number"
        DATE = "Date"
        INSPECTOR = "Inspector's name"

        NO_VISITS = "No visits have been planned yet"


class ComplianceVisitCase:
    BACK_LINK = "Back to compliance"

    class Tabs:
        ECJU_QUERIES = "ECJU queries"
        GENERATED_DOCUMENTS = "Generated documents"
