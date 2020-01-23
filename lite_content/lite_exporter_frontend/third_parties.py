from lite_content.lite_exporter_frontend import generic


# TODO Move this into a different file and then delete (there is no app called third_parties)
class UltimateEndUsers:
    BACK = "Back to application overview"
    TITLE = "Ultimate recipients"
    HELP = "What is an ultimate recipient?"
    DESCRIPTION = (
        "An ultimate recipient is an entity that uses the product or the higher level system into which the products are"
        " installed or incorporated. The end user and ultimate recipient may be different entities."
    )
    NOTICE = "There are no ultimate recipients on the application"
    MISSING_DOCS_NOTICE = "You need to attach a document to some ultimate recipients"
    ADD_BUTTON = "Add an ultimate recipient"

    class Document:
        DOWNLOAD = generic.Document.DOWNLOAD
        DELETE = generic.Document.DELETE
        PROCESSING = generic.Document.PROCESSING
        ATTACH = generic.Document.ATTACH
        REMOVE = generic.Document.REMOVE
