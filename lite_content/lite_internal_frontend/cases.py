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

    EDIT_FLAGS = "Edit goods flags"
    REVIEW_GOODS = "Review Goods"
    ADVICE = "Give or change advice"
    RESPOND_BUTTON = "Respond to Query"
    CLOSED = "This case is closed"


class GenerateDocumentsPage:
    TITLE = "Generate Document"
    ERROR = "Document Generation is unavailable at this time"

    class SelectTemplateForm:
        BACK_LINK = "Back to Case"


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
