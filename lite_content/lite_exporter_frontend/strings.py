from lite_content.lite_exporter_frontend import (  # noqa
    applications,  # noqa
    compliance,  # noqa
    goods,  # noqa
    goods_types,  # noqa
    roles,  # noqa
    users,  # noqa
    sites,  # noqa
    core,  # noqa
    end_users,  # noqa
    hub,  # noqa
    generic,  # noqa
    organisation,  # noqa
    declaration,  # noqa
    licences,  # noqa
    ecju_queries,  # noqa
)  # noqa

# Generic (used as defaults in forms)
BACK_TO_APPLICATION = "Back to application"
YES = "Yes"
NO = "No"
SUBMIT = "Submit"
SAVE = "Save"
CONTINUE = "Continue"
SAVE_AND_CONTINUE = "Save and continue"
CANCEL = "Cancel"
THERE_IS_A_PROBLEM = "There is a problem"

THIS_SECTION_IS = "This section is "  # The space at the end is intentional. Usage is 'This section is optional'
OPTIONAL = "Optional"
NOT_STARTED = "Not started"
IN_PROGRESS = "In progress"
DONE = "Saved"

SUBMIT_APPLICATION = "Submit application"
EDIT_APPLICATION_SUBMIT = "Submit application"
EDIT_APPLICATION_DONE = "Done"

HOME = "Home"


class Applications:
    NO_APPLICATIONS = "You haven't applied for any licences."

    class Standard:
        class Goods:
            DESCRIPTION = "List all the products that you're trying to export"
            TITLE = "List all the products that you're trying to export"

    class Edit:
        DESCRIPTION = "Depending on your answer it can take longer to reach a decision."
        TITLE = "How do you want to edit the application?"

        class Minor:
            DESCRIPTION = "This won't impact the time it takes to reach a decision."
            TITLE = "Change a site, or delete a product, third party or country"

        class Major:
            DESCRIPTION = "This will impact the time it takes to reach a decision."
            TITLE = "Something else"

    class InitialQuestions:
        EXPORT_TITLE = "Which export licence do you want to apply for?', 'Select one of the options."
        REFERENCE_TITLE = "Name and save this application so you can refer back to it when needed."


class Common:
    BACK_TO_TASK_LIST = "Back to application overview"
    SERVICE_NAME = "LITE"


class CaseNotes:
    MAX_LENGTH = "Enter up to 2,200 characters"


class EcjuQueries:
    NONE_APPLICATION = "There are no ECJU queries on this application."
    NONE_END_USER_ADVISORY = "There are no ECJU queries on this advisory."
    NONE_GOOD = "There are no queries from ECJU."


class Clc:
    class ClcForm:
        DESCRIPTION = ""
        TITLE = "Raise a control list classification (CLC) query"


class Drafts:
    DELETED = "Application deleted"
    DRAFT_NOT_FOUND = "Cannot find draft"
    NO_DRAFTS = "There are no draft applications."
    TITLE = "Drafts"


class Parties:
    class Documents:
        DELETE = "Delete"
        DOWNLOAD = "Download"
        ATTACH = "Attach document"
        VIRUS = "Document processing failed. Attach another"

    class Clearance:
        class Level:
            TITLE = "Select a proposed security grading"
            DESCRIPTION = ""

        class Descriptors:
            TITLE = "Descriptors, caveats or codewords (optional)"
            DESCRIPTION = ""


class EndUser:
    TITLE = "Select the type of end user"

    class Documents:
        ATTACH_LATER = " to upload the EUU later."
        BUTTON = "Documents"
        DELETE_DOCUMENT = "Delete"
        DESCRIPTION = "This is the document that has been uploaded for this end user."
        DOWNLOAD_DOCUMENT = "Download"
        END_USER_HAS_NO_DOCUMENTS = "There are no documents attached"
        PROCESSING = "Uploading"
        TITLE = "End user document"
        VIRUS_INFECTED = "Virus infected"

        class AttachDocuments:
            TITLE = "Attach end user documents"
            DESCRIPTION = (
                "You must attach:\n\n- a completed [end user undertaking"
                "(EUU)](https://www.gov.uk/government/publications/end-user-undertaking-euu-form) or "
                "[stockist undertaking (SU)](https://www.gov.uk/government/publications/stockist-undertaking-su-form) "
                "completed by the end user or stockist\n- a letterhead as proof of the end user or stockist\n\nIf the "
                "end user is a government organisation, instead of an EUU or SU you can attach a government purchase "
                "order. The purchase order must identify you as the applicant, any consignees, the products and "
                "respective quantities.\n\nIf any of the information provided by the end user is not in English, "
                "attach a translation.\n\nIf you haven’t received the completed undertakings from the end user, you "
                "can attach them later before you submit the application.\n\nThe files must be smaller than 50MB."
            )
            DESCRIPTION_FIELD_TITLE = "Description"
            BACK = "Back to end user summary"
            # Partial strings below
            SAVE_AND_RETURN_LATER = "save and return to the application overview"
            ATTACH_LATER = " to upload documents later."


class UltimateEndUser:
    class Documents:
        ATTACH_LATER = " to upload a document later."
        BUTTON = "Documents"
        DELETE_DOCUMENT = "Delete"
        DESCRIPTION = "This is the document that has been uploaded for this ultimate recipient."
        DOWNLOAD_DOCUMENT = "Download"
        END_USER_HAS_NO_DOCUMENTS = "There are no documents attached"
        PROCESSING = "Uploading"
        SAVE_AND_RETURN_LATER = "save and return to the application overview"
        TITLE = "Ultimate recipient document"
        VIRUS_INFECTED = "The selected file contains a virus"

        class AttachDocuments:
            TITLE = "Attach a document"
            DESCRIPTION = (
                "Do not attach a document that's above OFFICIAL-SENSITIVE.\n\nThe file must be smaller than 50MB."
            )
            DESCRIPTION_FIELD_TITLE = "Description"
            BACK = "Back to ultimate recipients"
            # Partial strings below
            SAVE_AND_RETURN_LATER = "save and return to the application overview"
            ATTACH_LATER = " to upload a document later."


class Consignee:
    TITLE = "Select the type of consignee"

    class Documents:
        ATTACH_LATER = " to upload a document later."
        BUTTON = "Documents"
        DELETE_DOCUMENT = "Delete"
        DESCRIPTION = "This is the document that has been uploaded for this consignee."
        DOWNLOAD_DOCUMENT = "Download"
        END_USER_HAS_NO_DOCUMENTS = "There are no documents attached"
        PROCESSING = "Uploading"
        SAVE_AND_RETURN_LATER = "save and return to the application overview"
        TITLE = "Consignee document"
        VIRUS_INFECTED = "The selected file contains a virus"

        class AttachDocuments:
            TITLE = "Attach a document"
            DESCRIPTION = (
                "Do not attach a document that's above OFFICIAL-SENSITIVE.\n\nThe file must be smaller than 50MB."
            )
            DESCRIPTION_FIELD_TITLE = "Description"
            BACK = "Back to consignee summary"
            # Partial strings below
            SAVE_AND_RETURN_LATER = "save and return to the application overview"
            ATTACH_LATER = " to upload a document later."


class ThirdParties:
    ADD = "Add a third party"
    DESCRIPTION = "You can add as many third parties as you want. These can be:"
    NO_RESULTS = "There are no third parties on the application"
    TITLE = "Will there be any third parties involved?"

    class Documents:
        ATTACH_LATER = " to upload a document later."
        BUTTON = "Documents"
        DELETE_DOCUMENT = "Delete"
        DESCRIPTION = "This is the document that has been uploaded for this third party."
        DOWNLOAD_DOCUMENT = "Download"
        END_USER_HAS_NO_DOCUMENTS = "There are no documents attached"
        PROCESSING = "Uploading"
        SAVE_AND_RETURN_LATER = "save and return to the application overview"
        TITLE = "Third party document"
        VIRUS_INFECTED = "The selected file contains a virus"

        class AttachDocuments:
            TITLE = "Attach a document"
            DESCRIPTION = (
                "Do not attach a document that's above OFFICIAL-SENSITIVE.\n\nThe file must be smaller than 50MB."
            )
            DESCRIPTION_FIELD_TITLE = "Description"
            BACK = "Back to third parties overview"
            # Partial strings below
            SAVE_AND_RETURN_LATER = "save and return to the application overview"
            ATTACH_LATER = " to upload a document later."


class EuaeQuery:
    CHECK_ELIGIBLE = "Check if an end user is eligible"
    CREATE_ADVISORY = "Create a new advisory"
    NO_ADVISORIES = "There are no end user advisories"
    REFRESH = "refresh this page"


class Hub:
    DESCRIPTION = "Home for exporters"
    TITLE = "Export control account"


class Licences:
    APPLY_FOR_A_LICENCE = "Apply for a licence"
    LENGTH_OF_TIME_FOR_APPLICATION = "This should take around 5 minutes"
    REFRESH = "Refresh"

    class ApplyForALicenceStart:
        TITLE = "Select the type of export licence you need"

        class LicenceQuestions:
            HINT = ""
            OPTION_1 = "Standard licence"
            OPTION_2 = "Open licence"
            RELATED_CONTENT = (
                "List of all available open general export licences"
                " https://www.gov.uk/government/collections/open-general-export-licences-ogels"
            )

    class Countries:
        DESCRIPTION = "Select all the destinations that apply."
        TITLE = "Select where the products are going"


class Misc:
    SIGNED_OUT = "You've been logged out"
    SIGN_IN = "Log in"
    SIGN_OUT = "Log out"


class Goods:
    NOTICE = "There are no products on the application."

    class AddFromOrganisation:
        BUTTON = "Add a product from your saved products list"
        TITLE = "Add a product from your product list"

    class AddGoodSummary:
        TITLE = "Product summary"
        CATEGORY = "Category"
        DESCRIPTION = "Description"
        PART_NUMBER = "Part number"
        CLC = "CLC"
        SECURITY_GRADING = "Security grading"
        MILITARY_USE = "Military use"
        COMPONENT = "Component"
        INFORMATION_SECURITY_FEATURES = "Information security features"
        PURPOSE_SOFTWARE_TECHNOLOGY = "Purpose"

        SAVE_AND_CONTINUE_BUTTON = "Continue"

        class FirearmDetails:
            PRODUCT_TYPE = "Product type"
            YEAR_OF_MANUFACTURE = "Year of manufacture"
            REPLICA_FIREARM = "Replica firearm"
            CALIBRE = "Calibre"
            COVERED_BY_THE_FIREARMS_ACT_1968 = "Firearms Act 1968"
            IDENTIFICATION_MARKINGS = "Identification markings"

    class Documents:
        BUTTON = "Documents"
        DESCRIPTION = ""
        DOWNLOAD_DOCUMENT = "Download document"
        GOOD_HAS_NO_DOCUMENTS = "There are no documents"
        PROCESSING = "Uploading"
        TITLE = "Product documents"
        VIRUS_INFECTED = "The selected file contains a virus"

        class AttachDocuments:
            BACK = "Back to product"
            BUTTON = "Add a document"
            DESCRIPTION = (
                "You need to attach a document to this product so you can include the product on an"
                " application or raise a CLC query.\n\nDo not attach a document that's OFFICIAL-SENSITIVE"
                " or above.\n\nThe file must be smaller than 50MB."
            )
            DESCRIPTION_FIELD_DETAILS = ""
            DESCRIPTION_FIELD_TITLE = "Description"
            SAVE_AND_RETURN_LATER = "save and return to the application overview"
            ATTACH_LATER = " to upload a document later."
            FILE_TOO_LARGE = "The selected file must be smaller than 50MB"
            TITLE = "Attach a document"

    class LocationQuestions:
        class Location:
            EXTERNAL_LOCATIONS = "At a location that's not part of my organisation"
            MY_SITES = "At one of my organisation's sites"
            TITLE = "Where are your products located?"

    class LocationLists:
        ADD_ADDRESS_BUTTON = "Create new address"
        FIND_ADDRESS_BUTTON = "Add existing address"
        TITLE = "Product locations"


class HelpAddress:
    ADDRESS_CITY = "London"
    EMAIL = "Email: exportcontrol.help@trade.gov.uk"
    LINE_1_ADDRESS = "3 Whitehall Place"
    POSTCODE = "SW1A 2AW"
    TELEPHONE_NUMBER = "Phone: 020 7215 4594"
    TITLE = "ECJU (Export Control Joint Unit)"


class AdditionalDocuments:
    ADD = "Add a document"
    NO_RESULTS = "No additional documents have yet been added to this application"
    TITLE = "Additional documents"
    BACK = "Back to application overview"
    NAME_COLUMN = "Document"
    DESCRIPTION_COLUMN = "Description"
    MESSAGE_COLUMN = ""
    ACTIONS_COLUMN = ""

    class Documents:
        ATTACH_LATER = ""
        BUTTON = "Documents"
        DELETE_DOCUMENT = "Delete"
        DESCRIPTION = "This is the document that has been uploaded for this draft."
        DOWNLOAD_DOCUMENT = "Download"
        VIRUS = "Document processing failed. Attach another."
        END_USER_HAS_NO_DOCUMENTS = "There are no documents attached"
        PROCESSING = "Uploading"
        SAVE_AND_RETURN_LATER = "save and return to the application overview"
        TITLE = "Additional document"
        VIRUS_INFECTED = "The selected file contains a virus"

        class AttachDocuments:
            TITLE = "Attach a supporting document"
            DESCRIPTION = (
                "Do not attach a document that's above OFFICIAL-SENSITIVE.\n\nThe file must be smaller than 50MB."
            )
            DESCRIPTION_FIELD_TITLE = "Description"
            BACK = "Back to supporting documents"
            # Partial strings below
            SAVE_AND_RETURN_LATER = "save and return to the application overview"
            ATTACH_LATER = " to upload a document later."


class Hmrc:
    class ConfirmOrg:
        BUTTON_TEXT = "Confirm and continue"
        TITLE = "Confirm that you want to make a query for this organisation"

    class QueryExplanation:
        BUTTON_TEXT = "Save and mark as done"
        TITLE = "Explain the reason behind your query"


class Exhibition:
    EXHIBITION_TITLE = "Exhibition details"
    TITLE = "Name"
    FIRST_EXHIBITION_DATE = "Exhibition start date"
    REQUIRED_BY_DATE = "Date the clearance is needed"
    DATE_DESCRIPTION = "For example, 12 11 2020"
    REASON_FOR_CLEARANCE = "The reason the clearance is needed by this date"


# TODO Remove
class Sites:
    CREATE = "Add a site"
