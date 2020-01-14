from lite_content.lite_exporter_frontend import generic
from lite_content.lite_exporter_frontend.generic import PERMISSION_FINDER_LINK


class GoodsList:
    TITLE = "Products"
    CREATE_GOOD = "Add a product"
    GOOD = "Product"
    VERIFIED = "This product has been verified by ECJU based on the information provided"
    EDIT_GOOD_LINK = "Edit product"
    IN_REVIEW = (
        "Your product is currently being reviewed by ECJU. "
        "It has limited functionality until the review is complete."
    )
    YOUR_GOOD = "Product"
    NO_LONGER_CAN_BE_CHANGED = "Your product has been used in an application and can therefore no longer be changed."

    class Count:
        ORGANISATION_ZERO = "Your organisation doesn't have any products."
        ORGANISATION_ONE = "Your organisation has 1 product"
        ORGANISATION_MANY = "Your organisation has %s products"  # %s will add the count of goods
        FILTERED_ZERO = "There are no products based on filter"
        FILTERED_ONE = "Displaying 1 product"
        FILTERED_MANY = "Displaying %s products"  # %s will add the count of goods

    class Filter:
        DESCRIPTION = generic.DESCRIPTION
        CONTROL_LIST_ENTRY = "Control list classification"
        PART_NUMBER = generic.PART_NUMBER
        APPLY = "Apply filters"
        CLEAR = "Clear filters"
        SHOW = "Show filters"
        HIDE = "Hide filters"

    class Table:
        DESCRIPTION = generic.DESCRIPTION
        CONTROL_LIST_ENTRY = "Control list classification"
        IS_GOOD_CONTROLLED = "Is the product on the control list?"
        PART_NUMBER = generic.PART_NUMBER
        QUANTITY = "Quantity"
        VALUE = "Value"
        INCORPORATED = "Incorporated"
        COUNTRIES = "Countries"
        STATUS = "Status"

    class Documents:
        TITLE = "Documents"
        NO_DOCUMENT_ATTACHED = "The product has no documents attached"
        NAME = "Name"
        DESCRIPTION = "Description"
        UPLOADED_BY = "Uploaded by"


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
    TITLE = "Add product"
    BUTTON = "Save and continue"

    class Description:
        TITLE = generic.DESCRIPTION
        DESCRIPTION = "Include the product name to make it easier to find the product when needed."

    class IsControlled:
        TITLE = "Is the product on the control list?"
        DESCRIPTION = "If you don't know you can use " + PERMISSION_FINDER_LINK
        CLC_REQUIRED = (
            "Products that aren't on the " + PERMISSION_FINDER_LINK + " may be affected by [military end use controls]"
            "(https://www.gov.uk/guidance/export-controls-military-goods-software-and-technology), "
            "[current trade sanctions and embargoes]"
            "(https://www.gov.uk/guidance/current-arms-embargoes-and-other-restrictions) or "
            "[weapons of mass destruction controls](https://www.gov.uk/guidance/supplementary-wmd-end-use-controls). "
            "If the product isn't subject to any controls, you'll get a no licence required (NLR) document from ECJU."
        )
        YES = "Yes"
        NO = "No"
        UNSURE = "I don't know"

    class ControlListEntry:
        TITLE = "Control list classification"
        DESCRIPTION = "For example, ML1a."

    class PartNumber:
        TITLE = generic.PART_NUMBER


class CLCQueryForm:
    TITLE = "Create a CLC query"
    DESCRIPTION = "By submitting you are creating a CLC query that cannot be altered"
    BACK_LINK = "Back to product"
    BUTTON = "Save"

    class CLCCode:
        TITLE = "What do you think is the product's control list classification? (optional)"
        DESCRIPTION = "For example, ML1a."

    class Additional:
        TITLE = "Product details (optional)"
        DESCRIPTION = "Include details of why you don't know if the product is controlled."


class EditGoodForm:
    TITLE = "Edit product"
    DESCRIPTION = ""

    class Description:
        TITLE = "Description"
        DESCRIPTION = "Include the product name to make it easier to find the product when needed."

    class IsControlled:
        TITLE = "Is the product on the control list?"
        DESCRIPTION = (
            "Products that aren't on the " + PERMISSION_FINDER_LINK + "may be affected "
            "by military end use controls, current trade sanctions and embargoes or weapons of "
            "mass destruction controls. If the product isn't subject to any controls, you'll get "
            "a no licence required (NLR) document from ECJU."
        )
        YES = "Yes"
        NO = "No"
        UNSURE = "I don't know"

    class ControlListEntry:
        TITLE = "Control list classification"
        DESCRIPTION = "For example, ML1a."

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
        TITLE = "Confirm you want to delete this product"
        YES = "Confirm and delete the product"
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
    BACK_LINK = "Back to product"

    class Description:
        TITLE = "Description (optional)"


class RespondToQueryForm:
    TITLE = "Respond to query"
    BUTTON = "Submit response"
    BACK_LINK = "Back to product"

    class Response:
        TITLE = "Your response"
        DESCRIPTION = "You won't be able to edit the response once it's submitted."

    class ConfirmationForm:
        TITLE = "Confirm you want to send the response?"
        BACK_LINK = "Back to edit response"
        YES = "Confirm and send the response"
        NO = "Cancel and change the response"


class GoodPage:
    class Tabs:
        DETAILS = "Details"
        NOTES = "Notes"
        ECJU_QUERIES = "ECJU queries"
        GENERATED_DOCUMENTS = "ECJU documents"

    class Query:
        CASE_OFFICER = "Case officer"
        NO_ASSIGNED_CASE_OFFICER = "Not assigned"
        REFERENCE = "Reference"


class AddGoodToApplicationForm:
    TITLE = "Add a product to your application"
    DESCRIPTION = ""
    DOCUMENT_MISSING = "A document is required"
    BACK_LINK = "Back to products"

    class Value:
        TITLE = "Value of your products"
        DESCRIPTION = ""

    class VALUE:
        TITLE = "Total value"
        DESCRIPTION = ""

    class Quantity:
        TITLE = "Quantity"
        DESCRIPTION = ""

    class Units:
        TITLE = "Unit of measurement"
        DESCRIPTION = ""

    class Incorporated:
        TITLE = "Is this product incorporated?"
        DESCRIPTION = ""
        YES = "Yes"
        NO = "No"


class AddPreexistingGoodToApplicationForm:
    TITLE = "Select a product from your product list"


class ViewGoodOnApplicationPage:
    TITLE = "Products"
    ADD_NEW_BUTTON = "Add a new product"


class GoodsLocationForm:
    WHERE_ARE_YOUR_GOODS_LOCATED_TITLE = "Where are the products located?"
    WHERE_ARE_YOUR_GOODS_LOCATED_DESCRIPTION = ""
    ONE_OF_MY_REGISTERED_SITES = "At one of my organisation’s sites"
    NOT_AT_MY_REGISTERED_SITES = "At a location that's not part of my organisation"
    EXTERNAL_LOCATION_TITLE = "Do you want to add a new external location or use an existing one?"
    EXTERNAL_LOCATION_NEW_LOCATION = "Add a new external location"
    EXTERNAL_LOCATION_PREEXISTING_LOCATION = "Use an existing external location"


class GoodsCountriesMatrix:
    BACK = "Back to application overview"
    TITLE = "Select the countries each product is going to (optional)"
    ERROR = "Select at least 1 country for each product"
    THIS_IS_OPTIONAL = ""
    SELECT_ALL = "Select all"
    DESELECT_ALL = "Deselect all"
    SAVE = "Save"


class GoodsLocationPage:
    SELECT_SITES_TITLE = "Products locations"
    SELECT_SITES_BUTTON = "Select sites"


class GoodsPage:
    NOTIFICATIONS = "Notifications"


class AttachDocumentPage:
    UPLOAD_FAILURE_ERROR = "We had an issue uploading your files. Try again later."
    UPLOAD_GENERIC_ERROR = "We had an issue creating your response. Try again later."
