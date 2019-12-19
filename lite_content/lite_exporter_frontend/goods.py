from conf.settings import env

PERMISSION_FINDER_LINK = "[control list](" + env("PERMISSIONS_FINDER_URL") + ")"


class GoodsList:
    TITLE = "Products"
    CREATE_GOOD = "Add a product"

    class Count:
        ORGANISATION_ZERO = "Your organisation doesn't have any products."
        ORGANISATION_ONE = "Your organisation has 1 product"
        ORGANISATION_MANY = "Your organisation has %s products"  # %s will add the count of goods
        FILTERED_ZERO = "There are no products based on filter"
        FILTERED_ONE = "Displaying 1 product"
        FILTERED_MANY = "Displaying %s products"  # %s will add the count of goods

    class Filter:
        DESCRIPTION = "Description"
        CONTROL_LIST_ENTRY = "Control list entry"
        PART_NUMBER = "Part number"
        APPLY = "Apply filters"
        CLEAR = "Clear filters"
        SHOW = "Show filters"
        HIDE = "Hide filters"

    class Table:
        DESCRIPTION = "Description"
        CONTROL_LIST_ENTRY = "Control list entry"
        PART_NUMBER = "Part number"
        STATUS = "Status"


class DocumentSensitivityForm:
    TITLE = "Does your product documentation meet the following criteria?"
    DESCRIPTION = (
        "I have a document for my product.\nDocumentation should be specifications, datasheets, sales brochures, "
        "drawings or anything else that fully details what the product is and what it's designed to do.\n\n"
        "The document is below OFFICIAL-SENSITIVE.\n\nThe document is not commercially sensitive."
    )
    ECJU_HELPLINE = (
        "**<noscript>If the answer is No;</noscript>**\n\nContact ECJU to arrange a more secure way to send "
        "this document.\n\n You can continue with the application "
        "without attaching a document.\n\n **ECJU helpline**\n 020 7215 4594.\n "
        "[Find out about call charges](https://www.gov.uk/call-charges)"
    )
    BUTTON = "Continue"

    class Options:
        YES = "Yes"
        NO = "No"


class CreateGoodForm:
    TITLE = "Add a product"
    BUTTON = "Save"

    class Description:
        TITLE = "Description"
        DESCRIPTION = "This can make it easier to find your product later"

    class IsControlled:
        TITLE = "Is the product controlled?"
        DESCRIPTION = "If you don't know you can use " + PERMISSION_FINDER_LINK
        CLC_REQUIRED = (
            "Products that aren't on the "
            + PERMISSION_FINDER_LINK
            + "may be affected by military end use controls, current trade sanctions and embargoes or weapons of mass "
            + "destruction controls. If your products and services aren't subject to any controls, you'll get a no "
            + "licence required (NLR) document from ECJU. "
        )
        YES = "Yes"
        NO = "No"
        UNSURE = "I don't know"

    class ControlListEntry:
        TITLE = "Control list classification"
        DESCRIPTION = (
            "<noscript>If your product is controlled, enter its control list classification. </noscript>"
            "For example, ML1a. "
        )

    class Incorporated:
        TITLE = "Will the product be incorporated into another product?"
        DESCRIPTION = ""
        YES = "Yes"
        NO = "No"

    class PartNumber:
        TITLE = "Part number (optional)"


class CLCQueryForm:
    TITLE = "Create a CLC query"
    DESCRIPTION = "By submitting you are creating a CLC query that cannot be altered"
    BACK_LINK = "Back to product"
    BUTTON = "Save"

    class CLCCode:
        TITLE = "What do you think is your product's control list entry?"
        DESCRIPTION = "For example, ML1a."

    class Additional:
        TITLE = "Further details about your product"
        DESCRIPTION = "Please enter details of why you don't know if your product is controlled"


class EditGoodForm:
    TITLE = "Edit product"
    DESCRIPTION = ""

    class Description:
        TITLE = "Description"
        DESCRIPTION = "This can make it easier to find your product later"

    class IsControlled:
        TITLE = "Is your product controlled?"
        DESCRIPTION = "If you don't know you can use " + PERMISSION_FINDER_LINK
        YES = "Yes"
        NO = "No"
        UNSURE = "I don't know"

    class ControlListEntry:
        TITLE = "Control list classification"
        DESCRIPTION = (
            "<noscript>If your product is controlled, enter its control list entry. </noscript>For example, " "ML1a. "
        )

    class Incorporated:
        TITLE = "Will the product be incorporated into another product?"
        DESCRIPTION = ""
        YES = "Yes"
        NO = "No"

    class PartNumber:
        TITLE = "Part number (optional)"

    class Buttons:
        SAVE = "Save"
        DELETE = "Delete product"

    class DeleteConfirmationForm:
        TITLE = "Are you sure you want to delete this product?"
        YES = "Yes, delete the product"
        NO = "Cancel"


class AttachDocumentForm:
    TITLE = "Attach a document"
    DESCRIPTION = (
        "Documentation could be specifications, datasheets, sales brochures, drawings "
        "or anything else that fully details what the item is and what it's designed to do."
        "\n\nDo not attach a document that’s OFFICIAL-SENSITIVE or above. "
        "\n\nThe file must be smaller than 100MB."
    )
    BUTTON = "Save"
    BACK_LINK = "Back to Good"

    class Description:
        TITLE = "Description (optional)"


class RespondToQueryForm:
    TITLE = "Respond to query"
    BUTTON = "Submit response"
    BACK_LINK = "Back to product"

    class Response:
        TITLE = "Your response"
        DESCRIPTION = "You won't be able to edit this once you've submitted it."

    class ConfirmationForm:
        TITLE = "Are you sure you want to send this response?"
        BACK_LINK = "Back to edit response"
        YES = "Yes, send the response"
        NO = "No, change my response"


class CreateGoodOnApplicationForm:
    TITLE = "Details for product on application"
    DOCUMENT_MISSING = "A document is required"
    BACK_LINK = "Back to products"
    VALUE = "What's the value of your products?"
    QUANTITY = "Quantity"
    UNITS = "Unit of measurement"


class AddPrexistingGoodToApplicationForm:
    TITLE = "Add a product from your database to your application"


class ViewGoodOnApplicationPage:
    TITLE = "Products"
    ADD_NEW_BUTTON = "Add a new product to your application"


class GoodsLocationForm:
    WHERE_ARE_YOUR_GOODS_LOCATED_TITLE = "Where are your products located?"
    WHERE_ARE_YOUR_GOODS_LOCATED_DESCRIPTION = ""
    ONE_OF_MY_REGISTERED_SITES = "At one of my organisation’s sites"
    NOT_AT_MY_REGISTERED_SITES = "At a location that's not part of my organisation"
    EXTERNAL_LOCATION_TITLE = "Do you want to add a new external location or use an existing one?"
    EXTERNAL_LOCATION_NEW_LOCATION = "Add a new external location"
    EXTERNAL_LOCATION_PREEXISTING_LOCATION = "Use an existing external location"


class GoodsLocationPage:
    SELECT_SITES_TITLE = "Select which sites your products are at"
    SELECT_SITES_BUTTON = "Select sites"


class GoodsPage:
    NOTIFICATIONS = "Notifications"


class AttachDocumentPage:
    UPLOAD_FAILURE_ERROR = "We had an issue uploading your files. Try again later."
    UPLOAD_GENERIC_ERROR = "We had an issue creating your response. Try again later."
