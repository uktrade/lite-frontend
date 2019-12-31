from conf.settings import env
from lite_content.lite_exporter_frontend import applications, goods, roles, users, sites, core, end_users, hub  # noqa

# Generic (used as defaults in forms)
BACK_TO_APPLICATION = "Back to application"
YES = "Yes"
NO = "No"
SUBMIT = "Submit"
SAVE = "Save"
CONTINUE = "Continue"
SAVE_AND_CONTINUE = "Save and continue"
CANCEL = "Cancel"
POST_NOTE = "Post note"

THIS_SECTION_IS = "This section is "  # The space at the end is intentional. Usage is 'This section is optional'
OPTIONAL = "Optional"
NOT_STARTED = "Not started"
IN_PROGRESS = "In progress"
DONE = "Completed"
VIEW = "View"

SUBMIT_APPLICATION = "Submit application"
EDIT_APPLICATION_SUBMIT = "Submit application"
EDIT_APPLICATION_DONE = "Done"

HOME = "Home"

# Constants
PERMISSION_FINDER_LINK = "[control list](" + env("PERMISSIONS_FINDER_URL") + ")"


class Address:
    ADDRESS_LINE_1 = "Building and street"
    ADDRESS_LINE_2 = ""
    TOWN = "Town or city"
    COUNTY = "County/State"
    POSTAL_CODE = "Postal Code"
    COUNTRY = "Country"


class Applications:
    NO_APPLICATIONS = "You haven't applied for any licences yet."

    class Standard:
        class Goods:
            DESCRIPTION = "List all the products that you're trying to export"
            TITLE = "List all the products that you're trying to export"

    class Edit:
        DESCRIPTION = "Depending on your answer it can take longer to reach a decision."
        TITLE = "How do you want to change your application?"

        class Minor:
            DESCRIPTION = "This won't impact the time it takes to reach a decision."
            TITLE = "Change a site, or delete a product, third party or country"

        class Major:
            DESCRIPTION = "This will impact the time it takes to reach a decision."
            TITLE = "Something else"

    class InitialQuestions:
        EXPORT_TITLE = "Which export licence do you want to apply for?', 'Select one of the options."
        REFERENCE_TITLE = "Name and save this application so you can refer back to it when needed."


class Authentication:
    class UserDoesNotExist:
        DESCRIPTION = "You are not registered to use this system"
        TITLE = "User not found"


class Common:
    BACK_TO_TASK_LIST = "Back to application overview"
    SERVICE_NAME = "LITE"


class CaseNotes:
    MAX_LENGTH = "Enter up to 2,200 characters"


class EcjuQueries:
    NONE_APPLICATION = "There haven't been any queries on this application."
    NONE_END_USER_ADVISORY = "There haven't been any queries on this advisory."
    NONE_GOOD = "There haven't been any queries on this product."


class Clc:
    class ClcForm:
        DESCRIPTION = "By submitting you are creating a CLC query that cannot be altered"
        TITLE = "Create a CLC query"


class Drafts:
    DELETED = "Application deleted"
    DRAFT_NOT_FOUND = "Cannot find draft"
    NO_DRAFTS = "You don't have any draft applications."
    TITLE = "Drafts"


class EndUser:
    TITLE = "Select the type of end user"

    class Documents:
        ATTACH_LATER = "to upload a document later."
        BUTTON = "Documents"
        DELETE_DOCUMENT = "Delete"
        DESCRIPTION = "This is the document that has been uploaded for this end user."
        DOWNLOAD_DOCUMENT = "Download"
        END_USER_HAS_NO_DOCUMENTS = "This end user has no documents attached"
        PROCESSING = "Processing"
        SAVE_END_USER = "Save and return to the application overview "
        TITLE = "End user document"
        VIRUS_INFECTED = "Virus infected"

        class AttachDocuments:
            BACK_TO_APPLICATION_OVERVIEW = "Back to application overview"
            BUTTON = "Attach document"
            DELETE_ERROR = "We had an issue deleting your files. Try again later."
            DESCRIPTION = (
                "Do not attach a document that's OFFICIAL-SENSITIVE or above.\n\nThe file must be smaller"
                " than 100MB."
            )
            DESCRIPTION_FIELD_DETAILS = "optional"
            DESCRIPTION_FIELD_TITLE = "Description"
            DOWNLOAD_ERROR = "We had an issue downloading your file. Try again later."
            FILE_TOO_LARGE = "The file you tried to upload is too large."
            TITLE = "Attach a document"
            UPLOAD_ERROR = "We had an issue uploading your files. Try again later."


class UltimateEndUser:
    OVERVIEW_DESCRIPTION = (
        "The entity that uses the product or the higher level system into which the products are"
        " installed or incorporated. The end user and ultimate recipient may be different entities."
    )

    class Documents:
        ATTACH_LATER = "to upload a document later."
        BUTTON = "Documents"
        DELETE_DOCUMENT = "Delete"
        DESCRIPTION = "This is the document that has been uploaded for this ultimate recipient."
        DOWNLOAD_DOCUMENT = "Download"
        END_USER_HAS_NO_DOCUMENTS = "This ultimate recipient has no documents attached"
        PROCESSING = "Processing"
        SAVE_END_USER = "Save and return to the application overview "
        TITLE = "Ultimate recipient document"
        VIRUS_INFECTED = "Virus infected"

        class AttachDocuments:
            BACK_TO_APPLICATION_OVERVIEW = "Back to ultimate recipients"
            BUTTON = "Attach Document"
            DELETE_ERROR = "We had an issue deleting your files. Try again later."
            DESCRIPTION = (
                "Do not attach a document that's OFFICIAL-SENSITIVE or above.\n\nThe file must be smaller"
                " than 100MB."
            )
            DESCRIPTION_FIELD_DETAILS = ""
            DESCRIPTION_FIELD_TITLE = "Description (optional)"
            DOWNLOAD_ERROR = "We had an issue downloading your file. Try again later."
            FILE_TOO_LARGE = "The file you tried to upload is too large."
            TITLE = "Attach a document"
            UPLOAD_ERROR = "We had an issue uploading your files. Try again later."


class Consignee:
    TITLE = "Select the type of consignee"

    class Documents:
        ATTACH_LATER = "to upload a document later."
        BUTTON = "Documents"
        DELETE_DOCUMENT = "Delete"
        DESCRIPTION = "This is the document that has been uploaded for this consignee."
        DOWNLOAD_DOCUMENT = "Download"
        END_USER_HAS_NO_DOCUMENTS = "This consignee has no documents attached"
        PROCESSING = "Processing"
        SAVE_END_USER = "Save and return to the application overview "
        TITLE = "Consignee document"
        VIRUS_INFECTED = "Virus infected"

        class AttachDocuments:
            BACK_TO_APPLICATION_OVERVIEW = "Back to application overview"
            BUTTON = "Attach Document"
            DELETE_ERROR = "We had an issue deleting your files. Try again later."
            DESCRIPTION = (
                "Do not attach a document that's OFFICIAL-SENSITIVE or above.\n\nThe file must be smaller"
                " than 100MB."
            )
            DESCRIPTION_FIELD_DETAILS = ""
            DESCRIPTION_FIELD_TITLE = "Description (optional)"
            DOWNLOAD_ERROR = "We had an issue downloading your file. Try again later."
            FILE_TOO_LARGE = "The file you tried to upload is too large."
            TITLE = "Attach a document"
            UPLOAD_ERROR = "We had an issue uploading your files. Try again later."


class ThirdParties:
    ADD = "Add a third party"
    DESCRIPTION = "You can add as many third parties as you want. These can be:"
    NO_RESULTS = "You haven't added any third parties to your application"
    TITLE = "Will there be any third parties involved?"

    class Documents:
        ATTACH_LATER = "to upload a document later."
        BUTTON = "Documents"
        DELETE_DOCUMENT = "Delete"
        DESCRIPTION = "This is the document that has been uploaded for this third party."
        DOWNLOAD_DOCUMENT = "Download"
        END_USER_HAS_NO_DOCUMENTS = "This third party has no documents attached"
        PROCESSING = "Processing"
        SAVE_END_USER = "Save and return to the application overview "
        TITLE = "Third party document"
        VIRUS_INFECTED = "Virus infected"

        class AttachDocuments:
            BACK_TO_APPLICATION_OVERVIEW = "Back to third parties overview"
            BUTTON = "Attach document"
            DELETE_ERROR = "We had an issue deleting your files. Try again later."
            DESCRIPTION = (
                "Do not attach a document that's OFFICIAL-SENSITIVE or above.\n\nThe file must be smaller"
                " than 100MB."
            )
            DESCRIPTION_FIELD_DETAILS = ""
            DESCRIPTION_FIELD_TITLE = "Description (optional)"
            DOWNLOAD_ERROR = "We had an issue downloading your file. Try again later."
            FILE_TOO_LARGE = "The file you tried to upload is too large."
            TITLE = "Attach a document"
            UPLOAD_ERROR = "We had an issue uploading your files. Try again later."


class EuaeQuery:
    CHECK_ELIGIBLE = "Check if an end user is eligible"
    CREATE_ADVISORY = "Create a new advisory"
    NO_ADVISORIES = "You haven't applied for any end user advisories"
    REFRESH = "refresh this page"


class Hub:
    DESCRIPTION = "Home for exporters"
    TITLE = "Exporter hub"


class Licences:
    APPLY_FOR_A_LICENCE = "Apply for a licence"
    LENGTH_OF_TIME_FOR_APPLICATION = "This should take around 5 minutes"
    REFRESH = "Refresh"

    class ApplyForALicenceStart:
        TITLE = "Select the type of licence you need"

        class LicenceQuestions:
            HINT = ""
            OPTION_1 = "Standard licence"
            OPTION_2 = "Open licence"
            RELATED_CONTENT = (
                "List of all available open general export licences"
                " https://www.gov.uk/government/collections/open-general-export-licences-ogels"
            )

    class Countries:
        DESCRIPTION = "Select all countries that apply."
        TITLE = "Where are your products going?"


class Misc:
    SIGNED_OUT = "You've been logged out"
    SIGN_IN = "Log in"
    SIGN_OUT = "Log out"


class Goods:
    NOTICE = "You haven't added any products to your application."

    class AddFromOrganisation:
        BUTTON = "Add an existing product"
        TITLE = "Add a product from your product database"

    class Documents:
        BUTTON = "Documents"
        DESCRIPTION = "These are all the documents that have been attached to this product."
        DOWNLOAD_DOCUMENT = "Download document"
        GOOD_HAS_NO_DOCUMENTS = "This product has no documents attached"
        PROCESSING = "Processing"
        TITLE = "Product documents"
        VIRUS_INFECTED = "Virus infected"

        class AttachDocuments:
            BACK_TO_GOOD = "Back to product"
            BUTTON = "Add a document"
            DESCRIPTION = (
                "You need to attach a document to this product so you can include the product on an"
                " application or raise a CLC query.\n\nDo not attach a document that's OFFICIAL-SENSITIVE"
                " or above.\n\nThe file must be smaller than 100MB."
            )
            DESCRIPTION_FIELD_DETAILS = ""
            DESCRIPTION_FIELD_TITLE = "Description (optional)"
            FILE_TOO_LARGE = "The file you tried to upload is too large."
            TITLE = "Attach a document"

    class LocationQuestions:
        class Location:
            EXTERNAL_LOCATIONS = "At a location that's not part of my organisation"
            MY_SITES = "At one of my organisation's sites"
            TITLE = "Where are your products located?"

    class LocationLists:
        ADD_ADDRESS_BUTTON = "Add new address"
        FIND_ADDRESS_BUTTON = "Find existing address"
        TITLE = "Product location address"


class GoodTypes:
    class Overview:
        NO_GOOD_TYPES = "Add product descriptions to your application"
        TITLE = "Describe your products"

    class OverviewGoodTypes:
        ADD_GOOD_TYPE_BUTTON = "Add a product"
        NO_GOOD_TYPES = "There are no products to show. To add a product use the Add a product button"
        TITLE = "Your products"

    class OverviewAddGoodTypes:
        DESCRIPTION = "Give us a short description of your products."
        Q1 = "Is your product controlled?"
        Q1_1 = "Control list classification"
        Q1_2 = "For example, ML1a."
        Q2 = "Is your product intended to be incorporated into an end product?"
        TITLE = "Add a description"


class HelpAddress:
    ADDRESS_CITY = "London"
    EMAIL = "Email: exportcontrol.help@trade.gov.uk"
    LINE_1_ADDRESS = "3 Whitehall Place"
    POSTCODE = "SW1A 2AW"
    TELEPHONE_NUMBER = "Phone: 020 7215 4594"
    TITLE = "ECJU (Export Control Joint Unit)"


class Sites:
    CREATE = "Add a site"
    DESCRIPTION = "Sites are locations where your organisation conducts business."
    TITLE = "Sites"


class GoodsTypes:
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


class AdditionalDocuments:
    ADD = "Add a document"
    NO_RESULTS = "You haven't added any additional documents to your application"
    TITLE = "Supporting documents"

    class Documents:
        ATTACH_LATER = ""
        BUTTON = "Documents"
        DELETE_DOCUMENT = "Delete"
        DESCRIPTION = "This is the document that has been uploaded for this draft."
        DOWNLOAD_DOCUMENT = "Download"
        END_USER_HAS_NO_DOCUMENTS = "This consignee has no documents attached"
        PROCESSING = "Processing"
        SAVE_END_USER = "save your progress and return to your application later"
        TITLE = "Additional document"
        VIRUS_INFECTED = "Virus infected"

        class AttachDocuments:
            BACK_TO_APPLICATION_OVERVIEW = "Back to additional documents overview"
            BUTTON = "Attach document"
            DELETE_ERROR = "We had an issue deleting your files. Try again later."
            DESCRIPTION = (
                "Do not attach a document that's OFFICIAL-SENSITIVE or above.\n\nThe file must be smaller"
                " than 100MB."
            )
            DESCRIPTION_FIELD_DETAILS = ""
            DESCRIPTION_FIELD_TITLE = "Description (optional)"
            DOWNLOAD_ERROR = "We had an issue downloading your file. Try again later."
            FILE_TOO_LARGE = "The file you tried to upload is too large."
            TITLE = "Attach a document"
            UPLOAD_ERROR = "We had an issue uploading your files. Try again later."


class Hmrc:
    class ConfirmOrg:
        BUTTON_TEXT = "Confirm and continue"
        TITLE = "Confirm that you want to make a query for this organisation"

    class QueryExplanation:
        BUTTON_TEXT = "Save and mark as done"
        TITLE = "Explain the reason behind your query"
