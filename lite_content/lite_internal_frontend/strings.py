from lite_content.lite_internal_frontend import (  # noqa
    advice,  # noqa
    cases,  # noqa
    letter_templates,  # noqa
    open_general_licences,  # noqa
    roles,  # noqa
    flags,  # noqa
    organisations,  # noqa
    generic,  # noqa
    goods,  # noqa
    users,  # noqa
    teams,  # noqa
    queues,  # noqa
    picklists,  # noqa
    routing_rules,  # noqa
)  # noqa

# Buttons
CONTINUE = "Continue"
SAVE = "Save"
NOT_APPLICABLE = "N/A"

QUEUE_ALL_CASES = "All cases"


# Organisation
ORGANISATION_CREATION_SUCCESS = "The organisation was created successfully"
ORGANISATION_SET_FLAGS = "Set flags on this organisation"
ORGANISATION_EDIT_FLAGS = "Edit organisation flags"

# HMRC Organisation
HMRC_ORGANISATION_CREATION_SUCCESS = "The HMRC organisation was created successfully"

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

DOCUMENT_TEMPLATES_TITLE = "Document templates"


class Common:
    SERVICE_NAME = "LITE Internal"


class Authentication:
    class UserDoesNotExist:
        DESCRIPTION = "You are not registered to use this system"
        TITLE = "User not found"


class UpdateUser:
    class Status:
        DEACTIVATE_WARNING = "This user will no longer be able to sign in or perform tasks"
        REACTIVATE_WARNING = "This user will be able to sign in to and perform tasks"


class Activity:
    ADDED_AN_ECJU_QUERY = " added an ECJU query:"
    ADDED_A_CASE_NOTE = " added a case note:"


class FlaggingRules:
    CREATE = "Create new flagging rule"
    TITLE = "Flagging rules"
    DESCRIPTION = "Flagging rules apply flags to cases automatically based on conditions"

    class List:
        class Filter:
            Type = "Type"
            MY_TEAM_ONLY = "Only show my team"
            INCLUDE_DEACTIVATED = "Include deactivated"

        TEAM = "Team"
        TYPE = "Type"
        FLAG = "Flag"
        CONDITION = "Condition"
        STATUS = "Status"
        ACTIONS = "Actions"

        EDIT = "Edit"
        REACTIVATE = "Reactivate"
        DEACTIVATE = "Deactivate"

    class Create:
        BACKLINK = "Back to flagging rules"

        class Type:
            TITLE = "Select flagging rule type"
            SAVE = "Continue"

            GOOD = "Good"
            DESTINATION = "Destination"
            APPLICATION = "Application type"

        class Condition_and_flag:
            GOOD_TITLE = "Select a control list classification and flag"
            DESTINATION_TITLE = "Select a country and flag"
            APPLICATION_TITLE = "Select a application type and flag"

            GOOD = "Control list classification"
            DESTINATION = "Country"
            APPLICATION = "Application type"

            FLAG = "Flag"

            GOODS_QUESTION = "Must this rule only apply to verified goods?"
            YES_OPTION = "Yes"
            NO_OPTION = "No"

    class Status:
        DEACTIVATE_HEADING = "Are you sure you want to deactivate this flagging rule?"
        DEACTIVATE_WARNING = "This flagging rule will no longer be able to be used unless it's reactivated"
        DEACTIVATE_CONFIRM = "Deactivate this flagging rule"

        REACTIVATE_HEADING = "Are you sure you want to reactivate this flagging rule?"
        REACTIVATE_WARNING = "This flagging rule will be able to be used unless it's deactivated again"
        REACTIVATE_CONFIRM = "Reactivate this flagging rule"

        BACK = "Back to flagging rules"
        CANCEL = "Cancel"

        NO_SELECTION_ERROR = "Select to confirm or not"


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
        SAVE_BUTTON = "Done"
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
        VISIBLE_TO_EXPORTER_TITLE = "Visible to exporter"
        DIGITAL_SIGNATURE_TITLE = "Has a digital signature"

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

        class IncludeSignature:
            TITLE = "Add a digital signature to the template?"
            DESCRIPTION = ""
            YES_OPTION = "Yes"
            NO_OPTION = "No"

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

        class VisibleToExporter:
            TITLE = "Visible to exporter"
            DESCRIPTION = "Should documents created with this template be visible to exporters?"
            YES_OPTION = "Yes"
            NO_OPTION = "No"
            BUTTON = "Continue"

        class IncludeSignature:
            TITLE = "Add a digital signature to the template?"
            DESCRIPTION = ""
            YES_OPTION = "Yes"
            NO_OPTION = "No"
            BUTTON = "Continue"

        class Layout:
            CONTINUE_BUTTON = "Continue"
            TITLE = "Choose a layout"
