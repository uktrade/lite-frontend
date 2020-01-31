from lite_content.lite_exporter_frontend import generic
from lite_content.lite_exporter_frontend.generic import PERMISSION_FINDER_LINK


class OverviewPage:
    BACK = generic.BACK_TO_APPLICATION_OVERVIEW
    TITLE = "Products"
    ADD_GOODS_TYPE_BUTTON = "Add products"
    ADD_ANOTHER_GOODS_TYPE_BUTTON = "Add another product"
    NO_GOODS = "The are no products on the application"


class Variables:
    DESCRIPTION = generic.DESCRIPTION
    CONTROL_LIST_ENTRY = "Control list classification"
    INCORPORATED = generic.INCORPORATED
    REMOVE_GOODS_TYPE = "Remove product"


class Document:
    TITLE = "Document"
    DOWNLOAD = generic.Document.DOWNLOAD
    DELETE = generic.Document.DELETE
    PROCESSING = generic.Document.PROCESSING
    ATTACH = generic.Document.ATTACH
    REMOVE = generic.Document.REMOVE


class Documents:
    SAVE_END_USER = "save your progress and return to the application later"

    class AttachDocuments:
        BACK_TO_APPLICATION_OVERVIEW = "Back to additional documents overview"
        BUTTON = "Attach document"
        DELETE_ERROR = "We had an issue deleting your files. Try again later."
        DESCRIPTION = (
            "Do not attach a document that\u2019s OFFICIAL-SENSITIVE or above.\n\nThe file must be"
            " smaller than 100MB."
        )
        DESCRIPTION_FIELD_DETAILS = ""
        DESCRIPTION_FIELD_TITLE = "Description (optional)"
        DOWNLOAD_ERROR = "We had an issue downloading your file. Try again later."
        FILE_TOO_LARGE = "The selected file must be smaller than 100MB"
        TITLE = "Upload a document to support your product (optional)"
        UPLOAD_ERROR = "We had an issue uploading your files. Try again later."


class CreateGoodsTypeForm:
    TITLE = "Add a new product category to your application"
    DESCRIPTION = ""

    class Description:
        TITLE = "Description"
        DESCRIPTION = "Start with the product name to make it easier to find the product when needed."

    class IsControlled:
        TITLE = "Is the product on the control list?"
        DESCRIPTION = (
            "Products that aren't on the " + PERMISSION_FINDER_LINK + " may be affected by "
            "[military end use controls](https://www.gov.uk/guidance/export-controls-military-goods-software-and-technology), "
            "[current trade sanctions and embargoes](https://www.gov.uk/guidance/current-arms-embargoes-and-other-restrictions) or "
            "[weapons of mass destruction controls](https://www.gov.uk/guidance/supplementary-wmd-end-use-controls). "
            "If the products aren't subject to any controls, you'll get a no licence required (NLR) document from ECJU."
        )
        YES = "Yes"
        NO = "No"

    class IsIncorporated:
        TITLE = "Will the products be incorporated into other products?"
        DESCRIPTION = ""
        YES = "Yes"
        NO = "No"
