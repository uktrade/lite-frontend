from lite_content.lite_internal_frontend import (  # noqa
    cases,  # noqa
    letter_templates,  # noqa
    roles,  # noqa
    organisations,  # noqa
    generic,  # noqa
    users,  # noqa
    teams,  # noqa
)  # noqa

# Buttons
CONTINUE = "Continue"
SAVE = "Save"
NOT_APPLICABLE = "N/A"

QUEUE_ALL_CASES = "All cases"

CASE_CHANGES = "See what has changed"

USERS_LIST_PAGE_EDIT = "Edit"

USER_PROFILE_PAGE_EDIT = "Edit"
USER_DEACTIVATE = "Deactivate"
USER_REACTIVATE = "Reactivate"

# Generate Document
CHOOSE_TEMPLATE_TITLE = "Select a template"
CHOOSE_TEMPLATE_BUTTON = CONTINUE
PREVIEW_DOCUMENT_TITLE = "Preview"
PREVIEW_DOCUMENT_BUTTON = SAVE

# Organisation
ORGANISATION_CREATION_SUCCESS = "The organisation was created successfully"
ORGANISATION_SET_FLAGS = "Set flags on this organisation"
ORGANISATION_EDIT_FLAGS = "Edit organisation flags"

# HMRC Organisation
HMRC_ORGANISATION_CREATION_SUCCESS = "The HMRC organisation was created successfully"

# Flags
SET_CASE_FLAGS = "Set case flags"
EDIT_CASE_FLAGS = "Edit case flags"

# Case
CASE_GOODS = "Goods"
CASE_ENTITIES_NONE = "No inactive case entities"
CASE_ENTITIES_ACTIVITY = "Activity"
CASE_PARTIES_LICENSEE = "Licensee"

CASE_INFO_TYPE = "Type"
CASE_INFO_ORGANISATION = "Organisation"
CASE_INFO_STATUS = "Status"
CASE_INFO_ACTIVITY = "Activity"
CASE_INFO_SUBMITTED_AT = "Submitted at"
CASE_INFO_REFERENCE_NUMBER = "Reference number"
CASE_INFO_EXPORT_TYPE = "Export type"
CASE_INFO_USAGE = "Usage"
CASE_INFO_LAST_UPDATED = "Last updated"

CASE_COUNTRIES = "Countries"
CASE_COUNTRIES_GREEN_LIST = "Green list"
CASE_DESTINATIONS_HEADER = "Destinations"

CASE_ACTIVITY_HEADING = "Activity"

# Good
GOOD_DESCRIPTION = "Description"
GOOD_CONTROL_LIST_ENTRY = "Control list classification"
GOOD_INCORPORATED = "Incorporated"
GOOD_CONTROLLED = "Controlled"
GOOD_FLAGS = "Flags"

STANDARD_CASE_TOTAL_VALUE = "Total value:"

# Supporting documentation
SUPPORTING_DOCUMENTATION_TITLE = "Supporting documents"
SUPPORTING_DOCUMENTATION_NAME = "Name"
SUPPORTING_DOCUMENTATION_DESCRIPTION = "Description"
SUPPORTING_DOCUMENTATION_DOCUMENT = "Document"
SUPPORTING_DOCUMENTATION_NO_DOCUMENTATION = "No supporting documents"

INACTIVE_ENTITIES = "No supporting documents"

COMBINE_USER_ADVICE = "Combine all user advice"
GIVE_OR_CHANGE_ADVICE = "Give or change advice"
CLEAR_ADVICE = "Clear advice"

DOCUMENT_TEMPLATES_TITLE = "Document templates"

REGISTER_BUSINESS_FIRST_AND_LAST_NAME = "First and last name"

USER_ADD_TITLE = "Add user"
USER_EMAIL_QUESTION = "Email address"
USER_TEAM_QUESTION = "Team"
USER_ROLE_QUESTION = "Role"
USER_ADD_FORM_BACK_TO_USERS = "Back to users"
USER_EDIT_TITLE = "Edit user"
USER_EDIT_FORM_BACK_TO_USER = "Back to user"
USER_EDIT_FORM_SAVE = "Save"


class Common:
    SERVICE_NAME = "LITE Internal"


class RegisterBusiness:
    COMMERCIAL_OR_PRIVATE_INDIVIDUAL = "Commercial or private individual?"
    CREATE_ADMIN = "Create an admin for this organisation"
    CREATE_DEFAULT_SITE = "Create a default site for this exporter"
    CRN = "Company registration number (CRN)"
    CRN_DESCRIPTION = "8 numbers, or 2 letters followed by 6 numbers."
    DEFAULT_USER = "This will be the default user for this organisation."
    EMAIL = "Email"
    EORI_NUMBER = "European Union registration and identification number (EORI)"
    FIRST_NAME = "First name"
    GO_HOME = "Go home"
    GO_TO_COMPANIES = "Go to organisation list"
    LAST_NAME = "Last name"
    NAME = "Name of organisation"
    NAME_OF_SITE = "Name of site"
    REGISTER_COMMERCIAL_TITLE = "Register an organisation"
    REGISTER_INDIVIDUAL_TITLE = "Register a private individual"
    EDIT_COMMERCIAL_TITLE = "Edit an organisation"
    EDIT_INDIVIDUAL_TITLE = "Edit a private individual"
    REGISTRATION_COMPLETE = "Registration complete"
    SUCCESSFULLY_REGISTERED = " Successfully registered"
    WHERE_IS_THE_EXPORTER_BASED = "Where is the exporter based?"

    class UkVatNumber:
        DESCRIPTION = "9 digits long, with the first 2 letters indicating the country code of the registered business."
        TITLE = "UK VAT number"

    class SicNumber:
        DESCRIPTION = "Classifies industries by a 4 digit code."
        TITLE = "SIC number"


class Authentication:
    class UserDoesNotExist:
        DESCRIPTION = "You are not registered to use this system"
        TITLE = "User not found"


class Users:
    DESCRIPTION = "Team level users can manage and view team user accounts."
    INVITE = "Invite a new user"


class UpdateUser:
    class Status:
        DEACTIVATE_WARNING = "This user will no longer be able to sign in or perform tasks"
        REACTIVATE_WARNING = "This user will be able to sign in to and perform tasks"


class Activity:
    ADDED_AN_ECJU_QUERY = " added an ECJU query:"
    ADDED_A_CASE_NOTE = " added a case note:"


class Queues:
    class QueueList:
        COLUMN_HEADING_ACTIONS = "Actions"
        COLUMN_HEADING_NAME = "Queue name"
        COLUMN_HEADING_TEAM = "Team name"
        PAGE_HEADING = "My work queues"

    class QueueAdd:
        TITLE = "Add queue"
        DESCRIPTION = ""
        BACK = "Back to queue"

        class Name:
            TITLE = "Name"
            DESCRIPTION = ""

    class QueueEdit:
        TITLE = "Edit queue"
        DESCRIPTION = ""
        BACK = "Back to queue"

        class Name:
            TITLE = "Name"
            DESCRIPTION = ""


class Flags:
    CREATE = "Create a flag"
    DESCRIPTION = "Flags are a simple way to tag cases, organisations, destinations and goods."
    TITLE = "Flags"

    class UpdateFlag:
        class Status:
            DEACTIVATE_HEADING = "Are you sure you want to deactivate this flag?"
            DEACTIVATE_WARNING = "This flag will no longer be able to be used unless it's reactivated"
            REACTIVATE_HEADING = "Are you sure you want to reactivate this flag?"
            REACTIVATE_WARNING = "This flag will be able to be used unless it's deactivated again"


class Picklist:
    TITLE = "Picklists"

    class Edit:
        class Status:
            DEACTIVATE_HEADING = "Are you sure you want to deactivate this picklist item?"
            DEACTIVATE_WARNING = "This picklist item will no longer be able to be used unless it's reactivated"
            REACTIVATE_HEADING = "Are you sure you want to reactivate this picklist item?"
            REACTIVATE_WARNING = "This picklist item will be able to be used unless it's deactivated again"


class LetterTemplates:
    class AddParagraph:
        ADD_BUTTON = "Add items"
        HINT = "Select letter paragraphs to use in your template."
        TITLE = "Add letter paragraphs"

    class EditParagraph:
        ADD_LINK = "Add another letter paragraph"
        HINT = "Drag and drop letter paragraphs to reorder."
        REMOVE_BUTTON = "Remove letter paragraph from template"
        SAVE_BUTTON = "Save"
        TITLE = "Edit letter paragraphs"

    class OrderParagraph:
        ADD_PARAGRAPH = "Add a new paragraph"
        JS_HINT = "Drag and drop letter paragraphs to move them around"
        NO_JS_HINT = "Delete and add new paragraphs"
        PREVIEW_BUTTON = "Preview"
        REMOVE_BUTTON = "Remove letter paragraph from template"
        TITLE = "Choose the letter paragraphs you want to use in your letter"

    class Preview:
        SAVE_BUTTON = "Save"
        TITLE = "Preview"

    class LetterTemplates:
        CREATE_BUTTON = "Create a template"
        ERROR_BANNER = "An error occurred whilst processing your template"
        LAYOUT_COLUMN_TITLE = "Layout"
        NAME_COLUMN_TITLE = "Name"
        RESTRICTED_COLUMN_TITLE = "Restricted to"
        SUCCESSFULLY_CREATED_BANNER = "Your letter template was created successfully"
        TITLE = "Letter templates"
        UPDATED_COLUMN_TITLE = "Last updated"

    class LetterTemplate:
        BACK_LINK = "Back to letter templates"
        CREATED_TITLE = "Created at"
        EDIT_BUTTON = "Edit name and layout"
        EDIT_PARAGRAPH_BUTTON = "Add or edit paragraphs"
        LAST_UPDATE_TITLE = "Last updated"
        LAYOUT_TITLE = "Layout"
        RESTRICTED_TITLE = "Restricted to"
        DECISIONS_TITLE = "Decisions"

    class EditLetterTemplate:
        BUTTON_NAME = "Save"
        TITLE = "Edit %s"

        class Name:
            HINT = (
                "Call it something that:\n• is easy to find\n• explains when to use this template\n\n For example,"
                " 'Refuse a licence'"
            )
            TITLE = "Give your template a name"

        class CaseTypes:
            TITLE = "When should someone use this template?"

            class Types:
                APPLICATION = "Applications"
                GOODS_QUERY = "Goods query"
                END_USER_ADVISORY = "End user advisory queries"

        class Decisions:
            TITLE = "Decisions (optional)"
            DESCRIPTION = "Select the decisions that apply to your template"

        class Layout:
            TITLE = "Choose a layout"

    class AddLetterTemplate:
        class Name:
            BACK_LINK = "Back to letter templates"
            CONTINUE_BUTTON = "Continue"
            HINT = (
                "Call it something that:\n• is easy to find\n• explains when to use this template\n\n For example,"
                " 'Refuse a licence'"
            )
            TITLE = "Give your template a name"

        class CaseTypes:
            CONTINUE_BUTTON = "Continue"
            TITLE = "When should someone use this template?"

            class Types:
                APPLICATION = "Applications"
                GOODS_QUERY = "Goods query"
                END_USER_ADVISORY = "End user advisory queries"

        class Decisions:
            TITLE = "Decisions (optional)"

        class Layout:
            CONTINUE_BUTTON = "Continue"
            TITLE = "Choose a layout"
