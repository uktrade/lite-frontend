class CaseDocumentsPage:
    title = "Case Documents"
    back_link = "Back to Case"
    attach = "Attach Document"
    generate = "Generate Document"


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


class GenerateDocumentsPage:
    TITLE = "Generate Document"
    ERROR = "Document Generation is unavailable at this time"

    class SelectTemplateForm:
        BACK_LINK = "Back to Case"
