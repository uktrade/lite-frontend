class CasesListPage:
    GO_TO_QUEUE = "Go to queue"
    NO_CASES = "There are no new cases"
    ACTIVE_FILTER_NO_CASES = "No cases match your filters"
    EXPORTER_AMENDMENTS_BANNER = "View cases that have changed"
    ASSIGN_USERS = "Assign users"
    STATUS = "Status"
    NOT_UPDATED_RECENTLY = "This case has not been updated in over 5 days"
    OPEN_TEAM_ECJU = "This case contains open enquiries by your team"
    FUTURE_REVIEW_DATE = "This case has a next review date set in the future"
    OPEN_ALL = "Open all"
    CLOSE_ALL = "Close all"

    class Table:
        SLA = "SLA"
        INFORMATION = "Information"
        CASE = "Case"
        ASSIGNEES = "Assignees"
        GOODS = "Goods"
        DESTINATIONS = "Destinations"
        FLAGS = "Flags"

    class NoContent:
        NO_GOODS_FLAGS = "No good flags set"
        NO_DESTINATION_FLAGS = "No destination flags set"
        NO_FLAGS = "No flags set"
        NO_USERS_ASSIGNED = "No users assigned"

    class Filters:
        CASE_TYPE = "type"
        CASE_STATUS = "status"
        CASE_OFFICER = "case officer"
        ASSIGNED_USER = "assigned user"
        NOT_ASSIGNED = "Not assigned"
        HIDDEN = "Show hidden cases, including cases with open ECJU queries."
        EXPORTER_APPLICATION_REFERENCE = "exporter application reference"
        ORGANISATION_NAME = "organisation name"
        EXPORTER_SITE_NAME = "exporter site name"
        EXPORTER_SITE_ADDRESS = "exporter site address"
        FINAL_ADVICE_TYPE = "final advice type"
        TEAM_ADVICE_TYPE = "team advice type"
        MAX_SLA_DAYS_REMAINING = "max SLA days remaining"
        MIN_SLA_DAYS_REMAINING = "min SLA days remaining"
        SLA_DAYS_ELAPSED = "SLA days elapsed"
        SUBMITTED_FROM = "submitted from"
        SUBMITTED_TO = "submitted to"
        FINALISED_FROM = "finalised from"
        FINALISED_TO = "finalised to"
        PARY_NAME = "party name"
        PARTY_ADDRESS = "party address"
        GOODS_RELATED_DESCRIPTION = "goods related description"
        COUNTRY = "country"
        CONTROL_LIST_ENTRY = "control list entry"
        FLAGS = "flags"
        SORT_BY_SLA_ELAPSED = "sorted by SLA days"
        SORT_BY_SLA_ELAPSED_ASCENDING = "Ascending"
        SORT_BY_SLA_ELAPSED_DESCDENDING = "Descending"

    class EnforcementXML:
        EXPORT_BUTTON = "Export EU XML"
        IMPORT_BUTTON = "Import EU XML"

        class Export:
            NO_CASES = "No matching cases found"
            GENERIC_ERROR = "An error occurred when generating XML for this queue."


class CasePage:
    IM_DONE_BUTTON = "I'm done"
    EDIT_FLAGS_LINK = "Edit <!--case--> flags"

    class Pills:
        class Goods:
            GOOD = "good"

        class Destinations:
            DESTINATION = "destination"

        class Flags:
            FLAG = "flag"

        class CaseOfficer:
            CASE_OFFICER = "Case officer"
            INSPECTOR = "Inspector"
            ASSIGNED_USERS = "Assigned users"
            NO_CASE_OFFICER = "No case officer assigned"
            NO_INSPECTOR = "No inspector assigned"
            NO_USERS_ASSIGNED = "No users assigned"

        class OpenGeneralLicence:
            READ_ON_GOVUK_LINK = "Read on GOV.UK"

        class Status:
            TITLE = "Latest status change"
            NOTICE = "This isn't available here."

    class Tabs:
        DETAILS = "Details"
        ADVICE_AND_DECISION = "Advice and decision"
        USER_ADVICE = "User advice"
        TEAM_ADVICE = "Team advice"
        FINAL_ADVICE = "Final decision"
        ECJU_QUERIES = "Queries"
        DOCUMENTS = "Documents"
        ADDITIONAL_CONTACTS = "Contacts"
        CASE_NOTES_AND_TIMELINE = "Notes and timeline"
        LICENCES = "Licences"

    class LicencesTab:
        REFERENCE_COLUMN = "Licence"
        PRODUCTS_COLUMN = "Products"
        USAGE_COLUMN = "Usage"
        STATUS_COLUMN = "Status"
        NO_CONTENT_NOTICE = "No licences on application"

    class DetailsTab:
        ADMINISTRATIVE_CENTRE = "Administrative Centre"
        EXPORTER_REFERENCE = "Exporter reference"
        SUBMITTED_AT = "Submitted at"
        SUBMITTED_BY = "Submitted by"
        STATUS = "Status"
        ASSIGNED_QUEUES = "Assigned queues"
        TYPE = "Type"
        LAST_UPDATED = "Last updated"
        CASE_OFFICER = "Case officer"
        ASSIGNED_USERS = "Assigned users"
        COPY_OF = "Copy of"
        RAISED_BY = "Raised by"
        EXPORT_TYPE = "Export type"
        SECURITY_GRADING = "Security grading"
        GOODS_CATEGORY = "Goods category"
        CLEARANCE_TYPES = "Clearance types"
        NO_QUEUES_ASSIGNED = "Not assigned to any queues"
        NO_USERS_ASSIGNED = "No users assigned"
        NO_CASE_OFFICER = "Not assigned"
        TRADE_CONTROL_ACTIVITY = "Trade control activity"
        TRADE_CONTROL_ACTIVITY_CATEGORIES = "Trade control activity categories"
        INSPECTOR = "Inspector"
        ADDRESS = "Address"
        NEXT_REVIEW_DATE = "Next review date"
        NO_NEXT_REVIEW_DATE = "No review date set"

        class Goods:
            TITLE = "good"
            TITLE_PLURAL = "goods"

            class Table:
                DESCRIPTION = "Description"
                CONTROLLED = "Controlled"
                CONTROL_LIST_ENTRIES = "Control list entries"
                INCORPORATED = "Incorporated"

        class Destinations:
            TITLE = "destination"
            TITLE_PLURAL = "destinations"

            class Table:
                COUNTRY = "Country"
                COUNTRY_CODE = "Country code"
                GOODS = "Goods"
                TYPE = "Type"
                NAME = "Name"
                CLEARANCE = "Clearance"
                DESCRIPTORS = "Descriptors"
                ADDRESS = "Address"
                BUSINESS = "Business"
                WEBSITE = "Website"
                DOCUMENTS = "Documents"
                SIGNATORY_NAME = "Signatory name"
                FLAGS = "Flags"

        class EndUseDetails:
            TITLE = "End use details"

            class Table:
                DESCRIPTION = "Description"
                ANSWER = "Answer"

        class Site:
            TITLE = "Site"
            DETAILS = "Details"
            RECORDS_HELD_AT = "Records held at"
            RECORDS_HELD_ON_SITE = "Records held on site"

        class OpenGeneralLicence:
            NAME = "Name"
            DESCRIPTION = "Description"
            CONTROL_LIST_ENTRIES = "Control list entries"
            COUNTRIES = "Countries"
            MORE_INFORMATION = "More information"
            VIEW_ON_LITE_LINK = "View on LITE"

        class RouteOfGoods:
            TITLE = "Route of goods"

            class Table:
                DESCRIPTION = "Description"
                ANSWER = "Answer"

        class SupportingDocumentation:
            TITLE = "Supporting documentation"

            class Table:
                pass
                # NEED TO DO! REMIND ME!

        class VisitReports:
            ADD = "Add a visit report"
            NO_VISIT_REPORTS = "There are no visit reports"
            REPORT_REFERENCE = "Report reference"
            VISIT_DATE = "Visit date"
            INSPECTOR = "Inspector"
            FLAGS = "Flags"

        class ComplianceVisitDetails:
            class VisitReportDetails:
                TITLE = "Visit report details"
                VISIT_TYPE = "Visit type"
                VISIT_DATE = "Visit date"
                OVERALL_RISK = "Overall risk value"
                LICENCE_RISK = "Licence risk value"
                EDIT = "Edit"

            class PeoplePresent:
                TITLE = "People present"
                NAME = "Name"
                JOB_TITLE = "Job title"
                ADD = "Add"
                EDIT = "Edit"
                REMOVE = "Remove"
                NO_PEOPLE_PRESENT = "There are no people present added"
                ADD_A_PERSON = "Add a person"

            class Overview:
                TITLE = "Overview"
                EDIT = "Edit"

            class Inspection:
                TITLE = "Inspection"
                EDIT = "Edit"

            class ComplianceWithLicences:
                TITLE = "Compliance with licences"
                OVERVIEW = "Overview"
                RISK_VALUE = "Risk value"
                EDIT = "Edit"

            class KnowledgeOfIndividuals:
                TITLE = "Knowledge and Understanding demonstrated by key export individuals at meeting"
                OVERVIEW = "Overview"
                RISK_VALUE = "Risk value"
                EDIT = "Edit"

            class KnowledgeOfControlledProducts:
                TITLE = "Knowledge of controlled items in their business' products"
                OVERVIEW = "Overview"
                RISK_VALUE = "Risk value"
                EDIT = "Edit"

    class DocumentsTab:
        ATTACH_DOCUMENT_BUTTON = "Attach document"
        GENERATE_DOCUMENT_BUTTON = "Generate document"
        NO_CONTENT_NOTICE = "No documents have been uploaded to this case"

    class AdditionalContactsTab:
        ADD_A_CONTACT_BUTTON = "Add a contact"
        NO_CONTENT_NOTICE = "There aren't any additional contacts on this case"
        SUCCESS_MESSAGE = "Contact added successfully"

        class Table:
            NAME = "Name"
            ADDRESS = "Address"
            EMAIL = "Email"
            PHONE_NUMBER = "Phone number"
            DETAILS = "Details"

    class CaseNotesAndTimeline:
        ADD_CASE_NOTE_LABEL = "Add case note"
        ADD_CASE_NOTE_DESCRIPTION = "You can enter up to 2200 characters"
        MAKE_VISIBLE_TO_EXPORTER = "Make visible to exporter"
        WARNING = "This note will be visible to the exporter, are you sure you wish to continue?"
        CANCEL = "Cancel"
        POST_NOTE = "Post note"

    class ComplianceLicencesTab:
        LICENCE_NUMBER = "Licence number"
        LICENCE_STATUS = "Licence status"
        LICENCE_FLAGS = "Flags"
        NO_LICENCES_NOTICE = "No Licences found"
        RETURN_COMPLETED = "Return completed"
        OLR_NOT_APPLICABLE = "N/A"

    class LicenceFilters:
        REFERENCE = "reference"


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
        USER_WORK_QUEUE = "Assign user"
        REISSUE_OGL = "Reissue OGL"
        RERUN_ROUTING_RULES = "Rerun routing rules"
        ADDITIONAL_CONTACTS = "Additional contacts"

    class Goods:
        MISSING_DOCUMENT_REASON_PREFIX = "No document given: "
        TITLE = "Products"
        CASE_GOODS_LOCATION = "Products location"
        OPEN_CASE_GOODS_LOCATION = "Destinations"
        CASE_GOODS_LOCATION_NAME = "Name"
        CASE_GOODS_LOCATION_ADDRESS = "Address"

        class Table:
            CLC = "CLC"
            DESCRIPTION = "Description"
            VALUE = "Quantity & value"
            DOCUMENTS = "Documents"
            FLAGS = "Flags"
            ADVICE = "Advice"
            PRODUCT_TYPE = "Product type"

    class Destinations:
        COUNTRY_NAME = "Country"
        PRODUCTS_CONTROL_CODES = "Goods"
        FLAGS_TABLE_HEADER = "Flags"

    class Parties:
        TITLE = "Entity"
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
        BUSINESS = "Business"
        FLAGS = "Flags"

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

    EDIT_DESTINATION_FLAGS = "Edit destination flags"
    ADVICE = "Give or change advice"
    RESPOND_BUTTON = "Respond to query"
    CLOSED = "This case is closed"
    CASE_OFFICER = "Case officer: "
    NO_CASE_OFFICER = "No case officer set"
    NO_USERS_ASSIGNED = "No users assigned"
    NO_QUEUES_ASSIGNED = "No queues assigned"
    COPY_OF_LABEL = "Copied from:"
    DONE_WITH_CASE = "I'm done"

    class EndUseDetails:
        TITLE = "End use details"
        NUMBER_COLUMN = "#"
        DESCRIPTION_COLUMN = "Description"
        ANSWER_COLUMN = "Answer"
        INTENDED_END_USE_TITLE = "Intended end use of the products"
        INFORMED_TO_APPLY_TITLE = "Informed by ECJU to apply for a licence"
        INFORMED_WMD_TITLE = "Informed by ECJU that products may be used in WMD"
        SUSPECTED_WMD_TITLE = "Exporter suspects products may be used in WMD"
        EU_MILITARY_TITLE = "European military products received under a transfer licence"
        COMPLIANT_LIMITATIONS_EU_TITLE = "Exporter compliant with terms of export limitations or obtained consent"

    class TemporaryExportDetails:
        TITLE = "Temporary export details"
        NUMBER_COLUMN = "#"
        DESCRIPTION_COLUMN = "Description"
        ANSWER_COLUMN = "Answer"
        TEMPORARY_EXPORT_DETAILS_TITLE = "Explain why the products are being exported temporarily"
        PRODUCTS_UNDER_DIRECT_CONTROL_TITLE = "Will the products remain under your direct control while overseas?"
        PROPOSED_RETURN_DATE_TITLE = "Proposed date the products will return to the UK"

    class AdditionalInformation:
        TITLE = "Additional Information"
        NUMBER_COLUMN = "#"
        DESCRIPTION_COLUMN = "Description"
        ANSWER_COLUMN = "Answer"
        ELECTRONIC_WARFARE_REQUIREMENT = "Electronic warfare requirement"
        EXPEDITED = "Expedited"
        FOREIGN_TECHNOLOGY = "Foreign Technology"
        LOCALLY_MANUFACTURED = "Locally manufactured"
        MTCR_TYPE = "MTCR type"
        VALUE = "Export Value"

    class RouteOfGoods:
        TITLE = "Route of products"
        DESCRIPTION_COLUMN = "Description"
        ANSWER_COLUMN = "Answer"
        SHIPPED_TITLE = "Shipped waybill or lading"

    class FreedomOfInformation:
        DESCRIPTION_COLUMN = "Description"
        ANSWER_COLUMN = "Answer"

    class Details:
        DETAILS = "Exhibition details"

        class Table:
            TITLE = "Title"
            REQUIRED_BY_DATE = "Required by date"
            FIRST_EXHIBITION_DATE = "First exhibition date"
            REASON_FOR_CLEARANCE = "Reason for clearance"

    class ActivityFilters:
        USER = "user"
        TEAM = "team"
        USER_TYPE = "user type"
        ACTIVITY_TYPE = "activity type"
        DATE_FROM = "date from"
        DATE_TO = "date to"
        NO_ACTIVITIES = "No activities match your filters"


class QueryPage:
    CREATED_AT_SUMMARY = "Created at"
    UPDATED_AT_SUMMARY = "Updated at"
    STATUS_SUMMARY = "Status"


class GenerateDocumentsPage:
    TITLE = "Generate document"
    ERROR = "Document generation is not available at this time"

    class SelectTemplateForm:
        BACK_LINK = "Back to case documents"

    class AddresseeForm:
        TITLE = "Select Addressee"
        DESCRIPTION = ""

        class Table:
            NAME_COLUMN = "Name"
            ADDRESS_COLUMN = "Address"
            EMAIL_COLUMN = "Email"
            PHONE_COLUMN = "Phone number"

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
        VISIBLE_TO_EXPORTER_COLUMN = "Visible to exporter"

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
    LICENSEE = "Applicant"
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


class ChangeStatusPage:
    TITLE = "Change case status"
    DESCRIPTION = ""
    SUCCESS_MESSAGE = "Case status successfully changed"
    NOTE = "Explain why you're making this decision (optional)"


class CLCReviewGoods:
    TITLE = "Respond to query"
    DESCRIPTION = "You won't be able to change this once you've submitted."
    SUCCESS_MESSAGE = "Reviewed successfully"
    HEADING = "Query"
    YOUR_RESPONSE = "Your response"
    CONTROL_LIST_ENTRY = "What are the correct control list entries for this good?"
    COMMENT = "Explain why you're making this decision (optional)"
    SUBMIT_BUTTON = "Submit"

    class Summary:
        DESCRIPTION = "Description of goods"
        PART_NUMBER = "Part number"
        IS_THIS_GOOD_CONTROLLED = "Is this good controlled?"
        CONTROL_LIST_ENTRIES = "What do you think the control list entry is?"
        EXPLANATION = "Why do you think this?"

    class Controlled:
        TITLE = "Is this good controlled?"
        YES = "Yes"
        NO = "No"

    class ReportSummary:
        TITLE = "Which report summary is applicable to this good?"
        DESCRIPTION = ""


class PVGradingForm:
    TITLE = "Respond to PV grading request"
    DESCRIPTION = "You won't be able to change this once you've submitted."
    SUBMIT_BUTTON = "Submit"
    SUCCESS_MESSAGE = "Reviewed successfully"
    BACK = "Back to case"
    HEADING = "Query"
    YOUR_RESPONSE = "Your response"
    COMMENT = "Explain why you're making this decision (optional)"

    class Summary:
        DESCRIPTION = "Description of goods"
        PART_NUMBER = "Part number"
        IS_THIS_GOOD_CONTROLLED = "Is this good controlled?"
        CONTROL_LIST_ENTRIES = "What do you think the control list entry is?"
        EXPLANATION = "Why do you think this?"

    class Grading:
        PREFIX = "Prefix"
        GRADING = "Grading"
        SUFFIX = "Suffix"


class EcjuQueries:
    CASE_HAS_NO_QUERIES = "This case has no ECJU queries"
    CLOSED = "Closed queries"
    CLOSED_DESCRIPTION = "Queries are automatically closed when the exporter responds to them."
    OPEN = "Open queries"
    CREATED_AT = "Created at"

    class Queries:
        ECJU_QUERY = "Standard query"
        PRE_VISIT_QUESTIONNAIRE = "Pre-visit questionnaire query"
        COMPLIANCE_ACTION = "Compliance query"

    class AddQuery:
        ADD_BUTTON_LABEL = "Add an ECJU query"
        ADD_PRE_VISIT_QUESTIONNAIRE = "Add pre visit questionnaire"
        COMPLIANCE_ACTIONS = "Add compliance actions"

        TITLE_PREFIX = "New "
        DESCRIPTION = (
            "Enter a full description. If your question is related to goods, then include technical"
            " details if appropriate."
        )
        SELECT_A_TYPE = "Select a type of query"
        SUBMIT = "Send"


class Advice:
    ERROR = "There is a problem"
    IMPORT_ADVICE = "Import advice from picklists"
    IMPORT_PROVISO = "Import proviso from picklists"
    OTHER = "Is there anything else you want to say to the applicant? (optional)"
    REASON = "What are your reasons for this decision?"
    TEXT_ON_LICENCE = "This will appear on the generated documentation"
    SELECT_GRADING = "Select a grading"


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
            DESCRIPTION = "Files must be smaller than 50MB"
            DESCRIPTION_FIELD_DETAILS = "optional"
            DESCRIPTION_FIELD_TITLE = "Document description"
            FILE_TOO_LARGE = "The selected file must be smaller than 50MB"
            TITLE = "Attach a document to this case"

    class MoveCase:
        TITLE = "Where do you want to move this case?"
        DESCRIPTION = ""
        SUCCESS_MESSAGE = "Case moved successfully"
        NOTE = "Explain why you're making this decision (optional)"

    class AssignUsers:
        DESCRIPTION = ""
        MULTIPLE_TITLE = "Which users do you want to assign to these cases?"
        MULTIPLE_WARNING = "Users already assigned to these cases will be overwritten."
        TITLE = "Which users do you want to assign to this case?"
        NOTE = "Explain why you're making this decision (optional)"
        BUTTON = "Save and return"
        SUCCESS_MESSAGE = "Case assigned successfully"
        SUCCESS_MULTI_MESSAGE = "Cases assigned successfully"

    class AssignUserAndQueue:
        USER_TITLE = "Select the user you want to assign the case to"
        USER_DESCRIPTION = ""
        QUEUE_TITLE = "Select a team queue to add the case to"
        QUEUE_DESCRIPTION = ""
        NOTE = "Explain why you're making this decision (optional)"
        SUBMIT_BUTTON = "Submit"

    class AssignCaseOfficer:
        TITLE = "Assign case officer"
        DESCRIPTION = ""
        DELETE_BUTTON = "Unassign existing case officer"
        SUBMIT_BUTTON = "Assign"
        INSPECTOR_TITLE = "Assign inspector"
        DELETE_INSPECTOR_BUTTON = "Unassign existing inspector"

    class RerunRoutingRules:
        TITLE = "Do you want to rerun routing rules?"
        BACKLINK = "Back to case"
        YES = "Yes"
        NO = "Cancel"
        SUBMIT_BUTTON = "Continue"

    class ReissueOGL:
        TITLE = "Are you sure you want to reissue this open general licence?"
        DESCRIPTION = "Doing so will allow the exporter to resume using this open general licence"
        YES = "Yes"
        NO = "No"
        SUBMIT = "Submit"
        ERROR = "Select an option"
        NOTE = "Explain why you're making this decision (optional)"

    class SetNextReviewDate:
        TITLE = "Set next review date"
        DESCRIPTION = "For example, 12 11 2020"


class ReviewGoodsForm:
    CONFIRM_BUTTON = "Confirm"
    HEADING = "Review goods"


class AddAdditionalContact:
    BACK_LINK = "Back to " + CasePage.Tabs.ADDITIONAL_CONTACTS.lower()
    TITLE = "Add a contact to this case"
    DESCRIPTION = ""
    SUBMIT_BUTTON = "Save and continue"

    class Name:
        TITLE = "Full name"
        DESCRIPTION = ""

    class Email:
        TITLE = "Email address"
        DESCRIPTION = ""

    class PhoneNumber:
        TITLE = "Phone number"
        DESCRIPTION = "For international numbers include the country code"

    class Details:
        TITLE = "Information about the contact"
        DESCRIPTION = ""

    class Address:
        TITLE = "Address"
        DESCRIPTION = ""


class GenerateFinalDecisionDocumentsPage:
    TITLE = "Generate Decision Documents"
    ERRORS_TITLE = "Errors"
    DONE_STATUS = "Done"
    NOT_STARTED_STATUS = "Not started"
    ADD_DOCUMENT = "Generate"
    RE_CREATE_DOCUMENT = "Regenerate"
    VIEW_DOCUMENT = "View"
    SUBMIT = "Confirm Documents"

    class Table:
        NAME_COLUMN = "Name"
        STATUS_COLUMN = "Status"
        USER_COLUMN = "Added by"
        DATE_COLUMN = "Date"
        ACTIONS_COLUMN = "Actions"


class DoneWithCaseOnQueueForm:
    TITLE = "Unassign queues"
    TITLE_SINGULAR = "Unassign {}"
    CHECKBOX_TITLE = ""
    CHECKBOX_DESCRIPTION = "Select which queues you are done with this case on"
    NOTE = "Explain why you're making this decision (optional)"
    SUBMIT = "Submit"
    SUCCESS_MESSAGE = "Done with case {}"


class UploadEnforcementXML:
    TITLE = "Upload the enforcement XML"
    DESCRIPTION = ""
    BACK_LINK = "Back to queue"
    SUCCESS_BANNER = "Enforcement XML successfully uploaded and processed"

    class Errors:
        NO_FILE = "You must attach an XML file"
        MULTIPLE_FILES = "You cannot upload multiple files"
        FILE_TOO_LARGE = "You cannot upload an XML larger than 1MB"
        FILE_READ = "Could not read the file. Please ensure the file you attach is an XML"


class OpenLicenceReturns:
    NO_CONTENT_NOTICE = "There are no open licence returns."
    TITLE = "Open licence returns"
    FILE_NAME = "File name"
    YEAR_COMPLETED = "Year completed"
    ADDED = "Added"


class ComplianceForms:
    class VisitReport:
        TITLE = "Visit report details"
        VISIT_TYPE = "Visit type"
        VISIT_DATE = "Visit date"
        VISIT_DATE_DESCRIPTION = "For example, 12 3 2020"
        OVERALL_RISK_VALUE = "Overall risk value"
        LICENCE_RISK_VALUE = "Licence risk value"

    class PeoplePresent:
        TITLE = "People present"
        NAME = "Name"
        JOB_TITLE = "Job title"
        DESCRIPTION = "Describes who the Compliance Inspector conducted the visit with from the exporting"
        " organisation - it may be referenced in a document."
        SUCCESS = "People present updated successfully"

    class Overview:
        TITLE = "Overview"

    class Inspection:
        TITLE = "Inspection"

    class ComplianceWithLicence:
        TITLE = "Compliance with licence"
        DESCRIPTION = (
            "If you have actions and recommendations for the organisation, you need to add them to the query section."
        )
        OVERVIEW = "Overview"
        RISK_VALUE = "Risk value"

    class KnowledgeOfPeople:
        TITLE = "Knowledge and Understanding demonstrated by key export individuals at meeting"
        OVERVIEW = "Overview"
        RISK_VALUE = "Risk value"

    class KnowledgeOfProducts:
        TITLE = "Knowledge of controlled items in their business' products"
        OVERVIEW = "Overview"
        RISK_VALUE = "Risk value"
