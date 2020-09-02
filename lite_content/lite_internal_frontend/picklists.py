class Picklists:
    ADD_BUTTON = "Add an item"
    ITEMS_COUNT = "item in total/items in total"
    SELECT_OPTION = "Select an option"


class PicklistItem:
    EDIT_BUTTON = "Edit item"
    DEACTIVATE_BUTTON = "Deactivate item"
    REACTIVATE_BUTTON = "Reactivate item"


class PicklistPicker:
    NO_CONTENT_NOTICE = "There aren't any items in this picklist"


class NewPicklistForm:
    ECJU_QUERY = "Create an ECJU query"
    PRE_VISIT_QUESTIONNAIRE = "Create a Pre-Visit Questionnaire Question (ECJU Query)"
    COMPLIANCE_ACTIONS = "Create a Compliance Actions (ECJU Query)"
    FOOTNOTES = "Create a footnote"
    LETTER_PARAGRAPH = "Create a letter paragraph"
    PROVISO = "Create a proviso"
    REPORT_SUMMARY = "Create a report summary"
    STANDARD_ADVICE = "Create standard advice"
    BACK_LINK = "Back to picklists"
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
    PROVISO = "Provisos"
    STANDARD_ECJU_QUERIES = "Standard ECJU Queries"
    PRE_VISIT_QUESTIONNAIRES = "Pre-Visit Questionnaire questions (ECJU Query)"
    COMPLIANCE_ACTIONS = "Compliance Actions (ECJU Query)"
    LETTER_PARAGRAPHS = "Letter Paragraphs"
    REPORT_SUMMARIES = "Report Summaries"
    STANDARD_ADVICE = "Standard Advice"
    FOOTNOTES = "Footnotes"
