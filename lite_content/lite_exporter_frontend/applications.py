class PartyForm:
    class Options:
        GOVERNMENT = "Government organisation"
        COMMERCIAL = "Commercial organisation"
        INDIVIDUAL = "An individual"
        OTHER = "Other"

    class CopyExistingForm:
        TITLE = "Do you want to reuse an existing party?"
        YES = "Yes"
        NO = "No"
        BACK_LINK = "Back to application overview"
        BUTTON = "Continue"


class PartyTypeForm:
    BACK_LINK = "Back"


class AddPartyForm:
    ERROR = "Select yes if you want to reuse an existing party"


class CopyExistingPartyPage:
    TITLE = "Select a party"
    BACK_LINK = "Back"
    HEADING = "Select a party"
    ADD_BUTTON = "Edit and add to application"
    NONE_FOUND = "No parties found"
    RESULTS = " parties found"

    class Table:
        NAME_COLUMN = "Name"
        TYPE_COLUMN = "Type"
        ADDRESS_COLUMN = "Address"
        COUNTRY_COLUMN = "Country"
        WEBSITE_COLUMN = "Website"


class EndUserForm:
    TITLE = "Select the type of end user"
    BUTTON = "Continue"
    NAME_FORM_TITLE = "End user name"
    WEBSITE_FORM_TITLE = "End user website address (optional)"
    ADDRESS_FORM_TITLE = "End user address"
    SUBMIT_BUTTON = "Save and continue"


class EndUserPage:
    TITLE = "End user"
    DELETE_ERROR = "Unexpected error removing end user"


class UltimateEndUserForm:
    TITLE = "Select the type of ultimate recipient"
    BUTTON = "Continue"
    NAME_FORM_TITLE = "Ultimate recipient name"
    WEBSITE_FORM_TITLE = "Ultimate recipient website address (optional)"
    ADDRESS_FORM_TITLE = "Ultimate recipient address"
    SUBMIT_BUTTON = "Save and continue"


class UltimateEndUserPage:
    DELETE_ERROR = "Unexpected error removing ultimate recipient"


class ConsigneeForm:
    TITLE = "Select the type of consignee"
    BUTTON = "Continue"
    NAME_FORM_TITLE = "Consignee name"
    WEBSITE_FORM_TITLE = "Consignee website address (optional)"
    ADDRESS_FORM_TITLE = "Consignee address"
    SUBMIT_BUTTON = "Save and continue"


class ConsigneePage:
    TITLE = "Consignee"
    DELETE_ERROR = "Unexpected error removing consignee"


class ThirdPartyForm:
    class Options:
        AGENT = "Agent or broker"
        ADDITIONAL_END_USER = "End user"
        INTERMEDIATE_CONSIGNEE = "Intermediate consignee"
        SUBMITTER = "Authorised submitter"
        CONSULTANT = "Consultant"
        CONTACT = "Contact"
        EXPORTER = "Exporter"

    ROLE_TITLE = "Select the role of the third party in your application"
    TYPE_TITLE = "Select the type of third party"
    BUTTON = "Continue"
    NAME_FORM_TITLE = "Third party name"
    WEBSITE_FORM_TITLE = "Third party website address (optional)"
    ADDRESS_FORM_TITLE = "Third party address"
    SUBMIT_BUTTON = "Save and continue"


class ThirdPartyPage:
    DELETE_ERROR = "Unexpected error removing third party"


class DeletePartyDocumentForm:
    TITLE = "Confirm you want to delete the document"


class GeneratedDocuments:
    NO_DOCUMENTS = "There are no documents from ECJU."

    class Table:
        NAME_COLUMN = "Name"
        DATE_COLUMN = "Date"
        DOWNLOAD_LINK = "Download"


class ApplicationSummaryPage:
    REFERENCE_CODE = "ECJU reference"
    REFERENCE_NAME = "Reference"
    TYPE = "Licence type"
    CASE_OFFICER = "Case officer"
    NO_ASSIGNED_CASE_OFFICER = "Not assigned"
    EXPORT_TYPE = "Export type"
    STATUS = "Status"
    LAST_UPDATED_AT = "Last updated"
    CREATED_AT = "Created"
    SUBMITTED_AT = "Submitted"
    END_USER = "End user"
    ULTIMATE_END_USERS = "Ultimate recipient"
    CONSIGNEE = "Consignee"
    THIRD_PARTIES = "Third parties"
    GOODS_LOCATIONS = "Locations"
    GOODS_DEPARTED = "Have the goods already left the UK?"
    SUPPORTING_DOCUMENTATION = "Supporting documents"
    GOODS = "Products"
    COUNTRIES = "Countries"
    ON_BEHALF_OF = "On behalf of"
    OPTIONAL_NOTE = "Optional note"
    COPY_REFERENCE_CODE = "Copy ECJU reference"
    COPIED = "Copied"

    class Sections:
        COMPLETED_TAG = "Saved"
        IN_PROGRESS_TAG = "In progress"
        NOT_STARTED_TAG = "Not started"

    class PartiesPreviewList:
        NAME = "Name"
        TYPE = "Type"
        ROLE = "Role"
        WEBSITE = "Website"
        ADDRESS = "Address"
        COUNTRY = "Country"
        ATTACH = "Attach"
        DOCUMENT = "Document"

    class Buttons:
        EDIT_APPLICATION_BUTTON = "Edit"
        WITHDRAW_ACCESS_BUTTON = "Withdraw"
        SURRENDER_APPLICATION_BUTTON = "Surrender licence"

    class Withdraw:
        TITLE = "Confirm you want to withdraw this application"
        BACK_TEXT = "Back to application"
        YES_LABEL = "Confirm and withdraw the application"
        NO_LABEL = "Cancel"
        SUBMIT_BUTTON = "Submit"
        WITHDRAW_ERROR = "Select confirm if you want to withdraw the application"

    class Surrender:
        TITLE = "Confirm you want to surrender this application"
        BACK_TEXT = "Back to application"
        YES_LABEL = "Confirm and surrender the application"
        NO_LABEL = "Cancel"
        SUBMIT_BUTTON = "Submit"
        WITHDRAW_ERROR = "Select confirm if you want to surrender the application"

    class Tabs:
        DETAILS = "Details"
        NOTES = "Notes"
        ECJU_QUERIES = "ECJU queries"
        GENERATED_DOCUMENTS = "ECJU documents"
        ACTIVITY = "Activity"


class ApplicationsSummaryPage:
    NAME = "Name"
    REFERENCE_CODE = "ECJU reference"
    TYPE = "Licence type"
    EXPORT_TYPE = "Export type"
    STATUS = "Status"
    LAST_UPDATED_AT = "Last updated"
    CREATED_AT = "Created"
    SUBMITTED_AT = "Submitted"


class InitialApplicationQuestionsForms:
    class OpeningQuestion:
        TITLE = "Select what you need"
        LABEL = ""
        DESCRIPTION = ""
        BREADCRUMB = "Apply for a licence"
        HELP_WITH_CHOOSING_A_LICENCE = ""
        HELP_WITH_CHOOSING_A_LICENCE_CONTENT = (
            "Read about the [different types of export control licences]"
            "(https://www.gov.uk/guidance/beginners-guide-to-export-controls#what-licence-do-i-need)."
        )

        class LicenceTypes:
            EXPORT_LICENCE_TITLE = "Export licence"
            EXPORT_LICENCE_DESCRIPTION = "Select if you’re sending products from the UK to another country"

            TRANSHIPMENT_LICENCE_TITLE = "Transhipment licence"
            TRANSHIPMENT_LICENCE_DESCRIPTION = (
                "Select if you're shipping something from overseas through the UK on to another country."
                " If the products will be in the UK for 30 days or more, apply for an export licence"
            )
            TRADE_CONTROL_LICENCE_TITLE = "Trade control licence"
            TRADE_CONTROL_LICENCE_DESCRIPTION = (
                "Select if you’re arranging or brokering the sale or movement of controlled military products "
                "located overseas"
            )

            MOD_CLEARANCE_TITLE = "MOD clearance"
            MOD_CLEARANCE_DESCRIPTION = "Select if you need an F680 to share information, go to an exhibition or you're gifting surplus products"

    class ReferenceNameQuestion:
        TITLE = "Name the application"
        ENTER_A_REFERENCE_NAME_SHORT_TITLE = "Reference name"
        DESCRIPTION = "Give the application a reference name so you can refer back to it when needed."
        LABEL = ""
        BACK_TO_LICENCE_TYPE = "Back to export licence type"
        BACK_TO_MOD_CLEARANCE_TYPE = "Back to MOD clearance type"


class ExportLicenceQuestions:
    class ExportLicenceQuestion:
        TITLE = "Select the type of export licence you need"
        BACK = "Back to application type"
        DESCRIPTION = ""
        STANDARD_LICENCE = "Standard licence"
        STANDARD_LICENCE_DESCRIPTION = (
            "Select a standard licence for a set quantity and set value of products. "
            "You must attach a completed "
            "[end user undertaking form](https://www.gov.uk/government/publications/end-user-undertaking-euu-form)"
            " to the application."
        )
        OPEN_LICENCE = "Open licence"
        OPEN_LICENCE_DESCRIPTION = (
            "Select an open licence for multiple shipments of specific products to specific countries. "
            "Open licences cover long term projects and repeat business."
        )

    class ExportType:
        TITLE = "Select an export type"
        DESCRIPTION = ""
        TEMPORARY = "Temporary"
        PERMANENT = "Permanent"

    class HaveYouBeenInformedQuestion:
        TITLE = "Have you been informed under an 'end use control' that you need to apply for a licence?"
        DESCRIPTION = "An end use control is an official letter or email from Border Force or HMRC."
        WHAT_WAS_THE_REFERENCE_CODE_TITLE = "Reference number"
        WHAT_WAS_THE_REFERENCE_CODE_DESCRIPTION = "The reference number is on the official letter or email."


class MODQuestions:
    class WhatAreYouApplyingFor:
        TITLE = "Select the type of MOD clearance you need"
        DESCRIPTION = ""
        BACK = "Back to application type"

        PERMISSION_TITLE = "MOD Form 680"
        PERMISSION_DESCRIPTION = (
            "Select an F680 approval if you need to release equipment or information with a classification of "
            "OFFICIAL-SENSITIVE or above to any foreign entity overseas or demonstrate it to them in the UK."
        )

        EXHIBITION_CLEARANCE_TITLE = "Exhibition clearance"
        EXHIBITION_CLEARANCE_DESCRIPTION = (
            "Select if you need clearance to exhibit defence related products that aren't MOD funded."
        )

        GIFTING_CLEARANCE_TITLE = "Gifting clearance"
        GIFTING_CLEARANCE_DESCRIPTION = "Select to request the gifting of surplus MOD property."


class DestinationForm:
    TITLE = "Where are the products going?"
    DESCRIPTION = ""


class StandardApplicationTaskList:
    ENTER_A_REFERENCE_NAME_SHORT_TITLE = "Reference"
    NEW_TITLE = "Standard export licence application"
    EDIT_TITLE = "Edit the application"
    END_USE_CONTROL = "End use control"
    GOODS = "Products"
    GOODS_LOCATION = "Locations"
    END_USER = "End user"
    ULTIMATE_END_USERS = "Ultimate recipients"
    CONSIGNEE = "Consignee"
    SUPPORTING_DOCUMENTS = "Supporting documents"
    THIRD_PARTIES = "Third parties"


class OpenApplicationTaskList:
    ENTER_A_REFERENCE_NAME_SHORT_TITLE = "Reference"
    NEW_TITLE = "Open export licence application"
    EDIT_TITLE = "Edit the application"
    GOODS = "Products"
    GOODS_LOCATION = "Locations"
    GOODS_DESTINATION = "Countries"
    COUNTRIES_WHERE_EACH_GOOD_IS_GOING = "Product destinations"
    SUPPORTING_DOCUMENTS = "Supporting documents"


class HMRCApplicationTaskList:
    ENTER_A_REFERENCE_NAME_SHORT_TITLE = "Reference"
    GOODS = "Products"
    GOODS_LOCATION = "Locations"
    END_USER = "End user"
    ULTIMATE_END_USERS = "Ultimate recipients"
    THIRD_PARTIES = "Third parties"
    CONSIGNEE = "Consignee"
    SUPPORTING_DOCUMENTS = "Supporting documents"
    REASON_FOR_QUERY = "Reason for query"
    CHECK_YOUR_ANSWERS = "Check your answers"


class ExhibitionClearanceTaskList:
    ENTER_A_REFERENCE_NAME_SHORT_TITLE = "Reference"
    NEW_TITLE = "Exhibition clearance application"
    EDIT_TITLE = "Edit the application"
    GOODS = "Products"
    GOODS_LOCATION = "Locations"
    END_USER = "End user"
    ULTIMATE_END_USERS = "Ultimate recipients"
    CONSIGNEE = "Consignee"
    SUPPORTING_DOCUMENTS = "Supporting documents"
    THIRD_PARTIES = "Third parties"


class GiftingClearanceTaskList:
    ENTER_A_REFERENCE_NAME_SHORT_TITLE = "Reference"
    NEW_TITLE = "Gifting clearance application"
    EDIT_TITLE = "Edit the application"
    GOODS = "Products"
    GOODS_LOCATION = "Locations"
    END_USER = "End user"
    SUPPORTING_DOCUMENTS = "Supporting documents"
    THIRD_PARTIES = "Third parties"


class F680ClearanceTaskList:
    ENTER_A_REFERENCE_NAME_SHORT_TITLE = "Reference"
    NEW_TITLE = "F680 clearance application"
    EDIT_TITLE = "Edit the application"
    GOODS = "Products"
    GOODS_LOCATION = "Locations"
    END_USER = "End user"
    SUPPORTING_DOCUMENTS = "Supporting documents"
    THIRD_PARTIES = "Third parties"


class EditApplicationPage:
    BACK = "Back to applications"
    DRAFT_DELETE_LINK = "Delete draft"
    SUBMIT = "Submit application"
    DONE = "Saved"
    ERRORS = "There is a problem"
    MINOR_EDIT = "Changes made to this application won't impact its processing time."
    MAJOR_EDIT = "This application won't be processed until it's submitted."

    class InitialTaskSection:
        TITLE = "Prepare application"
        EDITING = "Basic details"

    class MainTaskSection:
        TITLE = "Complete application"
        EDITING = "More information"


class EditOpenApplicationPage:
    BACK_TO_APPLICATIONS = "Back to applications"
    DRAFT_DELETE_LINK = "Delete draft"
    SUBMIT = "Submit application"


class DeleteApplicationPage:
    BUTTON = "Delete draft"
    TITLE = "Confirm you want to delete this draft"
    BACK_TEXT = "Back"
    YES_LABEL = "Confirm and delete the draft"
    NO_LABEL = "Cancel"
    SUBMIT_BUTTON = "Submit"
    DELETE_ERROR = "Select confirm if you want to delete the draft"


class AttachDocumentPage:
    UPLOAD_FAILURE_ERROR = "We had an issue uploading your files. Try again later."
    UPLOAD_GENERIC_ERROR = "We had an issue creating your response. Try again later."
    DOWNLOAD_GENERIC_ERROR = "We had an issue downloading your file. Try again later."


class DeleteDocument:
    DOCUMENT_DELETE_GENERIC_ERROR = "We had an issue deleting your file. Try again later."


class ApplicationSuccessPage:
    TITLE = "Application submitted"
    SECONDARY_TITLE = "ECJU reference: "
    DESCRIPTION = ""
    WHAT_HAPPENS_NEXT = ["You'll receive an email from ECJU when the check is finished."]
    VIEW_APPLICATIONS = "View your list of applications"
    APPLY_AGAIN = "Apply for another licence or clearance"
    RETURN_TO_DASHBOARD = "Return to your export control account dashboard"


class ApplicationsList:
    TITLE = "Applications"
    RAISE_A_QUERY_BUTTON = "Raise a query"
    APPLY_FOR_A_LICENCE_BUTTON = "Apply for a licence"
    REFRESH_BUTTON = "Refresh"
    IN_PROGRESS_TAB = "In progress"
    DRAFTS_TAB = "Drafts"
    NOTIFICATIONS_SUFFIX = "notifications"
    NO_CONTENT_NOTICE = "There are no applications in progress."
    NO_DRAFTS_CONTENT_NOTICE = "There are no draft applications."


class ApplicationPage:
    BACK = "Back to applications"
    NO_INFORMATION_PROVIDED = "No information added to this section."


class ThirdPartiesPage:
    TITLE = "Third parties"
    ADD = "Add a third party"
    NO_RESULTS = "There are no third parties on this application"

    class Variables:
        NAME = "Name"
        TYPE = "Type"
        ROLE = "Role"
        WEBSITE = "Website"
        ADDRESS = "Address"
        COUNTRY = "Country"
        DOCUMENT = "Document"


class UltimateEndUsersPage:
    TITLE = "Ultimate recipients"
    ADD = "Add a third party"
    NO_RESULTS = "There are no third parties on this application"
    BACK = "Back to application overview"
    HELP = "What is an ultimate recipient?"
    DESCRIPTION = (
        "An ultimate recipient is an entity that uses the product or the higher level system into which the product is"
        " installed or incorporated. The end user and ultimate recipient may be different parties."
    )
    NOTICE = "There are no ultimate recipients on this application"
    MISSING_DOCS_NOTICE = "You need to attach a document to some ultimate recipients"
    ADD_BUTTON = "Add an ultimate recipient"

    class Document:
        DOWNLOAD = "Download"
        DELETE = "Delete"
        PROCESSING = "Processing"
        ATTACH = "Attach"
        REMOVE = "Remove"

    class Variables:
        NAME = "Name"
        TYPE = "Type"
        ROLE = "Role"
        WEBSITE = "Website"
        ADDRESS = "Address"
        COUNTRY = "Country"
        DOCUMENT = "Document"


class Activity:
    NO_ACTIVITY = "There hasn't been any activity on this application"


class CaseNotes:
    TITLE = "Add a note"
    NOTICE = "You can enter up to 2200 characters."
    POST_NOTE = "Post note"
    CANCEL = "Cancel"
    ADDED_A_NOTE_SUFFIX = "added a note:"
    NO_NOTES = "There aren't any notes on this application"
