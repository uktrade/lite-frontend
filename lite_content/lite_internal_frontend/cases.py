class CaseDocumentsPage:
    BACK_LINK = "Back to Case"
    ATTACH = "Attach Document"
    GENERATE = "Generate Document"


class ApplicationPage:
    class Actions:
        DOCUMENT = "Attached Documents"
        ECJU = "ECJU Queries"
        MOVE = "Move Case"
        CHANGE_STATUS = "Change Status"
        DECISION = "Record Decision"
        ADVICE = "View Advice"
        GENERATE_DOCUMENT = "Generate Document"

    EDIT_FLAGS = "Edit products flags"
    REVIEW_GOODS = "Review Products"
    ADVICE = "Give or change advice"
    RESPOND_BUTTON = "Respond to Query"
    CLOSED = "This case is closed"


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
        CHANGE_STATUS = "Change Status"
        DOCUMENT = "Attached Documents"
        ECJU = "ECJU Queries"
        MOVE = "Move Case"


class HMRCPage:
    class Actions:
        CHANGE_STATUS = "Change Status"
        DOCUMENT = "Attached Documents"
        MOVE = "Move Case"
        RECORD_DECISION = "Record Decision"
        GENERATE_DOCUMENT = "Generate Document"
