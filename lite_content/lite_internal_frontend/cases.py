class CasesListPage:
    GO_TO_QUEUE = "Go to queue"
    NO_CASES = "There are no new cases to show."
    EXPORTER_AMENDMENTS_BANNER = "See what cases have changed"
    ASSIGN_USERS = "Assign Users"
    STATUS = "Status"

    class Filters:
        SHOW_FILTERS = "Show filters"
        HIDE_FILTERS = "Hide filters"
        APPLY_FILTERS = "Apply filters"
        CLEAR_FILTERS = "Clear filters"
        FILTER_BY_CASE_TYPE = "Filter by case type"
        FILTER_BY_CASE_STATUS = "Filter by case status"


class CaseDocumentsPage:
    BACK_LINK = "Back to Case"
    ATTACH = "Attach Document"
    GENERATE = "Generate Document"


class ApplicationPage:
    class Actions:
        CASE_OFFICER = "Assign Case Officer"
        DOCUMENT = "Attached Documents"
        ECJU = "ECJU Queries"
        MOVE = "Move Case"
        CHANGE_STATUS = "Change Status"
        DECISION = "Record Decision"
        ADVICE = "View Advice"
        GENERATE_DOCUMENT = "Generate Document"

    class Goods:
        MISSING_DOCUMENT_REASON_PREFIX = "No document given: "
        TITLE = "Products"

        class Table:
            CLC = "Control List Entry"
            DESCRIPTION = "Description"
            VALUE = "Quantity/Value"
            DOCUMENTS = "Documents"
            FLAGS = "Flags"
            ADVICE = "Advice"

    class Destinations:
        COUNTRY_NAME = "Country"
        PRODUCTS_CONTROL_CODES = "Goods"
        FLAGS_TABLE_HEADER = "Flags"

    class EndUser:
        NO_END_USER = "The applicant is editing the end user."

        class Table:
            Title = "End user"

    class Consignee:
        NO_CONSIGNEE = "The applicant is editing the consignee."

        class Table:
            Title = "Consignee"

    EDIT_FLAGS = "Edit products flags"
    EDIT_DESTINATION_FLAGS = "Edit destination flags"
    REVIEW_GOODS = "Review Products"
    ADVICE = "Give or change advice"
    RESPOND_BUTTON = "Respond to Query"
    CLOSED = "This case is closed"
    CASE_OFFICER = "Case Officer: "
    NO_CASE_OFFICER = "No Case Officer set."


class GenerateDocumentsPage:
    TITLE = "Generate Document"
    ERROR = "Document Generation is unavailable at this time"

    class SelectTemplateForm:
        BACK_LINK = "Back to Case Documents"

    class EditTextForm:
        HEADING = "Edit text"
        BACK_LINK = "Back to Templates"
        BACK_LINK_REGENERATE = "Back to Case Documents"
        ADD_PARAGRAPHS_LINK = "Add paragraphs"
        BUTTON = "Continue"

    class AddParagraphsForm:
        HEADING = "Add paragraphs"
        BUTTON = "Continue"


class AdditionalDocumentsPage:
    class Table:
        NAME_COLUMN = "Name"
        DOCUMENT_TYPE_COLUMN = "Type"
        DESCRIPTION_COLUMN = "Description"
        USER_COLUMN = "Added by"
        DATE_COLUMN = "Date"

    class Document:
        DOWNLOAD_LINK = "Download"
        INFECTED_LABEL = "Infected"
        PROCESSING_LABEL = "Processing"
        REGENERATE_LINK = "Regenerate"


class EndUserAdvisoriesPage:
    class Actions:
        CASE_OFFICER = "Assign Case Officer"
        CHANGE_STATUS = "Change Status"
        DOCUMENT = "Attached Documents"
        ECJU = "ECJU Queries"
        GENERATE_DOCUMENT = "Generate Document"
        MOVE = "Move Case"

    class Details:
        TITLE = "End User Details"
        NAME = "Name"
        TYPE = "Type"
        EMAIL = "Email"
        TELEPHONE = "Telephone"
        NATURE_OF_BUSINESS = "Nature of Business"
        PRIMARY_CONTACT_NAME = "Primary contact name"
        PRIMARY_CONTACT_JOB = "Primary contact job title"
        PRIMARY_CONTACT_EMAIL = "Primary contact email"
        PRIMARY_CONTACT_TELEPHONE = "Primary contact telephone"
        ADDRESS = "Address"
        WEBSITE = "Website"
        REASONING = "Reasoning behind query"
        NOTES = "Notes about end user"
        COPY_FROM = "Copied From"

    CASE_OFFICER = "Case Officer: "
    EDIT_DESTINATION_FLAGS = "Edit destination flags"
    NO_CASE_OFFICER = "No Case Officer set."


class HMRCPage:
    class Heading:
        EXPORTER = "Exporter "
        RAISED_BY = "Raised by "

    class Actions:
        CHANGE_STATUS = "Change Status"
        DOCUMENT = "Attached Documents"
        MOVE = "Move Case"
        RECORD_DECISION = "Record Decision"
        GENERATE_DOCUMENT = "Generate Document"

    class DenialReasons:
        TITLE = "Denial Reasons"
        REASON = "This case was denied because"
        FURTHER_INFO = "Further information"

    class Good:
        REVIEW_GOODS = "Review products"
        EDIT_FLAGS = "Set flags"
        DESCRIPTION = "Description"
        CONTROL_CODE = "Control list entry"
        CONTROLLED = "Controlled"
        FLAGS = "Flags"

    class SupportingDocumentation:
        TITLE = "Supporting Documentation"
        NAME = "Name"
        DESCRIPTION = "Description"
        DOCUMENT = "Document"

    CASE_FLAGS = "All Flags"


class CaseOfficerPage:
    ERROR = "There is a problem"

    class CurrentOfficer:
        TITLE = "Current case officer"
        FULLNAME = "Name"
        TEAM = "Team"
        EMAIL = "Email"
        REMOVE = "Unassign"
        BUTTON = "Unassign"

    class Error:
        GENERIC = "There appears to be a problem"
        NO_SELECTION = "Please select a user to assign"

    class Search:
        TITLE = "Assign a case officer"
        DESCRIPTION = "A case officer oversees the case for its lifespan."
        PLACEHOLDER = "Search users"
        SEARCH = "Search"
        ASSIGN = "Assign user as case officer"
        NO_RESULTS = "No users matching the criteria"


class StandardApplication:
    LICENSEE = "Licensee"
    END_USER = "End user"
    CONSIGNEE = "Consignee"
    ULTIMATE_END_USER = "Ultimate end user"
    THIRD_PARTY = "Third party"


class OpenApplication:
    SET_FLAGS = "Set flags"
    REVIEW_PRODUCTS = "Review products"


class ClcQuery:
    class Verified:
        OUTCOME = "Outcome"
        CONTROLLED = "Is the good controlled?"
        CONTROL_CODE = "What's the goods actual control list entry"
        REPORT = "Report Summary (optional)"
        COMMENT = "Why was this outcome chosen"

    class GoodDetails:
        TITLE = "Good Details"
        DESCRIPTION = "Description"
        CONTROLLED = "Controlled"
        CONTROL_CODE = "Control list entry"
        EXPECTED_CONTROL_CODE = "Expected Control list entry"
        REASON = "Reason"
        PART_NUMBER = "Part Number"
        FLAGS = "Flags"
        QUERY_TEXT = "CLC query Text"

    class Documents:
        TITLE = "Documents"
        DOWNLOAD = "Download"


class ReviewGoodsSummary:
    BACK_LINK = "Back to case"
    HEADING = "Review Goods"
    REVIEW_BUTTON = "Review and confirm item"
    SET_FLAGS = "Set goods flags"

    class Table:
        DESCRIPTION = "Description"
        REPORT_SUMMARY = "Report summary"
        CONTROLLED = "Controlled"
        CONTROL_LIST_ENTRY = "Control list entry"
        GOODS_COMMENT = "Goods comment"
        FLAGS = "Flags"
        QUANTITY_VALUE = "Quantity/Value"

    class NotSet:
        REPORT_SUMMARY = "Not Set"
        COMMENT = "Not Set"
        FLAGS = "None Set"


class EcjuQueries:
    BACK_TO_CASE = "Back to Case"
    CASE_HAS_NO_QUERIES = "This case has no ECJU Queries"
    CLOSED = "Closed queries"
    OPEN = "Open queries"
    TITLE = "ECJU Queries"

    class AddQuery:
        ADD_BUTTON_LABEL = "Add an ECJU Query"
        DESCRIPTION = (
            "Enter a full description. If your question is related to goods, then include technical"
            " details if appropriate."
        )
        DROPDOWN_DESCRIPTION = (
            "You can:<ul><li>write a new question, or</li><li>choose a question from a list</li></ul>"
        )
        DROPDOWN_TITLE = "Ask a question"
        TITLE = "Write or edit your question"


class Advice:
    ERROR = "There is a problem"
    IMPORT_ADVICE = "Import advice from picklists"
    IMPORT_PROVISO = "Import proviso from picklists"
    OTHER = "Is there anything else you want to say to the applicant? (optional)"
    REASON = "What are your reasons for this decision?"
    TEXT_ON_LICENCE = "This will appear on the generated documentation"


class Manage:
    class Documents:
        CASE_HAS_NO_DOCUMENTS = "This case has no documents"
        DESCRIPTION = "These are all the documents that have been uploaded to this case."
        DOWNLOAD_DOCUMENT = "Download document"
        PROCESSING = "Processing"
        VIRUS_INFECTED = "Virus infected"


class Tabs:
    class Activity:
        CHARACTER_LIMIT_2200 = "You can enter up to 2200 characters"
        CANCEL_POST = "Cancel"
        POST = "Post note"
