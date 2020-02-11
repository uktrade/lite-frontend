class CasesListPage:
    GO_TO_QUEUE = "Go to queue"
    NO_CASES = "There are no new cases to show"
    ACTIVE_FILTER_NO_CASES = "There are no cases to show with those filters"
    EXPORTER_AMENDMENTS_BANNER = "See what cases have changed"
    ASSIGN_USERS = "Assign users"
    STATUS = "Status"

    class Filters:
        CASE_TYPE = "type"
        CASE_STATUS = "status"
        CASE_OFFICER = "case officer"
        ASSIGNED_USER = "assigned user"
        NOT_ASSIGNED = "Not assigned"


class CaseDocumentsPage:
    BACK_LINK = "Back to Case"
    ATTACH = "Attach Document"
    GENERATE = "Generate Document"


class ApplicationPage:
    class Actions:
        CASE_OFFICER = "Assign case officer"
        DOCUMENT = "Attached documents"
        ECJU = "ECJU queries"
        MOVE = "Move case"
        CHANGE_STATUS = "Change status"
        DECISION = "Record decision"
        ADVICE = "View advice"
        GENERATE_DOCUMENT = "Generate document"

    class Goods:
        MISSING_DOCUMENT_REASON_PREFIX = "No document given: "
        TITLE = "Products"
        CASE_GOODS_LOCATION = "Products location"
        CASE_GOODS_LOCATION_NAME = "Name"
        CASE_GOODS_LOCATION_ADDRESS = "Address"

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

    class Parties:
        SELECT_ALL = "Select all/Deselect all"
        NAME = "Name"
        ADDRESS = "Address"
        TYPE = "Type"
        WEBSITE = "Website"
        DOCUMENT = "Document"
        NO_INACTIVE_CASES = "No inactive case entities"
        INACTIVE_CASES = "Entities deleted by exporter"

    class EndUser:
        NO_END_USER = "The applicant is editing the end user."

        class Table:
            Title = "End user"

    class Consignee:
        NO_CONSIGNEE = "The applicant is editing the consignee."

        class Table:
            Title = "Consignee"

    class ThirdParty:
        ROLE = "Role: "

    EDIT_FLAGS = "Edit products flags"
    EDIT_DESTINATION_FLAGS = "Edit destination flags"
    REVIEW_GOODS = "Review Products"
    ADVICE = "Give or change advice"
    RESPOND_BUTTON = "Respond to Query"
    CLOSED = "This case is closed"
    CASE_OFFICER = "Case Officer: "
    NO_CASE_OFFICER = "No Case Officer set."
    NO_USERS_ASSIGNED = "No users assigned."
    NO_QUEUES_ASSIGNED = "No queues assigned."


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

    class DenialReasons:
        TITLE = "Denial Reasons"
        REASON = "This case was denied because"
        FURTHER_INFO = "Further information"

    class Good:
        TITLE = "Products"
        REVIEW_GOODS = "Review products"
        EDIT_FLAGS = "Set flags"
        DESCRIPTION = "Description"
        CONTROL_CODE = "Control list entry"
        CONTROLLED = "Controlled"
        FLAGS = "Flags"

    class GoodsLocation:
        GOODS_DEPARTED = "Products have already left the UK"
        TITLE = "Products location"
        CASE_GOODS_LOCATION_NAME = "Name"
        CASE_GOODS_LOCATION_ADDRESS = "Address"

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
    class Actions:
        RESPOND_CLC = "Respond to CLC query"
        RESPOND_GRADING = "Respond to grading query"

    class Verified:
        OUTCOME = "Outcome"

        class Clc:
            TITLE = "CLC query"
            CONTROLLED = "Is the good controlled?"
            CONTROL_CODE = "What's the goods actual control list entry"
            REPORT = "Report Summary (optional)"
            COMMENT = "Why was this outcome chosen"

        class PvGrading:
            TITLE = "Grading Query"
            GRADING = "Grading"
            COMMENT = "Comment"

    class GoodDetails:
        class Details:
            TITLE = "Product Details"
            DESCRIPTION = "Description"
            PART_NUMBER = "Part Number"
            FLAGS = "Flags"

        class Clc:
            TITLE = "Control list classification"
            CONTROLLED = "Controlled"
            CONTROL_CODE = "Control list entry"
            EXPECTED_CONTROL_CODE = "Expected Control list entry"
            NO_CONTROL_CODE = "Not on the control list"
            REASON = "Reason"

        class Grading:
            TITLE = "Grading"
            GRADING = "Grading"
            ISSUING_AUTHORITY = "Issuing authority"
            REFERENCE = "Reference"
            DATE_OF_ISSUE = "Date of issue"
            COMMENTS = "Comments"

        class Documents:
            TITLE = "Documents"
            DOWNLOAD = "Download"


class ClcResponseOverview:
    TITLE = "Response overview"
    WARNING = "You won't be able to change this once submitted"
    SUBMIT = "Submit response"
    CHANGE = "Change response"

    class Details:
        DESCRIPTION = "Description"
        CONTROL_LIST_ENTRY = "Control list entry"
        PART_NUMBER = "Part number"

        class Flags:
            FLAGS = "Flags"
            EDIT = "Edit good flags"
            SET = "Set a flag on this good"

        class Documents:
            DOCUMENTS = "Documents"
            DOWNLOAD = "Download"
            NONE = "This good has no documents attached."

    class Response:
        TITLE = "What you've said"
        CONTROLLED = "Is this good controlled?"
        CONTROL_LIST_ENTRY = "Control list entry"
        REPORT_SUMMARY = "Report Summary (optional)"
        COMMENT = "Comment (optional)"


class GradingResponseOverview:
    TITLE = "Response overview"
    WARNING = "You won't be able to change this once submitted"
    SUBMIT = "Submit response"
    CHANGE = "Change response"

    class Details:
        PRODUCT_HEADING = "Product details"
        DESCRIPTION = "Description"
        PART_NUMBER = "Part number"

        CONTROL_HEADING = "Control code"
        CONTROL_LIST_ENTRY = "Control list entry"

        class Flags:
            FLAGS = "Flags"
            EDIT = "Edit good flags"
            SET = "Set a flag on this good"

        class Documents:
            DOCUMENTS = "Documents"
            DOWNLOAD = "Download"
            NONE = "This good has no documents attached."

    class Response:
        TITLE = "What you've said"
        PREFIX = "Prefix (optional)"
        GRADING = "Grading"
        SUFFIX = "Suffix (optional)"
        COMMENT = "Comment (optional)"


class RespondClCQueryForm:
    TITLE = "Respond to CLC Query"
    BUTTON = "Continue to overview"
    BACK = "Back to case"

    CONTROL_LIST_ENTRY = "What is the correct control list entry?"
    COMMENT = "Good's comment (optional)"

    class Summary:
        DESCRIPTION = "Description"
        CONTROL_LIST_ENTRY = "Control list entry"
        NO_CONTROL_LIST_ENTRY = "N/A"

    class Controlled:
        TITLE = "Is this good controlled?"
        YES = "Yes"
        NO = "No"

    class ReportSummary:
        TITLE = "Which report summary would you like to use? (optional)"
        DESCRIPTION = "You only need to do this if the item is controlled"


class RespondGradingQueryForm:
    TITLE = "Respond to grading query"
    BUTTON = "Continue to overview"
    BACK = "Back to case"

    COMMENT = "Comment"

    class Grading:
        PREFIX = "Prefix"
        GRADING = "Grading"
        SUFFIX = "Suffix"


class ChangeStatusPage:
    TITLE = "Change case status"
    DESCRIPTION = ""
    SUCCESS_MESSAGE = "You've changed the case status successfully"


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
        TITLE = "Case Documents"

        class AttachDocuments:
            BACK_TO_CASE_DOCUMENTS = "Back to Case Documents"
            BUTTON = "Attach Document"
            DESCRIPTION = "Maximum size: 100MB per file"
            DESCRIPTION_FIELD_DETAILS = "optional"
            DESCRIPTION_FIELD_TITLE = "Document description"
            FILE_TOO_LARGE = "The file you tried to upload was too large."
            TITLE = "Attach a document to this case"

    class MoveCase:
        TITLE = "Where do you want to move this case?"
        DESCRIPTION = "Select all queues that apply."
        SUCCESS_MESSAGE = "You've moved the case successfully"

    class AssignUsers:
        DESCRIPTION = "Select all users that apply."
        MULTIPLE_TITLE = "Which users do you want to assign to these cases?"
        MULTIPLE_WARNING = "Users already assigned to these cases will be overwritten."
        TITLE = "Which users do you want to assign to this case?"


class Tabs:
    class Activity:
        TITLE = "Add case note"
        CHARACTER_LIMIT_2200 = "You can enter up to 2200 characters"
        CANCEL_POST = "Cancel"
        POST = "Post note"
        MAKE_VISIBLE_TO_EXPORTER = "Make visible to exporter"


class ReviewGoodsForm:
    BACK_LINK = "Back to review goods"
    CONFIRM_BUTTON = "Add to Case"
    HEADING = "Check control list classification and add report summary"


class GoodsDecisionMatrixPage:
    ERROR = "There is a problem"
    NO_ADVICE_DEFAULT = "No advice"
    REFUSE_ADVICE_TAG = "(Reject)"

    class Actions:
        BACK_TO_FINAL_ADVICE = "Back to final advice"
        SELECT_DECISION = "Select a decision for each good and country combination"
        FINALISE_BUTTON = "Finalise"
        SAVE_BUTTON = "Save"

    class Table:
        GOOD_TITLE = "Good"
        COUNTRIES_TITLE = "Countries"
        APPROVE_TITLE = "Approve"
        REJECT_TITLE = "Reject"
        REFUSE_TITLE = "Refuse"
        NLR_TITLE = "No licence required"
        HIDDEN_NLR_TITLE = "No licence required for"


class FinaliseLicenceForm:
    APPROVE_TITLE = "Approve"
    FINALISE_TITLE = "Finalise"
    DATE_DESCRIPTION = "For example, 27 3 2007"
    DATE_TITLE = "When will the licence start?"
    DURATION_DESCRIPTION = "This must be a whole number of months, such as 12"
    DURATION_TITLE = "How long will it last?"

    class Actions:
        BACK_TO_ADVICE_BUTTON = "Back to final advice"
        BACK_TO_DECISION_MATRIX_BUTTON = "Back to finalise goods and countries"


class AdviceRecommendationForm:
    TITLE = "What do you advise?"
    DESCRIPTION = "You can advise to:"

    class Actions:
        CONTINUE_BUTTON = "Continue"
        BACK_BUTTON = "Back to advice"

    class RadioButtons:
        GRANT = "Grant the licence"
        PROVISO = "Add a proviso"
        NLR = "Tell the applicant they do not need a licence"
        NOT_APPLICABLE = "Not applicable"
        REJECT = "Reject the licence"
        REFUSE = "Refuse the licence"


class AdvicePage:
    PROVISO_TITLE = "Proviso"
    DENIAL_REASONS_TITLE = "Denial reasons"
    REASON_FOR_ADVICE_TITLE = "Reason for this advice"
    NOTE_TO_APPLICANT_TITLE = "Note to applicant"

    class Table:
        REJECT = "Reject"
        ADVICE_BY = "advice by"
        AT = "at"


class ViewAdvicePage:
    USER_ADVICE = "User Advice"
    TEAM_ADVICE = "Team Advice"
    FINAL_ADVICE = "Final Advice"

    class Actions:
        GIVE_OR_CHANGE = "Give or change advice"
        CLEAR = "Clear advice"
        FINALISED_GOODS_AND_COUNTRIES = "Finalise goods and countries"
        FINALISE = "Finalise"
        COMBINE_TEAM_ADVICE = "Combine all team advice"
