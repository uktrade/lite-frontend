class CasesListPage:
    GO_TO_QUEUE = "Go to queue"
    NO_CASES = "There are no new cases"
    ACTIVE_FILTER_NO_CASES = "No cases match your filters"
    EXPORTER_AMENDMENTS_BANNER = "View cases that have changed"
    ASSIGN_USERS = "Assign users"
    STATUS = "Status"
    NOT_UPDATED_RECENTLY = "This case has not been updated in over 5 days"

    class Filters:
        CASE_TYPE = "type"
        CASE_STATUS = "status"
        CASE_OFFICER = "case officer"
        ASSIGNED_USER = "assigned user"
        NOT_ASSIGNED = "Not assigned"


class CaseDocumentsPage:
    BACK_LINK = "Back to case"
    ATTACH = "Attach document"
    GENERATE = "Generate document"


class ApplicationPage:
    class Info:
        CLEARANCE_LEVEL = "Security grading"
        F680_CLEARANCE_TYPES = "Clearance types"
        DESCRIPTORS = "Descriptors"

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
        OPEN_CASE_GOODS_LOCATION = "Countries"
        CASE_GOODS_LOCATION_NAME = "Name"
        CASE_GOODS_LOCATION_ADDRESS = "Address"

        class Table:
            CLC = "CLC"
            DESCRIPTION = "Description"
            VALUE = "Quantity & value"
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
        CLEARANCE_LEVEL = "Clearance"
        DESCRIPTORS = "Descriptors"
        ADDRESS = "Address"
        TYPE = "Type"
        WEBSITE = "Website"
        DOCUMENT = "Document"
        ENTITIES_INVOLVED = "Entities involved"
        NO_INACTIVE_CASES = "No inactive case entities"
        ENTITIES_DELETED = "Entities deleted by exporter"

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
    REVIEW_GOODS = "Review products"
    ADVICE = "Give or change advice"
    RESPOND_BUTTON = "Respond to query"
    CLOSED = "This case is closed"
    CASE_OFFICER = "Case officer: "
    NO_CASE_OFFICER = "No case officer set"
    NO_USERS_ASSIGNED = "No users assigned"
    NO_QUEUES_ASSIGNED = "No queues assigned"
    COPY_OF_LABEL = "Copied from:"


class GenerateDocumentsPage:
    TITLE = "Generate document"
    ERROR = "Document generation is not available at this time"

    class SelectTemplateForm:
        BACK_LINK = "Back to case documents"

    class EditTextForm:
        HEADING = "Edit text"
        BACK_LINK = "Back to templates"
        BACK_LINK_REGENERATE = "Back to case documents"
        ADD_PARAGRAPHS_LINK = "Add paragraphs"
        BUTTON = "Preview"

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
        TITLE = "End user details"
        NAME = "Name"
        TYPE = "Type"
        EMAIL = "Email"
        TELEPHONE = "Telephone"
        NATURE_OF_BUSINESS = "Nature of business"
        PRIMARY_CONTACT_NAME = "Contact name"
        PRIMARY_CONTACT_JOB = "Job title"
        PRIMARY_CONTACT_EMAIL = "Email"
        PRIMARY_CONTACT_TELEPHONE = "Telephone"
        ADDRESS = "Address"
        WEBSITE = "Website"
        REASONING = "Reason for query"
        NOTES = "Notes about the end user"
        COPY_FROM = "Copied from"

    CASE_OFFICER = "Case officer: "
    EDIT_DESTINATION_FLAGS = "Edit destination flags"
    NO_CASE_OFFICER = "No case officer set"


class HMRCPage:
    class Heading:
        EXPORTER = "Exporter "
        RAISED_BY = "Raised by "

    class DenialReasons:
        TITLE = "Denial reasons"
        REASON = "This case was denied because"
        FURTHER_INFO = "Further information"

    class Good:
        TITLE = "Goods"
        REVIEW_GOODS = "Review goods"
        EDIT_FLAGS = "Set flags"
        DESCRIPTION = "Description"
        CONTROL_CODE = "Control list entry"
        CONTROLLED = "Controlled"
        FLAGS = "Flags"

    class GoodsLocation:
        GOODS_DEPARTED = "Goods have already left the UK"
        TITLE = "Goods locations"
        CASE_GOODS_LOCATION_NAME = "Name"
        CASE_GOODS_LOCATION_ADDRESS = "Address"

    class SupportingDocumentation:
        TITLE = "Supporting documents"
        NAME = "Name"
        DESCRIPTION = "Description"
        DOCUMENT = "Document"

    CASE_FLAGS = "All flags"


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

    class Search:
        TITLE = "Assign a case officer"
        DESCRIPTION = " "
        PLACEHOLDER = "Search users"
        SEARCH = "Search"
        ASSIGN = "Assign user as case officer"
        NO_RESULTS = "No users matching the criteria"


class StandardApplication:
    LICENSEE = "Licensee"
    END_USER = "End user"
    CONSIGNEE = "Consignee"
    ULTIMATE_END_USER = "Ultimate recipient"
    THIRD_PARTY = "Third party"


class OpenApplication:
    SET_FLAGS = "Set flags"
    REVIEW_PRODUCTS = "Review products"


class ClcQuery:
    class Actions:
        RESPOND_CLC = "Respond to CLC query"
        RESPOND_GRADING = "Respond to PV grading request"

    class Verified:
        OUTCOME = "Outcome"

        class Clc:
            TITLE = "CLC query"
            CONTROLLED = "Are the goods controlled?"
            CONTROL_CODE = "What's the goods actual control list classification"
            REPORT = "Report summary (optional)"
            COMMENT = "Why was this outcome chosen"

        class PvGrading:
            TITLE = "PV grading request"
            GRADING = "Grading"
            COMMENT = "Comment"

    class GoodDetails:
        class Details:
            TITLE = "Goods details"
            DESCRIPTION = "Description"
            PART_NUMBER = "Part number"
            FLAGS = "Flags"

        class Clc:
            TITLE = "Control list classification"
            CONTROLLED = "Controlled"
            CONTROL_CODE = "Control list classification"
            EXPECTED_CONTROL_CODE = "Expected CLC"
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
    WARNING = "You will not be able to change this once submitted"
    SUBMIT = "Submit response"
    CHANGE = "Change response"

    class Details:
        DESCRIPTION = "Description"
        CONTROL_LIST_ENTRY = "Control list classification"
        PART_NUMBER = "Part number"

        class Flags:
            FLAGS = "Flags"
            EDIT = "Edit goods flags"
            SET = "Set a flag on this good"

        class Documents:
            DOCUMENTS = "Documents"
            DOWNLOAD = "Download"
            NONE = "This good has no attached documents."

    class Response:
        TITLE = "What you've said"
        CONTROLLED = "Is this good controlled?"
        CONTROL_LIST_ENTRY = "Control list classification"
        REPORT_SUMMARY = "Report summary (optional)"
        COMMENT = "Comment (optional)"


class GradingResponseOverview:
    TITLE = "Response overview"
    WARNING = "You will not be able to change this once submitted"
    SUBMIT = "Submit response"
    CHANGE = "Change response"

    class Details:
        PRODUCT_HEADING = "Goods details"
        DESCRIPTION = "Description"
        PART_NUMBER = "Part number"

        CONTROL_HEADING = "Control code"
        CONTROL_LIST_ENTRY = "Control list classification"

        class Flags:
            FLAGS = "Flags"
            EDIT = "Edit goods flags"
            SET = "Set a flag on this good"

        class Documents:
            DOCUMENTS = "Documents"
            DOWNLOAD = "Download"
            NONE = "This good has no attached documents."

    class Response:
        TITLE = "What you've said"
        PREFIX = "Prefix (optional)"
        GRADING = "Grading"
        SUFFIX = "Suffix (optional)"
        COMMENT = "Comment (optional)"


class RespondClCQueryForm:
    TITLE = "Respond to CLC query"
    BUTTON = "Continue to overview"
    BACK = "Back to case"

    CONTROL_LIST_ENTRY = "What is the correct control list classification?"
    COMMENT = "Goods comment (optional)"

    class Summary:
        DESCRIPTION = "Description"
        CONTROL_LIST_ENTRY = "Control list classification"
        NO_CONTROL_LIST_ENTRY = "N/A"

    class Controlled:
        TITLE = "Is this good controlled?"
        YES = "Yes"
        NO = "No"

    class ReportSummary:
        TITLE = "Which report summary would you like to use? (optional)"
        DESCRIPTION = "You only need to do this if the good is controlled"


class RespondGradingQueryForm:
    TITLE = "Respond to PV grading request"
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
    SUCCESS_MESSAGE = "Case status successfully changed"


class ReviewGoodsSummary:
    BACK_LINK = "Back to case"
    HEADING = "Review goods"
    REVIEW_BUTTON = "Review and confirm goods"
    SET_FLAGS = "Set goods flags"

    class Table:
        DESCRIPTION = "Description"
        REPORT_SUMMARY = "Report summary"
        CONTROLLED = "Controlled"
        CONTROL_LIST_ENTRY = "Control list classification"
        GOODS_COMMENT = "Goods comment"
        FLAGS = "Flags"
        QUANTITY_VALUE = "Quantity & value"

    class NotSet:
        REPORT_SUMMARY = "Not Set"
        COMMENT = "Not Set"
        FLAGS = "None Set"


class EcjuQueries:
    BACK_TO_CASE = "Back to case"
    CASE_HAS_NO_QUERIES = "This case has no ECJU queries"
    CLOSED = "Closed queries"
    OPEN = "Open queries"
    TITLE = "ECJU queries"

    class AddQuery:
        ADD_BUTTON_LABEL = "Add an ECJU query"
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
        TITLE = "Case documents"

        class AttachDocuments:
            BACK_TO_CASE_DOCUMENTS = "Back to case documents"
            BUTTON = "Attach document"
            DESCRIPTION = "Files must be smaller than 100MB"
            DESCRIPTION_FIELD_DETAILS = "optional"
            DESCRIPTION_FIELD_TITLE = "Document description"
            FILE_TOO_LARGE = "The selected file must be smaller than 100MB"
            TITLE = "Attach a document to this case"

    class MoveCase:
        TITLE = "Where do you want to move this case?"
        DESCRIPTION = ""
        SUCCESS_MESSAGE = "Case moved successfully"

    class AssignUsers:
        DESCRIPTION = ""
        MULTIPLE_TITLE = "Which users do you want to assign to these cases?"
        MULTIPLE_WARNING = "Users already assigned to these cases will be overwritten."
        TITLE = "Which users do you want to assign to this case?"
        BUTTON = "Submit"

    class AssignCaseOfficer:
        TITLE = "Assign a case officer"
        DESCRIPTION = ""
        DELETE_BUTTON = "Unassign existing case officer only"
        SUBMIT_BUTTON = "Submit"


class Tabs:
    class Activity:
        TITLE = "Add case note"
        CHARACTER_LIMIT_2200 = "Enter up to 2200 characters"
        CANCEL_POST = "Cancel"
        POST = "Post note"
        MAKE_VISIBLE_TO_EXPORTER = "Make visible to exporter"


class ReviewGoodsForm:
    BACK_LINK = "Back to review goods"
    CONFIRM_BUTTON = "Add to case"
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
        GOOD_TITLE = "Goods"
        COUNTRIES_TITLE = "Countries"
        APPROVE_TITLE = "Approve"
        REJECT_TITLE = "Reject"
        REFUSE_TITLE = "Refuse"
        NLR_TITLE = "No licence required"
        HIDDEN_NLR_TITLE = "No licence required for"


class FinaliseLicenceForm:
    APPROVE_TITLE = "Approve"
    FINALISE_TITLE = "Finalise"
    DATE_DESCRIPTION = "For example, 27 3 2019"
    DATE_TITLE = "Licence start date"
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
    USER_ADVICE = "User advice"
    TEAM_ADVICE = "Team advice"
    FINAL_ADVICE = "Final advice"

    class Actions:
        GIVE_OR_CHANGE = "Give or change advice"
        CLEAR = "Clear advice"
        FINALISED_GOODS_AND_COUNTRIES = "Finalise goods and countries"
        FINALISE = "Finalise"
        COMBINE_TEAM_ADVICE = "Combine all team advice"

    class EndUserTable:
        HEADING = "End user"
        NAME_COLUMN = "Name"
        TYPE_COLUMN = "Type"
        ADDRESS_COLUMN = "Address"
        WEBSITE_COLUMN = "Website"
        DOCUMENT_COLUMN = "Document"
        ADVICE_COLUMN = "Advice"

    class ConsigneeTable:
        HEADING = "Consignee"
        NAME_COLUMN = "Name"
        TYPE_COLUMN = "Type"
        ADDRESS_COLUMN = "Address"
        WEBSITE_COLUMN = "Website"
        DOCUMENT_COLUMN = "Document"
        ADVICE_COLUMN = "Advice"

    class UltimateEndUserTable:
        HEADING = "Ultimate recipient"
        NAME_COLUMN = "Name"
        TYPE_COLUMN = "Type"
        ADDRESS_COLUMN = "Address"
        WEBSITE_COLUMN = "Website"
        DOCUMENT_COLUMN = "Document"
        ADVICE_COLUMN = "Advice"

    class ThirdPartyTable:
        HEADING = "Third parties"
        NAME_COLUMN = "Name"
        TYPE_COLUMN = "Type"
        ROLE_COLUMN = "Role"
        ADDRESS_COLUMN = "Address"
        WEBSITE_COLUMN = "Website"
        DOCUMENT_COLUMN = "Document"
        ADVICE_COLUMN = "Advice"
