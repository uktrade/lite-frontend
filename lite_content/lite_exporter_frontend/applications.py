class PartyForm:
    class Options:
        GOVERNMENT = "Government organisation"
        COMMERCIAL = "Commercial organisation"
        INDIVIDUAL = "An individual"
        OTHER = "Other"


class EndUserForm:
    TITLE = "Select the type of end user"
    BUTTON = "Continue"
    NAME_FORM_TITLE = "Name of the end user"
    WEBSITE_FORM_TITLE = "Website address for the end user (optional)"
    ADDRESS_FORM_TITLE = "Address of the end user"
    SUBMIT_BUTTON = "Save and continue"


class UltimateEndUserForm:
    TITLE = "Select the type of ultimate recipient"
    BUTTON = "Continue"
    NAME_FORM_TITLE = "Name of the ultimate recipient"
    WEBSITE_FORM_TITLE = "Website address for the ultimate recipient (optional)"
    ADDRESS_FORM_TITLE = "Address of the ultimate recipient"
    SUBMIT_BUTTON = "Save and continue"


class ConsigneeForm:
    TITLE = "Select the type of consignee"
    BUTTON = "Continue"
    NAME_FORM_TITLE = "Name of consignee"
    WEBSITE_FORM_TITLE = "Website address for the consignee (optional)"
    ADDRESS_FORM_TITLE = "Address of the consignee"
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
    BUTTON = "Continue"
    NAME_FORM_TITLE = "Name of the third party"
    WEBSITE_FORM_TITLE = "Website address for the third party (optional)"
    ADDRESS_FORM_TITLE = "Address of the third party"
    SUBMIT_BUTTON = "Save and continue"


class GeneratedDocuments:
    NO_DOCUMENTS = "There are no documents from ECJU."

    class Table:
        NAME_COLUMN = "Name"
        DATE_COLUMN = "Date"
        DOWNLOAD_LINK = "Download"


class ApplicationSummaryPage:
    REFERENCE_NAME = "Reference"
    TYPE = "Licence type"
    CASE_OFFICER = "Case Officer"
    NO_CASE_OFFICER = "Not assigned"
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
    SUPPORTING_DOCUMENTATION = "Supporting documents"
    GOODS = "Products"
    COUNTRIES = "Countries"
    ON_BEHALF_OF = "On behalf of"
    OPTIONAL_NOTE = "Optional note"

    class Buttons:
        EDIT_APPLICATION_BUTTON = "Edit application"
        WITHDRAW_ACCESS_BUTTON = "Withdraw application"

    class Withdraw:
        TITLE = "Confirm you want to withdraw this application?"
        BACK_TEXT = "Back to application"
        YES_LABEL = "Confirm and withdraw the application"
        NO_LABEL = "Cancel"
        SUBMIT_BUTTON = "Submit"
        WITHDRAW_ERROR = "Select confirm if you want to withdraw the application"

    class Tabs:
        DETAILS = "Details"
        NOTES = "Notes"
        ECJU_QUERIES = "ECJU queries"
        GENERATED_DOCUMENTS = "ECJU documents"
        ACTIVITY = "Activity"


class ApplicationsSummaryPage:
    REFERENCE_NAME = "Reference"
    TYPE = "Licence type"
    EXPORT_TYPE = "Export type"
    STATUS = "Status"
    LAST_UPDATED_AT = "Last updated"
    CREATED_AT = "Created at"
    SUBMITTED_AT = "Submitted at"


class InitialApplicationQuestionsForms:
    WHICH_EXPORT_LICENCE_DO_YOU_WANT_TITLE = "Select the type of licence you need"
    WHICH_EXPORT_LICENCE_DO_YOU_WANT_DESCRIPTION = ""
    STANDARD_LICENCE = "Standard licence"
    STANDARD_LICENCE_DESCRIPTION = (
        "Select a standard licence for a set quantity and set value of products. "
        "You must attach a completed end user undertaking form to the application."
    )
    OPEN_LICENCE = "Open licence"
    OPEN_LICENCE_DESCRIPTION = (
        "Select an open licence for multiple shipments of specific products to specific countries. "
        "Open licences cover long term projects and repeat business."
    )
    HELP_WITH_CHOOSING_A_LICENCE = "What licence do I need?"
    HELP_WITH_CHOOSING_A_LICENCE_CONTENT = "Read about the different types of export control licences."
    ENTER_A_REFERENCE_NAME_TITLE = "Name the application"
    ENTER_A_REFERENCE_NAME_SHORT_TITLE = "Reference name"
    ENTER_A_REFERENCE_NAME_DESCRIPTION = (
        "Give the application a reference name so you can refer back to it when needed."
    )
    TEMPORARY_OR_PERMANENT_TITLE = "Select an export type"
    TEMPORARY_OR_PERMANENT_DESCRIPTION = ""
    TEMPORARY = "Temporary"
    PERMANENT = "Permanent"
    HAVE_YOU_BEEN_INFORMED_TITLE = (
        "Have you been informed under an 'end use control' that you need to apply for a licence?"
    )
    HAVE_YOU_BEEN_INFORMED_DESCRIPTION = (
        "An end use control is an official a letter or email from Border Force or HMRC."
    )
    WHAT_WAS_THE_REFERENCE_CODE_TITLE = "Reference number (optional)"
    WHAT_WAS_THE_REFERENCE_CODE_DESCRIPTION = "The reference number is on the official letter or email."


class DestinationForm:
    TITLE = "Where are your products going?"
    DESCRIPTION = "Select all countries that apply."


class EditStandardApplicationPage:
    DRAFT_DELETE_LINK = "Delete draft"
    SUBMIT = "Submit application"


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


class TaskListPage:
    ENTER_A_REFERENCE_NAME_SHORT_TITLE = "Reference name"
    WHERE_ARE_YOUR_GOODS_GOING_SHORT_TITLE = "Set countries"
