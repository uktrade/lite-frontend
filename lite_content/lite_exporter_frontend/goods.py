from lite_content.lite_exporter_frontend import generic
from lite_content.lite_exporter_frontend.generic import PERMISSION_FINDER_LINK


class GoodsList:
    TITLE = "Product list"
    CREATE_GOOD = "Add a product"

    class Count:
        ORGANISATION_ZERO = "Your organisation has no products listed."
        ORGANISATION_ONE = "Your organisation has 1 product listed"
        ORGANISATION_MANY = "Your organisation has %s products listed"  # %s will add the count of goods
        FILTERED_ZERO = "No products match your filters"
        FILTERED_ONE = "1 product matches your filters"
        FILTERED_MANY = "%s products match your filters"  # %s will add the count of goods

    class Filter:
        DESCRIPTION = generic.DESCRIPTION
        CONTROL_LIST_ENTRY = "Control list classification (CLC)"
        PART_NUMBER = generic.PART_NUMBER
        APPLY = "Apply filters"
        CLEAR = "Clear filters"
        SHOW = "Show filters"
        HIDE = "Hide filters"

    class Table:
        DESCRIPTION = generic.DESCRIPTION
        CONTROL_LIST_ENTRY = "Control list entries"
        IS_GOOD_CONTROLLED = "Controlled"
        PART_NUMBER = generic.PART_NUMBER
        QUANTITY = "Quantity"
        VALUE = "Value"
        INCORPORATED = "Incorporated"
        COUNTRIES = "Destinations"
        STATUS = "Status"
        PRODUCT_TYPE = "Product type"

    class Documents:
        TITLE = "Documents"
        NO_DOCUMENT_ATTACHED = "There are no documents."
        NAME = "File"
        DESCRIPTION = "Description"
        UPLOADED_BY = "Uploaded by"


class GoodPage:
    TITLE = "Product"
    ADD_TO_APPLICATION = "Add to application"
    DELETE_GOOD = "Delete product"
    YOUR_QUERY_HEADING = "Your query"
    VERIFIED = "ECJU has verified this product based on the information provided"
    IN_REVIEW = "ECJU is currently reviewing this product."
    YOUR_GOOD = "Product"
    NO_LONGER_CAN_BE_CHANGED = "This product has been used on an application so can’t be edited."

    class Tabs:
        DETAILS = "Details"
        NOTES = "Notes"
        ECJU_QUERIES = "ECJU queries"
        GENERATED_DOCUMENTS = "ECJU documents"

    class Query:
        TITLE = "Product query"
        CASE_OFFICER = "Case officer"
        NO_ASSIGNED_CASE_OFFICER = "Not assigned"
        REFERENCE = "ECJU reference"
        CLC_RAISED_REASONS = "CLC query reasons"
        GRADING_RAISED_REASONS = "Grading query reasons"

    class Document:
        DOWNLOAD = generic.Document.DOWNLOAD
        DELETE = generic.Document.DELETE
        PROCESSING = generic.Document.PROCESSING
        ATTACH = generic.Document.ATTACH
        REMOVE = generic.Document.REMOVE

    class Table:
        DESCRIPTION = "Description"
        IS_GOOD_CONTROLLED = "Controlled"
        CONTROL_LIST_ENTRY = "CLC"
        CATEGORY = "Category"
        MILITARY_USE = "Military use"
        COMPONENT = "Component"
        INFORMATION_SECURITY_FEATURES = "Information security features"
        PURPOSE_SOFTWARE_TECHNOLOGY = "Purpose"

        class Grading:
            IS_GRADED = "Security graded"
            GRADING = "Grade"
            REFERENCE = "Reference"
            ISSUING_AUTHORITY = "Issuing authority"
            DATE_OF_ISSUE = "Date of issue"

        class FirearmDetails:
            PRODUCT_TYPE = "Product type"
            YEAR_OF_MANUFACTURE = "Year of manufacture"
            REPLICA_FIREARM = "Replica firearm"
            CALIBRE = "Calibre"
            COVERED_BY_THE_FIREARMS_ACT_1968 = "Firearms Act 1968"
            IDENTIFICATION_MARKINGS = "Serial numbers"
            IDENTIFICATION_MARKINGS = "Identification markings"


class DocumentAvailabilityForm:
    TITLE = "Do you have a document that shows what your product is and what it’s designed to do?"
    DESCRIPTION = (
        "For example, a technical specification, datasheet, sales brochure or something else that fully describes the product details."
        "\nThis is required in order to process the application."
    )
    NO_DOCUMENT_TEXTFIELD_DESCRIPTION = (
        "Explain why you are not able to upload a product document. This may delay your application."
    )
    SUBMIT_BUTTON = "Continue"


class DocumentSensitivityForm:
    TITLE = "Is the document rated above OFFICIAL-SENSITIVE?"
    ECJU_HELPLINE = (
        "**<noscript>If the answer is No;</noscript>**\n\nContact ECJU to arrange a more secure way to send "
        "this document.\n\n You can continue with the application "
        "without attaching a document.\n\n**ECJU helpline**\n 020 7215 4594\n "
        "[Find out about call charges (opens in new tab)](https://www.gov.uk/call-charges)"
    )
    SUBMIT_BUTTON = "Save and continue"

    class Options:
        YES = "Yes"
        NO = "No"


class CreateGoodForm:
    TITLE_APPLICATION = "Add a product to your application"
    TITLE_GOODS_LIST = "Add a product to your product list"
    SUBMIT_BUTTON = "Continue"
    BACK_BUTTON = "Back"

    class Description:
        TITLE = generic.DESCRIPTION
        DESCRIPTION = (
            "Start with the product name to make it easier to find the product when needed. Include the commodity code "
            "if you know it."
        )

    class IsControlled:
        TITLE = "Is the product on the control list?"
        DESCRIPTION = (
            "Products that aren't on the " + PERMISSION_FINDER_LINK + " may be affected by [military end use controls]"
            "(https://www.gov.uk/guidance/export-controls-military-goods-software-and-technology), "
            "[current trade sanctions and embargoes]"
            "(https://www.gov.uk/guidance/current-arms-embargoes-and-other-restrictions) or "
            "[weapons of mass destruction controls](https://www.gov.uk/guidance/supplementary-wmd-end-use-controls). "
            "If the product isn't subject to any controls, you'll get a no licence required (NLR) document from ECJU."
        )
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
        UNSURE = "I don't know, raise a control list classification (CLC) query"

    class ControlListEntry:
        TITLE = "Control list entries"
        DESCRIPTION = "Type to get suggestions. For example, ML1a."

    class IsGraded:
        TITLE = "Does the product have a security grading?"
        DESCRIPTION = (
            "For example, UK OFFICIAL or NATO UNCLASSIFIED. The security grading of the product doesn't affect if an "
            "export licence is needed."
        )
        YES = "Yes"
        NO = "No, it doesn't need one"
        RAISE_QUERY = "No, it needs one, apply for a private venture (PV) grading"

    class PartNumber:
        TITLE = generic.PART_NUMBER

    class ProductCategory:
        TITLE = "Select a product category"
        GROUP1_PLATFORM = "Platform, vehicle, system or machine"
        GROUP1_DEVICE = "Device, equipment or object"
        GROUP1_COMPONENTS = "Components, modules or accessories of something"
        GROUP1_MATERIALS = "Materials or substances"
        GROUP2_FIREARMS = "Firearms"
        GROUP3_SOFTWARE = "Software"
        GROUP3_TECHNOLOGY = "Technology"

    class MilitaryUse:
        TITLE = "Is the product for military use?"
        YES_DESIGNED = "Yes, specially designed for military use"
        YES_MODIFIED = "Yes, modified for military use"
        MODIFIED_MILITARY_USE_DETAILS = "Provide details of the modifications"
        NO = "No"

    class ProductComponent:
        TITLE = "Is the product a component?"
        YES_DESIGNED = "Yes, it's designed specially for hardware"
        YES_MODIFIED = "Yes, it's been modified for hardware"
        YES_GENERAL_PURPOSE = "Yes, it's a general purpose component"
        NO = "No"
        DESIGNED_DETAILS = "Provide details of the hardware"
        MODIFIED_DETAILS = "Provide details of the modifications and the hardware"
        GENERAL_DETAILS = "Provide details of the types of applications it's intended to be used in"

    class ProductInformationSecurity:
        TITLE = "Is the product designed to employ 'information security' features?"
        INFORMATION_SECURITY_DETAILS = "Provide details of the information security features"
        NO = "No"

    class TechnologySoftware:
        TITLE = "Describe the purpose of the "

    class FirearmGood:
        class ProductType:
            TITLE = "Select the type of product"
            BUTTON_TEXT = "Continue"

            FIREARM = "Firearm"
            COMPONENTS_FOR_FIREARM = "Component of a firearm"
            AMMUNITION = "Ammunition"
            COMPONENTS_FOR_AMMUNITION = "Component of firearm ammunition"
            FIREARMS_ACCESSORY = "Accessory of a firearm"
            SOFTWARE_RELATED_TO_FIREARM = "Software relating to a firearm"
            TECHNOLOGY_RELATED_TO_FIREARM = "Technology relating to a firearm"

        class FirearmsAmmunitionDetails:
            TITLE = "Firearms and ammunition details"
            YEAR_OF_MANUFACTURE = "Year of manufacture"
            CALIBRE = "Enter the calibre"

        class FirearmsReplica:
            TITLE = "Is the product a replica firearm?"
            DESCRIPTION = "Describe the firearm the product is a replica of"

        class FirearmsActCertificate:
            TITLE = "Is the product covered by Section 1, 2 or 5 of the Firearms Act 1968?"

            FIREARMS_ACT = "Firearms Act 1968:"
            SECTION_ONE = "Section 1 (opens in new tab)"
            SECTION_ONE_LINK = "http://www.legislation.gov.uk/ukpga/1968/27/section/1"
            SECTION_TWO = "Section 2 (opens in new tab)"
            SECTION_TWO_LINK = "http://www.legislation.gov.uk/ukpga/1968/27/section/2"
            SECTION_FIVE = "Section 5 (opens in new tab)"
            SECTION_FIVE_LINK = "http://www.legislation.gov.uk/ukpga/1968/27/section/5"

            SECTION_CERTIFICATE_NUMBER = "Certificate number"
            EXPIRY_DATE = "Expiry date"
            EXPIRY_DATE_HINT = "For example, 12 11 2022"
            YES = "Yes"
            NO = "No"
            DONT_KNOW = "I don't know"

        class IdentificationMarkings:
            TITLE = "Will each product have a serial number or other identification marking?"
            NO_MARKINGS_DETAILS = "Explain why the product has not been marked"
            YES_NOW = "Yes, I can add serial numbers now"
            YES_LATER = "Yes, I can add serial numbers later"
            NO = "No"

            BUTTON_TEXT = "Continue"


class GoodGradingForm:
    TITLE = "Security grading"
    DESCRIPTION = ""

    PREFIX = "Prefix"
    GRADING = "Grading"
    SUFFIX = "Suffix"
    OTHER_GRADING = "Other type of security grading"
    ISSUING_AUTHORITY = "Issuing authority"
    REFERENCE = "Reference"
    DATE_OF_ISSUE = "Date of issue"

    BUTTON = "Save and continue"


class GoodsQueryForm:
    TITLE = "Product query"
    DESCRIPTION = ""
    BACK_LINK = "Back to product"
    BUTTON = "Submit"

    class CLCQuery:
        TITLE = "Raise a control list classification (CLC) query"

        class Code:
            TITLE = "What do you think the CLC is for the product?"
            DESCRIPTION = "For example, ML1a."

        class Details:
            TITLE = "Comments"

    class PVGrading:
        TITLE = "Apply for a private venture (PV) grading"

        class Details:
            TITLE = "Comments"

    class Additional:
        TITLE = "Comments"
        DESCRIPTION = "Include details of why you don't know if the product is controlled."


class EditGoodForm:
    TITLE = "Edit product"
    DESCRIPTION = ""

    class Description:
        TITLE = "Description"
        DESCRIPTION = (
            "Start with the product name to make it easier to find the product when needed. Include the commodity code "
            "if you know it."
        )

    class IsControlled:
        TITLE = "Is the product on the control list?"
        DESCRIPTION = (
            "Products that aren't on the " + PERMISSION_FINDER_LINK + " may be affected by "
            "[military end use controls](https://www.gov.uk/guidance/export-controls-military-goods-software-and-technology), "
            "[current trade sanctions and embargoes](https://www.gov.uk/guidance/current-arms-embargoes-and-other-restrictions) or "
            "[weapons of mass destruction controls](https://www.gov.uk/guidance/supplementary-wmd-end-use-controls). "
            "If the product isn't subject to any controls, you'll get a no licence required (NLR) document from ECJU."
        )
        YES = "Yes"
        NO = "No"
        UNSURE = "I don't know, raise a control list classification (CLC) query"

    class ControlListEntry:
        TITLE = "Control list entries"
        DESCRIPTION = "Type to get suggestions. For example, ML1a."

    class Incorporated:
        TITLE = "Will the product be incorporated into another product?"
        DESCRIPTION = ""
        YES = "Yes"
        NO = "No"

    class PartNumber:
        TITLE = "Part number"

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
        "or anything else that fully details what the product is and what it's designed to do."
        "\n\nDo not attach a document that’s above OFFICIAL-SENSITIVE. "
        "\n\nThe file must be smaller than 50MB."
    )
    BUTTON = "Save and continue"
    BACK_FORM_LINK = "Back"
    BACK_GOOD_LINK = "Back to product"

    class Description:
        TITLE = "Description"


class RespondToQueryForm:
    TITLE = "Respond to ECJU query"
    BUTTON = "Submit response"
    BACK_LINK = "Back to product"

    class Response:
        TITLE = "Your response"
        DESCRIPTION = ""

    class ConfirmationForm:
        TITLE = "Confirm you want to send the response"
        BACK_LINK = "Back to edit response"
        YES = "Confirm and send the response"
        NO = "Cancel and change the response"


class AddGoodToApplicationForm:
    TITLE = "Quantity and value of the product"
    DESCRIPTION = ""
    DOCUMENT_MISSING = "Select a document"
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
        DESCRIPTION = "If you select 'intangible', quantity and value are optional."

    class Incorporated:
        TITLE = "Will the product be incorporated into another product?"
        DESCRIPTION = ""
        YES = "Yes"
        NO = "No"

    class Exhibition:
        TITLE = "Select what will be exhibited for the product"
        DESCRIPTION = ""
        BACK_LINK = "Back"


class AddPreexistingGoodToApplicationForm:
    TITLE = "Add a product from your product list"

    class Table:
        DESCRIPTION = "Description"
        PART_NUMBER = "Part number"
        CONTROL_LIST_ENTRIES = "Control list entries"


class ViewGoodOnApplicationPage:
    TITLE = "Tell us about the products"
    ADD_NEW_BUTTON = "Add a new product"
    NO_CONTENT = "You haven't added any products to this application"
    NO_CONTENT_DESCRIPTION = (
        "Adding a new product to the application will also add it to your product list. "
        "This allows you to add the product to other applications."
    )


class GoodsLocationForm:
    WHERE_ARE_YOUR_GOODS_LOCATED_TITLE = "Where are the products located?"
    WHERE_ARE_YOUR_GOODS_LOCATED_DESCRIPTION = ""
    ONE_OF_MY_REGISTERED_SITES = "At one of my organisation’s sites"
    ONE_OF_MY_REGISTERED_SITES_DESCRIPTION = ""
    NOT_AT_MY_REGISTERED_SITES = "At a location that's not part of my organisation"
    NOT_AT_MY_REGISTERED_SITES_DESCRIPTION = ""
    DEPARTED_THE_COUNTRY = "The products are no longer in the UK"
    DEPARTED_THE_COUNTRY_DESCRIPTION = ""
    EXTERNAL_LOCATION_TITLE = "Do you want to add a new external location or use an existing one?"
    EXTERNAL_LOCATION_NEW_LOCATION = "Add a new external location"
    EXTERNAL_LOCATION_PREEXISTING_LOCATION = "Use an existing external location"
    ERROR = "Select an option"


class NewLocationForm:
    TITLE = "Add an external location"
    DESCRIPTION = ""

    class Name:
        TITLE = "Name"
        DESCRIPTION = ""

    class Address:
        TITLE = "Address"
        SEA_BASED_TITLE = "Enter an address or coordinates"
        DESCRIPTION = ""
        SITL_DESCRIPTION = "If you're unsure of the exact location of where your goods are, explain why."
        SEA_BASED_DESCRIPTION = "For example,\n Platform in international waters,\n 15N, 30E or 15 10.234, 30 -23.456."

    class Country:
        TITLE = "Country"


class LocationTypeForm:
    TITLE = "Select a location type"
    DESCRIPTION = ""
    CONTINUE = "Continue"
    LAND_BASED = "Land based"
    SEA_BASED = "Vessel (sea) based"


class GoodsCountriesMatrix:
    BACK = "Back to application overview"
    TITLE = "Select the destinations each product is going to"
    ERROR = "Select at least 1 destination for each product"
    THIS_IS_OPTIONAL = ""
    SELECT_ALL = "Select all"
    DESELECT_ALL = "Deselect all"
    SAVE = "Save"


class GoodsLocationPage:
    SELECT_SITES_TITLE = "Product locations"
    SELECT_SITES_BUTTON = "Add sites"


class GoodsTypeAllDestinationsPage:
    DESTINATIONS_TITLE = "Destinations"
    DESTINATIONS_DESCRIPTION_MEDIA_OIEL = "These are the destinations you can export to with a media OIEL."
    DESTINATIONS_DESCRIPTION = "These are the destinations you can export to with a "
    UK_CONTINENTAL_SHELF_DESCRIPTION = "The UK continental shelf includes parts of the North Sea, the North Atlantic, the Irish Sea and the English Channel."


class GoodsPage:
    NOTIFICATIONS = "Notifications"


class GoodsDetailSummary:
    TITLE = "Products"
    HEADING = "Product"
    SELECT_CATEGORY = "Select a product category"
    DESCRIPTION = "Description"
    PART_NUMBER = "Part number"
    CONTROLLED = "Is the product on the control list?"
    GRADED = "Does the product have a security grading?"
    MILITARY = "Is the product for military use?"
    COMPONENT = "Is the product a component?"
    DESIGNED_FOR_INFORMATION_SECURITY = "Is the product designed to employ 'information security' features?"
    DOCUMENTS = "Product documentation"
    BACK_BUTTON = "Back to check your answers page"
    PV_GRADING_YES = "Yes"
    PV_GRADING_NO = "No"
    INCORPORATED = "Incorporated"
    PURPOSE_SOFTWARE_TECHNOLOGY = "Purpose"

    class FirearmDetails:
        PRODUCT_TYPE = "Product type"
        YEAR_OF_MANUFACTURE = "Year of manufacture"
        CALIBRE = "Calibre"
        COVERED_BY_THE_FIREARMS_ACT_1968 = "Firearms Act 1968"
        IDENTIFICATION_MARKINGS = "Identification markings"


class AttachDocumentPage:
    UPLOAD_FAILURE_ERROR = "We had an issue uploading your files. Try again later."
    UPLOAD_GENERIC_ERROR = "We had an issue creating your response. Try again later."


class DeleteGoodDocumentPage:
    TITLE = "Confirm you want to delete this document"
    BACK = "Back to product"
    DOCUMENT_NAME = "Name"
    DOCUMENT_CREATED_AT = "Created at"
    DOCUMENT_CREATED_BY = "Created by"
    DOCUMENT_DESCRIPTION = "Description"
    BUTTON = "Delete document"


class F680Details:
    TITLE = "Select the types of clearance you need"
    DESCRIPTION = ""

    BACK = "Back"
    BUTTON = "Save and continue"
