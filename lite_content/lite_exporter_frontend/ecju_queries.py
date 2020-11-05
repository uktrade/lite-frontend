from lite_content.lite_exporter_frontend import generic

class Forms:
    class RespondForm:
        BACK_LINK = "Back to ecju queries"
        TITLE = "Respond to query"
        RESPONSE = "Your response"
        SAVE = "Save"

    class ConfirmResponseForm:
        TITLE = "Confirm you want to send this response"
        YES_LABEL = "Confirm and send the response"
        NO_LABEL = "Cancel"
        BACK_LINK = "Back to edit response"
        SUBMIT_BTN = "Continue"


class DocumentsList:
    class AttachDocuments:
        BUTTON = "Add a document"

    class Documents:
        TITLE = "Documents"
        NO_DOCUMENT_ATTACHED = "There are no documents."
        DELETE = generic.Document.DELETE


class SupportingDocumentSensitivityForm:
    TITLE = "Do you have a document for the query and is the document rated OFFICIAL-SENSITIVE or below?"
    DESCRIPTION = (
        "Documentation should be specifications, datasheets, sales brochures, drawings or anything else that fully "
        "details what the query is and what it's designed to do."
    )
    ECJU_HELPLINE = (
        "**<noscript>If the answer is No;</noscript>**\n\nContact ECJU to arrange a more secure way to send "
        "this document.\n\n You can continue with the application "
        "without attaching a document.\n\n**ECJU helpline**\n 020 7215 4594\n "
        "[Find out about call charges](https://www.gov.uk/call-charges)"
    )
    SUBMIT_BUTTON = "Continue"
    BACK_BUTTON = "Back to respond to query"
    LABEL = "Missing document reason"

    class Options:
        YES = "Yes"
        NO = "No"


class UploadDocumentForm:
    TITLE = "Upload a document"
    DESCRIPTION = (
        "Documentation could be specifications, datasheets, sales brochures, drawings "
        "or anything else that fully details what the query is and what it's designed to do."
        "\n\nDo not attach a document that’s above OFFICIAL-SENSITIVE. "
        "\n\nThe file must be smaller than 50MB."
    )
    BUTTON = "Save"
    BACK_FORM_LINK = "Back"

    class Description:
        TITLE = "Description"


class SupportingDocumentDeletePage:
    TITLE = "Confirm you want to delete this document"
    BACK = "Back to respond to query"
    DOCUMENT_NAME = "Name"
    DOCUMENT_CREATED_AT = "Created at"
    DOCUMENT_CREATED_BY = "Created by"
    DOCUMENT_DESCRIPTION = "Description"
    BUTTON = "Delete document"
