class OpenReturnsHelpPage:
    TITLE = "Before you start"
    BACK = "Back to hub"
    DESCRIPTION = """Submit open licence returns using a csv file that follows this [template and guidance](https://assets.publishing.service.gov.uk/government/uploads/system/uploads/attachment_data/file/385687/14-1290-open-licence-returns.pdf).\n
     You must submit open licence returns for:\n
     - Open Individual Export Licences (OIELs)\n - Open Individual Trade Control Licences (OITCLs)\n - Open General Export Licences (OGELs)\n - Open General Trade Control Licences (OGTCLs)
     """  # noqa
    FORMATTING_HELP_LINK = "Format your open licence returns csv"
    FORMATTING_HELP_DETAILS = """The first row must contain column headers, or be blank. It must not contain returns data.\n
     Columns must start from column A and be in the following order:\n

    - Licence number\n - Destination\n - End user type\n - Usage count\n - Period\n

    Licence number must be in one of the following formats:\n

    - GBOXX20XX/XXXXX. For example GBOIE2020/00001)\n - GBOXX20XX/XXXXX/X for amended licences. For example GBOIE2020/00001/A\n

    Destination names must be entered exactly as they appear on the licence.\n
    \n

    End user type must be one of the following, entered exactly as shown here:\n

    - Government\n - Commercial\n - Pvt Indiv\n - Other\n

    Usage count must be a positive integer.\n
    \n

    Period must be in the following format, entered exactly as shown with YY replaced with the last 2 digits of the year:\n

    - 01-JAN-YY to 31-DEC-YY\n"""
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
        SECONDARY_TITLE = ""
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
    PRIMARY_SITE = "This is your organisation's primary site"

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
