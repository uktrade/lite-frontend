class Picklists:
    ADD_BUTTON = "Add an item"
    ITEMS_COUNT = "item in total/items in total"
    SELECT_OPTION = "Select an option"


class PicklistItem:
    EDIT_BUTTON = "Edit item"
    DEACTIVATE_BUTTON = "Deactivate item"
    REACTIVATE_BUTTON = "Reactivate item"


class PicklistPicker:
    NO_CONTENT_NOTICE = "Templates have not been added yet"


class NewPicklistForm:
    ECJU_QUERY = "Create an ECJU query"
    PRE_VISIT_QUESTIONNAIRE = "Create a pre-visit query (ECJU)"
    COMPLIANCE_ACTIONS = "Create a compliance action (ECJU)"
    FOOTNOTES = "Create a reporting footnote"
    LETTER_PARAGRAPH = "Create a letter paragraph"
    PROVISO = "Create a licence condition"
    REPORT_SUMMARY = "Create a report summary"
    STANDARD_ADVICE = "Create an approval reason"
    BACK_LINK = "Back to templates"
    HELP = "Help"
    EDIT_PREFIX = "Edit"

    class Name:
        TITLE = "Name"

    class Text:
        TITLE = "Text"


class EditPicklistItemForm:
    SUCCESS_MESSAGE = "Picklist item updated successfully"


class ReactivatePicklistItem:
    TITLE = "Are you sure you want to reactivate {}?"
    DESCRIPTION = "This will allow internal users to use this picklist item. You can change this in the future"
    BACK_LINK = "Back to {}"
    YES = "Yes"
    NO = "No"
    SUBMIT_BUTTON = "Submit"
    SUCCESS_MESSAGE = "Picklist item reactivated successfully"


class DeactivatePicklistItem:
    TITLE = "Are you sure you want to deactivate {}?"
    DESCRIPTION = "This will prevent internal users from using this picklist item. You can change this in the future"
    BACK_LINK = "Back to {}"
    YES = "Yes"
    NO = "No"
    SUBMIT_BUTTON = "Submit"
    SUCCESS_MESSAGE = "Picklist item deactivated successfully"


class PicklistCategory:
    PROVISO = "Licence conditions"
    STANDARD_ECJU_QUERIES = "Standard queries (ECJU)"
    PRE_VISIT_QUESTIONNAIRES = "Pre-visit queries (ECJU)"
    COMPLIANCE_ACTIONS = "Compliance action queries (ECJU)"
    LETTER_PARAGRAPHS = "Letter paragraphs"
    REPORT_SUMMARIES = "Report summaries"
    STANDARD_ADVICE = "Standard Advice"
    FOOTNOTES = "Reporting footnotes"
