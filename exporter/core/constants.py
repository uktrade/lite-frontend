from core.constants import GoodsTypeCategory
from lite_content.lite_exporter_frontend import applications


DATE_FORMAT = "%Y-%m-%d"
PAGE_DATE_FORMAT = "%d %B %Y"
TIMEZONE = "Europe/London"

MAX_OPEN_LICENCE_RETURNS_FILE_SIZE = 1000000  # 1 MB

# Applications constants
STANDARD = "standard"
OPEN = "open"
HMRC = "hmrc"
EXHIBITION = "exhibition_clearance"
GIFTING = "gifting_clearance"
F680 = "f680_clearance"


class CaseTypes:
    OIEL = "oiel"
    OGEL = "ogel"
    OGTL = "ogtl"
    OGTCL = "ogtcl"
    OICL = "oicl"
    SIEL = "siel"
    SICL = "sicl"
    SITL = "sitl"
    F680 = "f680"
    EXHC = "exhc"
    GIFT = "gift"
    CRE = "cre"
    GQY = "gqy"
    EUA = "eua"


# Case type task list sections
CASE_SECTIONS = {
    "HMRC": HMRC,
    "F680": F680,
    "HAS_F680_CLEARANCE_TYPES": F680,
    "HAS_CLEARANCE_LEVEL": [F680],
    "HAS_F680_ADDITIONAL_INFORMATION": [F680],
    "EXHIBITION": EXHIBITION,
    "HAS_LICENCE_TYPE": [STANDARD, OPEN],
    "HAS_TOLD_BY_OFFICIAL": [STANDARD],
    "HAS_GOODS": [STANDARD, EXHIBITION, GIFTING, F680],
    "HAS_GOODS_TYPES": [OPEN, HMRC],
    "HAS_LOCATIONS": [OPEN, HMRC, EXHIBITION],
    "HAS_PRODUCT_JOURNEY": [STANDARD],
    "HAS_COUNTRIES": OPEN,
    "HAS_END_USER": [STANDARD, F680, GIFTING, CaseTypes.OICL],
    "HAS_END_USER_OPEN_APP": [GoodsTypeCategory.MILITARY, GoodsTypeCategory.UK_CONTINENTAL_SHELF],
    "HAS_ULTIMATE_END_USERS": [STANDARD, HMRC, OPEN],
    "HAS_CONSIGNEE": [STANDARD, HMRC],
    "HAS_THIRD_PARTIES": [STANDARD, F680, GIFTING],
    "HAS_OPTIONAL_NOTE": [HMRC],
    "HAS_NOTES": [STANDARD, OPEN, EXHIBITION, F680, GIFTING],
    "HAS_END_USE_DETAILS": [STANDARD, OPEN, F680],
    "END_USERS_OPTIONAL": [F680, OPEN],
}

PERMANENT = "permanent"
TEMPORARY = "temporary"

APPLICANT_EDITING = "applicant_editing"

NOT_STARTED = "not_started"
IN_PROGRESS = "in_progress"
DONE = "done"

SUPER_USER_ROLE_ID = "00000000-0000-0000-0000-000000000003"
DEFAULT_USER_ROLE_ID = "00000000-0000-0000-0000-000000000004"

# CLC
UNSURE = "unsure"

SAVE_BUTTON = "Save"
CONTINUE = "Continue"


class Permissions:
    EXPORTER_ADMINISTER_ROLES = "EXPORTER_ADMINISTER_ROLES"
    ADMINISTER_SITES = "ADMINISTER_SITES"
    ADMINISTER_USERS = "ADMINISTER_USERS"
    SUBMIT_CLEARANCE_APPLICATION = "SUBMIT_CLEARANCE_APPLICATION"
    SUBMIT_LICENCE_APPLICATION = "SUBMIT_LICENCE_APPLICATION"

    MANAGE_ORGANISATION_PERMISSIONS = [ADMINISTER_SITES, ADMINISTER_USERS, EXPORTER_ADMINISTER_ROLES]


class NotificationType:
    APPLICATION = "application"
    GOODS = "goods"
    EUA = "end_user_advisory"


APPLICATION_TYPE_STRINGS = {
    STANDARD: applications.ApplicationPage.Summary.Licence.STANDARD,
    HMRC: applications.ApplicationPage.Summary.Licence.HMRC,
    OPEN: applications.ApplicationPage.Summary.Licence.OPEN,
    GIFTING: applications.ApplicationPage.Summary.Licence.GIFTING,
    F680: applications.ApplicationPage.Summary.Licence.F680,
    EXHIBITION: applications.ApplicationPage.Summary.Licence.EXHIBITION,
}


class LocationType:
    SEA_BASED = "sea_based"
    LAND_BASED = "land_based"


PRODUCT_CATEGORY_FIREARM = "group2_firearms"
FIREARMS = "firearms"
FIREARMS_ACCESSORY = "firearms_accessory"
FIREARM_COMPONENT = "components_for_firearms"
FIREARM_AMMUNITION_COMPONENT_TYPES = [
    "firearms",
    "ammunition",
    "components_for_firearms",
    "components_for_ammunition",
]
FIREARM_OR_AMMUNITION = [
    "firearms",
    "ammunition",
]
FIREARMS_SOFTWARE_TECH = [
    "software_related_to_firearms",
    "technology_related_to_firearms",
]
FIREARMS_ALL_TYPES = [
    "firearms",
    "ammunition",
    "components_for_firearms",
    "components_for_ammunition",
    "firearms_accessory",
    "software_related_to_firearms",
    "technology_related_to_firearms",
]

DOCUMENT_TYPE_PARAM_ENGLISH_TRANSLATION = "english_translation"
DOCUMENT_TYPE_PARAM_COMPANY_LETTERHEAD = "company_letterhead"


class GoodsStartingPoint:
    TITLE = "Where will the products begin their export journey?"
    GB = "Great Britain"
    NI = "Northern Ireland"


class TemporaryOrPermanent:
    TITLE = "Are the products being permanently exported?"
    YES = "Yes"
    NO = "No, this is a temporary export"


class TemporaryExportDetails:
    TEMPORARY_EXPORT_DETAILS_CAPTION = "Temporary export details"
    PROPOSED_DATE_HINT = "For example, 12 11 2020"

    TEMPORARY_EXPORT_DETAILS = "Explain why the products are being exported temporarily"
    PRODUCTS_UNDER_DIRECT_CONTROL = "Will the products remain under your direct control while overseas?"
    PRODUCTS_UNDER_DIRECT_CONTROL_DETAILS = (
        "Who will be in control of the products while overseas, and what is your relationship to them?"
    )
    PROPOSED_RETURN_DATE = "Proposed date the products will return to the UK"

    class SummaryList:
        TITLE = "Temporary export details summary list"
        TEMPORARY_EXPORT_DETAILS = "Explain why the products are being exported temporarily"
        PRODUCTS_UNDER_DIRECT_CONTROL = "Will the products remain under your direct control while overseas?"
        PROPOSED_RETURN_DATE = "Proposed date the products will return to the UK"

    class CheckYourAnswers:
        TEMPORARY_EXPORT_DETAILS = "Explain why the products are being exported temporarily"
        PRODUCTS_UNDER_DIRECT_CONTROL = "Will the products remain under your direct control while overseas?"
        PROPOSED_RETURN_DATE = "Proposed date the products will return to the UK"


class RouteOfGoods:
    TITLE = "Are the products being shipped from the UK on an air waybill or bill of lading?"
    NO_ANSWER_DESCRIPTION = "Provide details of the route of the products"


class GoodsRecipients:
    TITLE = "Who are the products going to?"


class AddGoodFormSteps:
    PRODUCT_CATEGORY = "PRODUCT_CATEGORY"
    GROUP_TWO_PRODUCT_TYPE = "GROUP_TWO_PRODUCT_TYPE"
    FIREARMS_NUMBER_OF_ITEMS = "FIREARMS_NUMBER_OF_ITEMS"
    IDENTIFICATION_MARKINGS = "IDENTIFICATION_MARKINGS"
    FIREARMS_CAPTURE_SERIAL_NUMBERS = "FIREARMS_CAPTURE_SERIAL_NUMBERS"
    PRODUCT_MILITARY_USE = "PRODUCT_MILITARY_USE"
    PRODUCT_USES_INFORMATION_SECURITY = "PRODUCT_USES_INFORMATION_SECURITY"
    ADD_GOODS_QUESTIONS = "ADD_GOODS_QUESTIONS"
    PV_DETAILS = "PV_DETAILS"
    FIREARMS_YEAR_OF_MANUFACTURE_DETAILS = "FIREARMS_YEAR_OF_MANUFACTURE_DETAILS"
    FIREARMS_REPLICA = "FIREARMS_REPLICA"
    FIREARMS_CALIBRE_DETAILS = "FIREARMS_CALIBRE_DETAILS"
    REGISTERED_FIREARMS_DEALER = "REGISTERED_FIREARMS_DEALER"
    ATTACH_FIREARM_DEALER_CERTIFICATE = "ATTACH_FIREARM_DEALER_CERTIFICATE"
    FIREARMS_ACT_CONFIRMATION = "FIREARMS_ACT_CONFIRMATION"
    SOFTWARE_TECHNOLOGY_DETAILS = "SOFTWARE_TECHNOLOGY_DETAILS"
    PRODUCT_MILITARY_USE_ACC_TECH = "PRODUCT_MILITARY_USE_ACC_TECH"
    PRODUCT_COMPONENT = "PRODUCT_COMPONENT"
    PRODUCT_USES_INFORMATION_SECURITY_ACC_TECH = "PRODUCT_USES_INFORMATION_SECURITY_ACC_TECH"


class SetPartyFormSteps:
    PARTY_REUSE = "PARTY_REUSE"
    PARTY_SUB_TYPE = "PARTY_SUB_TYPE"
    PARTY_NAME = "PARTY_NAME"
    PARTY_WEBSITE = "PARTY_WEBSITE"
    PARTY_ADDRESS = "PARTY_ADDRESS"
    PARTY_SIGNATORY_NAME = "PARTY_SIGNATORY_NAME"
    PARTY_DOCUMENTS = "PARTY_DOCUMENTS"
    PARTY_DOCUMENT_UPLOAD = "PARTY_DOCUMENT_UPLOAD"
    PARTY_ENGLISH_TRANSLATION_UPLOAD = "PARTY_ENGLISH_TRANSLATION_UPLOAD"
    PARTY_COMPANY_LETTERHEAD_DOCUMENT_UPLOAD = "PARTY_COMPANY_LETTERHEAD_DOCUMENT_UPLOAD"


class PartyDocumentType:
    SUPPORTING_DOCUMENT = "supporting_document"
    END_USER_UNDERTAKING_DOCUMENT = "end_user_undertaking_document"
    END_USER_ENGLISH_TRANSLATION_DOCUMENT = "end_user_english_translation_document"
    END_USER_COMPANY_LETTERHEAD_DOCUMENT = "end_user_company_letterhead_document"
