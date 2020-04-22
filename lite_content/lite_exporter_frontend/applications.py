class PartyForm:
    class Options:
        GOVERNMENT = "Government organisation"
        COMMERCIAL = "Commercial organisation"
        INDIVIDUAL = "An individual"
        OTHER = "Other"

    class CopyExistingForm:
        TITLE = "Do you want to reuse an existing party?"
        YES = "Yes"
        NO = "No"
        BACK_LINK = "Back to application overview"
        BUTTON = "Continue"


class PartyTypeForm:
    BACK_LINK = "Back"


class AddPartyForm:
    ERROR = "Select yes if you want to reuse an existing party"


class CopyExistingPartyPage:
    TITLE = "Select a party"
    BACK_LINK = "Back"
    HEADING = "Select a party"
    ADD_BUTTON = "Edit and add to application"
    NONE_FOUND = "There are no existing parties."
    RESULTS = " parties found"

    class Table:
        NAME_COLUMN = "Name"
        TYPE_COLUMN = "Type"
        ADDRESS_COLUMN = "Address"
        COUNTRY_COLUMN = "Country"
        WEBSITE_COLUMN = "Website"


class EndUserForm:
    TITLE = "Select the type of end user"
    BUTTON = "Continue"
    NAME_FORM_TITLE = "End user name"
    WEBSITE_FORM_TITLE = "End user website address (optional)"
    ADDRESS_FORM_TITLE = "End user address"
    SUBMIT_BUTTON = "Save and continue"


class EndUserPage:
    TITLE = "End user"
    DELETE_ERROR = "Unexpected error removing end user"


class UltimateEndUserForm:
    TITLE = "Select the type of ultimate recipient"
    BUTTON = "Continue"
    NAME_FORM_TITLE = "Ultimate recipient name"
    WEBSITE_FORM_TITLE = "Ultimate recipient website address (optional)"
    ADDRESS_FORM_TITLE = "Ultimate recipient address"
    SUBMIT_BUTTON = "Save and continue"


class UltimateEndUserPage:
    DELETE_ERROR = "Unexpected error removing ultimate recipient"


class ConsigneeForm:
    TITLE = "Select the type of consignee"
    BUTTON = "Continue"
    NAME_FORM_TITLE = "Consignee name"
    WEBSITE_FORM_TITLE = "Consignee website address (optional)"
    ADDRESS_FORM_TITLE = "Consignee address"
    SUBMIT_BUTTON = "Save and continue"


class ConsigneePage:
    TITLE = "Consignee"
    DELETE_ERROR = "Unexpected error removing consignee"


class ThirdPartyForm:
    class Options:
        AGENT = "Agent or broker"
        ADDITIONAL_END_USER = "End user"
        INTERMEDIATE_CONSIGNEE = "Intermediate consignee"
        SUBMITTER = "Authorised submitter"
        CONSULTANT = "Consultant"
        CONTACT = "Contact"
        EXPORTER = "Exporter"
        CUSTOMER = "Customer"

    ROLE_TITLE = "Select the role of the third party"
    TYPE_TITLE = "Select the type of third party"
    BUTTON = "Continue"
    NAME_FORM_TITLE = "Third party name"
    WEBSITE_FORM_TITLE = "Third party website address (optional)"
    ADDRESS_FORM_TITLE = "Third party address"
    SUBMIT_BUTTON = "Save and continue"


class ThirdPartyPage:
    DELETE_ERROR = "Unexpected error removing third party"


class DeletePartyDocumentForm:
    TITLE = "Confirm you want to delete the document"


class GeneratedDocuments:
    NO_DOCUMENTS = "There are no documents from ECJU."

    class Table:
        NAME_COLUMN = "Name"
        DATE_COLUMN = "Date"
        DOWNLOAD_LINK = "Download"


class ApplicationSummaryPage:
    ADDITIONAL_INFORMATION = "Additional information"
    CLEARANCE_LEVEL = "Security grading"
    F680_CLEARANCE_TYPES = "Clearance types"
    REFERENCE_CODE = "ECJU reference"
    REFERENCE_NAME = "Reference"
    TYPE = "Licence type"
    CASE_OFFICER = "Case officer"
    NO_ASSIGNED_CASE_OFFICER = "Not assigned"
    EXPORT_TYPE = "Export type"
    STATUS = "Status"
    LAST_UPDATED_AT = "Last updated"
    CREATED_AT = "Created"
    SUBMITTED_AT = "Submitted"
    END_USER = "End user"
    ULTIMATE_END_USERS = "Ultimate recipient"
    CONSIGNEE = "Consignee"
    THIRD_PARTIES = "Third parties"
    GOODS_LOCATIONS = "Locations"
    GOODS_DEPARTED = "Goods have left the UK"
    SUPPORTING_DOCUMENTATION = "Supporting documents"
    EXHIBITION_DETAILS = "Exhibition details"
    GOODS_CATEGORIES = "Products"
    GOODS = "Products"
    COUNTRIES = "Destinations"
    ON_BEHALF_OF = "Exporter"
    OPTIONAL_NOTE = "Notes"
    COPY_REFERENCE_CODE = "Copy ECJU reference"
    COPIED = "Copied"
    CLEARANCE = "Security grading"
    END_USE_DETAILS = "End use details"
    ROUTE_OF_GOODS = "Route of products"
    TEMPORARY_EXPORT_DETAILS = "Temporary export details"
    TRADE_CONTROL_ACTIVITY = "Type of activity"
    TRADE_CONTROL_PRODUCT_CATEGORY = "Product category"

    class Sections:
        COMPLETED_TAG = "Saved"
        IN_PROGRESS_TAG = "In progress"
        NOT_STARTED_TAG = "Not started"

    class PartiesPreviewList:
        NAME = "Name"
        TYPE = "Type"
        ROLE = "Role"
        WEBSITE = "Website"
        ADDRESS = "Address"
        COUNTRY = "Country"
        ATTACH = "Attach"
        DOCUMENT = "Document"

    class Buttons:
        EDIT_APPLICATION_BUTTON = "Edit"
        WITHDRAW_ACCESS_BUTTON = "Withdraw"
        SURRENDER_APPLICATION_BUTTON = "Surrender licence"
        COPY_APPLICATION_BUTTON = "Copy"

    class Withdraw:
        TITLE = "Confirm you want to withdraw this application"
        BACK_TEXT = "Back to application"
        YES_LABEL = "Confirm and withdraw the application"
        NO_LABEL = "Cancel"
        SUBMIT_BUTTON = "Submit"
        WITHDRAW_ERROR = "Select confirm if you want to withdraw the application"

    class Surrender:
        TITLE = "Confirm you want to surrender this application"
        BACK_TEXT = "Back to application"
        YES_LABEL = "Confirm and surrender the application"
        NO_LABEL = "Cancel"
        SUBMIT_BUTTON = "Submit"
        WITHDRAW_ERROR = "Select confirm if you want to surrender the application"

    class Tabs:
        DETAILS = "Details"
        NOTES = "Notes"
        ECJU_QUERIES = "ECJU queries"
        GENERATED_DOCUMENTS = "ECJU documents"
        ACTIVITY = "Activity"


class ApplicationsSummaryPage:
    NAME = "Name"
    REFERENCE_CODE = "ECJU reference"
    TYPE = "Type"
    EXPORT_TYPE = "Export type"
    STATUS = "Status"
    LAST_UPDATED_AT = "Last updated"
    CREATED_AT = "Created"
    SUBMITTED_AT = "Submitted"


class InitialApplicationQuestionsForms:
    class OpeningQuestion:
        TITLE = "Select what you need"
        LABEL = ""
        DESCRIPTION = ""
        BREADCRUMB = "Apply for a licence"
        HELP_WITH_CHOOSING_A_LICENCE = "What licence do I need?"
        HELP_WITH_CHOOSING_A_LICENCE_CONTENT = (
            "Read about the [different types of export control licences]"
            "(https://www.gov.uk/guidance/beginners-guide-to-export-controls#what-licence-do-i-need)."
        )

        class LicenceTypes:
            EXPORT_LICENCE_TITLE = "Export licence"
            EXPORT_LICENCE_DESCRIPTION = (
                "Select if you’re sending products from the UK to another country. You need an export licence "
                "before you provide access to technology, software or data."
            )

            TRANSHIPMENT_LICENCE_TITLE = "Transhipment licence"
            TRANSHIPMENT_LICENCE_DESCRIPTION = (
                "Select if you're shipping something from overseas through the UK on to another country."
                " If the products will be in the UK for 30 days or more, apply for an export licence."
            )

            TRADE_CONTROL_LICENCE_TITLE = "Trade control licence"
            TRADE_CONTROL_LICENCE_DESCRIPTION = (
                "Select if you’re arranging or brokering the sale or movement of controlled military products "
                "located overseas."
            )

            MOD_CLEARANCE_TITLE = "MOD clearance"
            MOD_CLEARANCE_DESCRIPTION = (
                "Select if you need to share information (an F680) or to go to an exhibition, or if you're gifting "
                "surplus products."
            )

    class ReferenceNameQuestion:
        TITLE = "Name the application"
        ENTER_A_REFERENCE_NAME_SHORT_TITLE = "Reference name"
        DESCRIPTION = "Give the application a reference name so you can refer back to it when needed."
        LABEL = ""
        BACK_TO_LICENCE_TYPE = "Back to export licence type"
        BACK_TO_MOD_CLEARANCE_TYPE = "Back to MOD clearance type"


class ExportLicenceQuestions:
    class ExportLicenceQuestion:
        TITLE = "Select the type of export licence you need"
        DESCRIPTION = ""
        BACK = "Back"
        STANDARD_LICENCE = "Standard licence"
        STANDARD_LICENCE_DESCRIPTION = "Select a standard licence for a set quantity and set value of products."
        OPEN_LICENCE = "Open licence"
        OPEN_LICENCE_DESCRIPTION = (
            "Select an open licence for multiple shipments of specific products to specific destinations. "
            "Open licences cover long term projects and repeat business."
        )

    class ExportType:
        TITLE = "Select an export type"
        DESCRIPTION = ""
        TEMPORARY = "Temporary"
        PERMANENT = "Permanent"

    class HaveYouBeenInformedQuestion:
        TITLE = "Have you received a letter or email from Border Force or HMRC informing you to apply for a licence?"
        DESCRIPTION = "You may know this as an 'end use control'."
        WHAT_WAS_THE_REFERENCE_CODE_TITLE = "Reference number"
        WHAT_WAS_THE_REFERENCE_CODE_DESCRIPTION = (
            "For example, CRE/2020/1234567. The reference number is on the letter or email."
        )


class TradeControlLicenceQuestions:
    class TradeControlLicenceQuestion:
        TITLE = "Select the type of trade control licence you need"
        DESCRIPTION = ""
        BACK = "Back"
        STANDARD_LICENCE = "Standard licence"
        STANDARD_LICENCE_DESCRIPTION = "Select a standard licence for a set quantity and set value of products."
        OPEN_LICENCE = "Open licence"
        OPEN_LICENCE_DESCRIPTION = (
            "Select an open licence for multiple shipments of specific products to specific destinations. "
            "Open licences cover long term projects and repeat business."
        )

    class ControlActivity:
        TITLE = "Select the type of trade control activity you're providing"
        DESCRIPTION = ""
        OTHER_DESCRIPTION = "Provide details"

    class ProductCategory:
        TITLE = "Select a trade control product category"
        DESCRIPTION = (
            "Find out about [trade control product categories]("
            "https://www.gov.uk/guidance/export-controls-military-goods-software-and-technology#trade"
            "-controls-and-arranging-sales-or-movements)."
        )
        CATEGORY_A_HINT = "This is a hint for Category A"
        CATEGORY_B_HINT = "This is a hint for Category B"
        CATEGORY_C_HINT = "This is a hint for Category C"


class TranshipmentQuestions:
    class TranshipmentLicenceQuestion:
        TITLE = "Select the type of transhipment licence you need"
        DESCRIPTION = ""
        BACK = "Back"
        STANDARD_LICENCE = "Standard licence"
        STANDARD_LICENCE_DESCRIPTION = "Select a standard licence for a set quantity and set value of products."
        OPEN_LICENCE = "Open licence"
        OPEN_LICENCE_DESCRIPTION = (
            "Select an open licence for multiple shipments of specific products to specific destinations. "
            "Open licences cover long term projects and repeat business."
        )

    class ExportType:
        TITLE = "Select an export type"
        DESCRIPTION = ""
        TEMPORARY = "Temporary"
        PERMANENT = "Permanent"

    class HaveYouBeenInformedQuestion:
        TITLE = "Have you received a letter or email from Border Force or HMRC informing you to apply for a licence?"
        DESCRIPTION = "You may know this as an 'end use control'."
        WHAT_WAS_THE_REFERENCE_CODE_TITLE = "Reference number"
        WHAT_WAS_THE_REFERENCE_CODE_DESCRIPTION = "The reference number is on the official letter or email."


class MODQuestions:
    class ConfirmationStatement:
        TITLE = "MOD Form 680 confirmation statement"
        DESCRIPTION = (
            "UK companies need MOD Form 680 (F680) approval to release information or equipment classified "
            "OFFICIAL-SENSITIVE and above to foreign entities.\n"
            "Some materials classified OFFICIAL need F680 approval, but only if there’s information or equipment "
            "connected with the release that holds a higher classification. An F680 is not required where both the "
            "equipment and information intended for release is classified OFFICIAL. This process also applies to MOD "
            "agencies and other parts of the MOD.\n"
            "To get this clearance, you must complete this form, the main purpose of which is to help prevent "
            "unauthorised disclosure of classified information and equipment.\n"
            "Where any activities detailed in the application involve the export or transfer of controlled "
            "technology to an overseas end user, the export or transfer is subject to UK export controls. You need "
            "to apply for an export licence in addition to obtaining F680 clearance.\n"
            "F680 applications are limited to a maximum of 20 combined end users and destinations. However, there’s "
            "the facility to copy applications. Further information can be found in the guidance notes.\n"
            "No information above OFFICIAL-SENSITIVE should be entered or uploaded using this application"
        )

    class WhatAreYouApplyingFor:
        TITLE = "Select the type of MOD clearance you need"
        DESCRIPTION = ""
        BACK = "Back to application type"

        PERMISSION_TITLE = "MOD Form 680"
        PERMISSION_DESCRIPTION = (
            "Select an F680 approval if you need to release equipment or information with a classification of "
            "OFFICIAL-SENSITIVE or above to any foreign entity overseas or demonstrate it to them in the UK."
        )

        EXHIBITION_CLEARANCE_TITLE = "Exhibition clearance"
        EXHIBITION_CLEARANCE_DESCRIPTION = (
            "Select if you need clearance to exhibit defence related products that aren't MOD funded."
        )

        GIFTING_CLEARANCE_TITLE = "Gifting clearance"
        GIFTING_CLEARANCE_DESCRIPTION = "Select to request the gifting of surplus MOD property."


class DestinationForm:
    TITLE = "Select where the products are going"
    DESCRIPTION = ""


class StandardApplicationTaskList:
    ENTER_A_REFERENCE_NAME_SHORT_TITLE = "Reference"
    NEW_TITLE = "Standard Individual Export Licence application"
    EDIT_TITLE = "Edit the application"
    END_USE_CONTROL = "Informed to apply"
    GOODS_CATEGORIES = "Categories"
    GOODS = "Products"
    GOODS_LOCATION = "Locations"
    END_USER = "End user"
    ULTIMATE_END_USERS = "Ultimate recipients"
    CONSIGNEE = "Consignee"
    SUPPORTING_DOCUMENTS = "Supporting documents"
    THIRD_PARTIES = "Third parties"
    END_USE_DETAILS = "End use details"
    TEMPORARY_EXPORT_DETAILS = "Temporary export details"
    NOTES = "Notes"


class OpenApplicationTaskList:
    ENTER_A_REFERENCE_NAME_SHORT_TITLE = "Reference"
    NEW_TITLE = "Open Individual Export Licence application"
    EDIT_TITLE = "Edit the application"
    GOODS = "Products"
    GOODS_LOCATION = "Locations"
    GOODS_DESTINATION = "Destinations"
    COUNTRIES_WHERE_EACH_GOOD_IS_GOING = "Product destinations"
    SUPPORTING_DOCUMENTS = "Supporting documents"
    END_USE_DETAILS = "End use details"
    TEMPORARY_EXPORT_DETAILS = "Temporary export details"
    NOTES = "Notes"


class HMRCApplicationTaskList:
    ENTER_A_REFERENCE_NAME_SHORT_TITLE = "Reference"
    GOODS = "Products"
    GOODS_LOCATION = "Locations"
    END_USER = "End user"
    ULTIMATE_END_USERS = "Ultimate recipients"
    THIRD_PARTIES = "Third parties"
    CONSIGNEE = "Consignee"
    SUPPORTING_DOCUMENTS = "Supporting documents"
    REASON_FOR_QUERY = "Notes"
    CHECK_YOUR_ANSWERS = "Check your answers"


class ExhibitionClearanceTaskList:
    ENTER_A_REFERENCE_NAME_SHORT_TITLE = "Reference"
    DETAILS = "Exhibition details"
    NEW_TITLE = "Exhibition Clearance application"
    EDIT_TITLE = "Edit the application"
    GOODS = "Products"
    GOODS_LOCATION = "Locations"
    END_USER = "End user"
    ULTIMATE_END_USERS = "Ultimate recipients"
    CONSIGNEE = "Consignee"
    SUPPORTING_DOCUMENTS = "Supporting documents"
    THIRD_PARTIES = "Third parties"
    NOTES = "Notes"


class GiftingClearanceTaskList:
    ENTER_A_REFERENCE_NAME_SHORT_TITLE = "Reference"
    NEW_TITLE = "Gifting Clearance application"
    EDIT_TITLE = "Edit the application"
    GOODS = "Products"
    GOODS_LOCATION = "Locations"
    END_USER = "End user"
    SUPPORTING_DOCUMENTS = "Supporting documents"
    THIRD_PARTIES = "Third parties"
    NOTES = "Notes"


class F680ClearanceTaskList:
    ENTER_A_REFERENCE_NAME_SHORT_TITLE = "Reference"
    SAVE_AND_RETURN = "Save and return to application overview"
    NOTICE_TITLE = ""
    NOTICE_TEXT = ""
    NEW_TITLE = "MOD Form 680 application"
    EDIT_TITLE = "Edit the application"
    F680_DETAILS = "Clearance types"
    ADDITIONAL_INFORMATION = "Additional information"
    GOODS = "Products"
    GOODS_LOCATION = "Locations"
    END_USER = "End user"
    SUPPORTING_DOCUMENTS = "Supporting documents"
    THIRD_PARTIES = "Third parties"
    NOTES = "Notes"
    CLEARANCE = "Security grading"
    END_USE_DETAILS = "End use details"


class F680Questions:
    CAPTION = "F680 Additional Information"

    class Expedited:
        TITLE = "Do you need the F680 clearance in less than 30 days due to exceptional circumstances?"
        DATE = "Date you need the licence"

    class ForeignTechnology:
        TITLE = "Is there any foreign technology or information involved in the release?"
        DESCRIPTION = "Include written release agreements or clearances from the originating nations"
        PROVIDE_DETAILS = "Provide details"

    class LocallyManufactured:
        TITLE = "Is local assembly or manufacture required?"
        PROVIDE_DETAILS = "Provide details"

    class MtcrType:
        TITLE = "Do you believe the products are rated under the Missile Technology Control Regime (MTCR)"

        class Categories:
            ONE = "Yes, Category 1"
            TWO = "Yes, Category 2"
            NO = "No"
            I_DONT_KNOW = "I don't know"

    class EWRequirement:
        TITLE = "Is there is a requirement to release UK MOD owned electronic warfare (EW) data or information in support of this export"
        ATTACHMENT = (
            "You need to complete part A of the MOD EW Data Release Capture Form "
            "and attach it to the application in the supporting documents section."
        )

    class UKServiceEquipment:
        TITLE = "Is the equipment or a version of it due to enter service with the UK armed forces?"
        TYPE = "Select how the product is funded"
        PROVIDE_DETAILS_OPTIONAL = "Provide details (optional)"

        class Types:
            MOD_FUNDED = "MOD funded"
            MOD_VENTURE_FUNDED = "Part MOD funded / part private venture"
            PRIVATE_VENTURE = "Private venture"

    class ProspectValue:
        TITLE = "What is the total value of prospect?"


class EditApplicationPage:
    BACK = "Back to applications"
    DRAFT_DELETE_LINK = "Delete draft"
    SUBMIT = "Submit application"
    DONE = "Saved"
    ERRORS = "There is a problem"
    MINOR_EDIT = "Changes made to this application won't impact its processing time."
    MAJOR_EDIT = "This application won't be processed until it's submitted."

    class InitialTaskSection:
        TITLE = "Prepare application"
        EDITING = "Basic details"

    class MainTaskSection:
        TITLE = "Complete application"
        EDITING = "More information"


class EditOpenApplicationPage:
    BACK_TO_APPLICATIONS = "Back to applications"
    DRAFT_DELETE_LINK = "Delete draft"
    SUBMIT = "Submit application"


class DeleteApplicationPage:
    BUTTON = "Delete draft"
    TITLE = "Confirm you want to delete this draft"
    BACK_TEXT = "Back to applications"
    YES_LABEL = "Confirm and delete the draft"
    NO_LABEL = "Cancel"
    SUBMIT_BUTTON = "Submit"
    DELETE_ERROR = "Select confirm if you want to delete the draft"


class ApplicationNotesPage:
    TITLE = "Notes"
    DESCRIPTION = ""
    BACK_LINK = "Back to application overview"


class AttachDocumentPage:
    UPLOAD_FAILURE_ERROR = "We had an issue uploading your files. Try again later."
    UPLOAD_GENERIC_ERROR = "We had an issue creating your response. Try again later."
    DOWNLOAD_GENERIC_ERROR = "We had an issue downloading your file. Try again later."


class DeleteDocument:
    DOCUMENT_DELETE_GENERIC_ERROR = "We had an issue deleting your file. Try again later."


class ApplicationSuccessPage:
    TITLE = "Application submitted"
    SECONDARY_TITLE = "ECJU reference: "
    DESCRIPTION = ""
    WHAT_HAPPENS_NEXT = ["You'll receive an email from ECJU when the check is finished."]
    VIEW_APPLICATIONS = "View your list of applications"
    APPLY_AGAIN = "Apply for another licence or clearance"
    RETURN_TO_DASHBOARD = "Return to your export control account dashboard"


class ApplicationsList:
    TITLE = "Applications"
    RAISE_A_QUERY_BUTTON = "Raise a query"
    APPLY_FOR_A_LICENCE_BUTTON = "Apply for a licence"
    REFRESH_BUTTON = "Refresh"
    IN_PROGRESS_TAB = "Submitted"
    DRAFTS_TAB = "Drafts"
    NOTIFICATIONS_SUFFIX = "notifications"
    NO_CONTENT_NOTICE = "There are no applications in progress."
    NO_DRAFTS_CONTENT_NOTICE = "There are no draft applications."
    COPY_HEADER = "Copy"
    COPY_LINK = "Copy"


class ApplicationPage:
    BACK = "Back to applications"
    NO_INFORMATION_PROVIDED = "No information added to this section."


class ThirdPartiesPage:
    TITLE = "Third parties"
    ADD = "Add a third party"
    NO_RESULTS = "There are no third parties on this application."

    class Variables:
        NAME = "Name"
        TYPE = "Type"
        CLEARANCE_LEVEL = "Clearance"
        DESCRIPTORS = "Descriptors"
        ROLE = "Role"
        WEBSITE = "Website"
        ADDRESS = "Address"
        COUNTRY = "Country"
        DOCUMENT = "Document"


class ClearanceLevel:
    TITLE = "Select a proposed security grading for the F680 clearance"
    DESCRIPTION = ""


class UltimateEndUsersPage:
    TITLE = "Ultimate recipients"
    ADD = "Add a third party"
    NO_RESULTS = "There are no third parties on this application"
    BACK = "Back to application overview"
    HELP = "What is an ultimate recipient?"
    DESCRIPTION = (
        "An ultimate recipient is a party that uses the product or the higher level system into which the product is"
        " installed or incorporated. The end user and ultimate recipient may be different parties."
    )
    NOTICE = "There are no ultimate recipients on this application."
    MISSING_DOCS_NOTICE = "You need to attach a document to some ultimate recipients"
    ADD_BUTTON = "Add an ultimate recipient"

    class Document:
        DOWNLOAD = "Download"
        DELETE = "Delete"
        PROCESSING = "Processing"
        ATTACH = "Attach"
        REMOVE = "Remove"

    class Variables:
        NAME = "Name"
        TYPE = "Type"
        ROLE = "Role"
        WEBSITE = "Website"
        ADDRESS = "Address"
        COUNTRY = "Country"
        DOCUMENT = "Document"


class Activity:
    NO_ACTIVITY = "There's been no activity."


class CaseNotes:
    TITLE = "Add a note"
    NOTICE = "Enter up to 2200 characters."
    POST_NOTE = "Post note"
    CANCEL = "Cancel"
    ADDED_A_NOTE_SUFFIX = "added a note:"
    NO_NOTES = "There are no notes."


class GoodsCategories:
    TITLE = "Do any products on the application fall into any of these categories?"
    DESCRIPTION = ""
    ERROR = "You can't change product categories while doing a minor edit"


class AdditionalInformation:
    ELECTRONIC_WARFARE_REQUIREMENT = "Has electronic warfare requirement"
    EXPEDITED = "Is expedited"
    EXPEDITED_DATE = "Expedited date"
    FOREIGN_TECHNOLOGY = "Has foreign technology"
    FOREIGN_TECHNOLOGY_DESCRIPTION = "Foreign technology description"
    FOREIGN_TECHNOLOGY_TYPE = "Foreign technology type"
    LOCALLY_MANUFACTURED = "Is locally manufactured"
    LOCALLY_MANUFACTURED_DESCRIPTION = "Locally manufactured description"
    MTCR_TYPE = "MTCR type"
    UK_SERVICE_EQUIPMENT = "Has UK service equipment"
    UK_SERVICE_EQUIPMENT_DESCRIPTION = "UK service equipment description"
    UK_SERVICE_EQUIPMENT_TYPE = "UK service equipment type"
    VALUE = "Value"


class EndUseDetails:
    REFERENCE = "Reference"
    REFERENCE_ECJU_LETTER = "This reference is on the ECJU letter"
    NOTICE = "Enter up to 2,200 characters"
    PROVIDE_DETAILS = "Provide details"
    EU_MILITARY_PROVIDE_DETAILS = "If no, provide details (optional)"

    INTENDED_END_USE = "Provide details of the intended end use of the products"
    INFORMED_TO_APPLY = (
        "Have you received a letter from ECJU informing you that the products "
        "require a licence to export or are controlled under the military end use controls?"
    )
    INFORMED_WMD = (
        "Have you been informed by ECJU that the products are or may be intended, wholly or in part, "
        "for use in chemical, biological or nuclear weapons, "
        "or any purpose connected with missiles capable of delivering these weapons?"
    )
    SUSPECTED_WMD = (
        "Do you know or suspect that the products might be used, wholly or in part, in connection with "
        "chemical, biological or nuclear weapons, "
        "or any purpose connected with missiles capable of delivering these weapons?"
    )
    EU_MILITARY = (
        "Have you received European military products under a transfer licence from a European Union member state "
        "that have export limitations attached to them?"
    )
    IS_COMPLIANT_LIMITATIONS_EU = (
        "Have you complied with the terms of the export limitations attached to them? "
        "Or where appropriate, have you obtained the required consent from the originating "
        "EU member state?"
    )

    class EndUseDetailsSummaryList:
        TITLE = "End use summary list"
        INTENDED_END_USE = "Intended end use of the products"
        INFORMED_TO_APPLY = "Informed by ECJU to apply for a licence"
        INFORMED_WMD = "Informed by ECJU that products may be used in WMD"
        SUSPECTED_WMD = "You suspect products may be used in WMD"
        EU_MILITARY = "Products received under a transfer licence"
        COMPLIANT_LIMITATIONS_EU = "Compliant with terms of export limitations or obtained consent"

    class CheckYourAnswers:
        INTENDED_END_USE_TITLE = "Intended end use"
        INFORMED_TO_APPLY_TITLE = "Informed to apply"
        INFORMED_WMD_TITLE = "Informed WMD"
        SUSPECTED_WMD_TITLE = "Suspect WMD"
        EU_MILITARY_TITLE = "EU transfer licence"
        COMPLIANT_LIMITATIONS_EU_TITLE = "Complied to terms"


class TemporaryExportDetails:
    TEMPORARY_EXPORT_DETAILS_CAPTION = "Temporary export details"
    PROPOSED_DATE_HINT = "For example, 12 11 2020"

    TEMPORARY_EXPORT_DETAILS = "Provide details of why the export is temporary"
    PRODUCTS_UNDER_DIRECT_CONTROL = "Will the products remain under your direct control while overseas?"
    PRODUCTS_UNDER_DIRECT_CONTROL_DETAILS = (
        "Provide details of who will be in control of the products while overseas and their relationship to you"
    )
    PROPOSED_RETURN_DATE = "Proposed date the products will return to the UK"

    class SummaryList:
        TITLE = "Temporary export details summary list"
        TEMPORARY_EXPORT_DETAILS = "Temporary export details"
        PRODUCTS_UNDER_DIRECT_CONTROL = "Products remaining under your direct control"
        PROPOSED_RETURN_DATE = "Date products returning to the UK"

    class CheckYourAnswers:
        TEMPORARY_EXPORT_DETAILS = "Temporary export details"
        PRODUCTS_UNDER_DIRECT_CONTROL = "Products remaining under your direct control"
        PROPOSED_RETURN_DATE = "Date products returning to the UK"


class HMRCQuery:
    class InitialQuestions:
        REFERENCE_NAME_TITLE = "Name the query"
        REFERENCE_NAME_DESCRIPTION = "Give the query a reference name so you can refer back to it when needed."
        REFERENCE_NAME_BUTTON = "Continue"


class RouteOfGoods:
    TITLE = "Are the products being shipped on an air waybill or bill of lading?"
    NO_ANSWER_DESCRIPTION = "Provide details of the route of the products"
    SAVE_BUTTON = "Save"
