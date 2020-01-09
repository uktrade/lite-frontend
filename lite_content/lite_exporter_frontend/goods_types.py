from lite_content.lite_exporter_frontend import generic
from lite_content.lite_exporter_frontend.strings import PERMISSION_FINDER_LINK


class Overview:
    BACK = generic.BACK_TO_APPLICATION_OVERVIEW
    TITLE = "Add products"
    ADD_GOODS_TYPE_BUTTON = "Add a product"
    ADD_ANOTHER_GOODS_TYPE_BUTTON = "Add another product"


class Variables:
    DESCRIPTION = generic.DESCRIPTION
    CONTROL_LIST_ENTRY = generic.CONTROL_LIST_ENTRY
    INCORPORATED = generic.INCORPORATED
    DOCUMENT = "Document"


class OverviewGoodTypes:
    NO_GOOD_TYPES = "There are no products to show. To add a product use the Add a product button"
    TITLE = "Your products"


class Documents:
    SAVE_END_USER = "save your progress and return to your application later"

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
        FILE_TOO_LARGE = "The file you tried to upload is too large."
        TITLE = "Upload a document to support your product (optional)"
        UPLOAD_ERROR = "We had an issue uploading your files. Try again later."


class CreateGoodsTypeForm:
    TITLE = "Add a new product to your application"

    class Description:
        TITLE = "Description"
        DESCRIPTION = "Include the product name to make it easier to find the product when needed."

    class IsControlled:
        TITLE = "Are the products controlled??"
        DESCRIPTION = (
            "Products that aren't on the "
            + PERMISSION_FINDER_LINK
            + " may be affected by military end use controls, current trade sanctions and embargoes or weapons of "
              "mass destruction controls. If your products aren't subject to any controls, you'll get a no licence "
              "required (NLR) document from ECJU."
        )
        YES = "Yes"
        NO = "No"

    class IsIncorporated:
        TITLE = "Will the products be incorporated into other products?"
        DESCRIPTION = ""
        YES = "Yes"
        NO = "No"
