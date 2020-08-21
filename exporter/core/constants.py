from lite_content.lite_exporter_frontend import applications

ISO8601_FMT = "%Y-%m-%dT%H:%M:%S.%fZ"
DATE_FORMAT = "%Y-%m-%d"
PAGE_DATE_FORMAT = "%d %B %Y"
TIMEZONE = "Europe/London"
NEWLINE = "\n"

MAX_OPEN_LICENCE_RETURNS_FILE_SIZE = 1000000  # 1 MB

# URLs
ACTIVITY_URL = "/activity/"
ORGANISATIONS_URL = "/organisations/"
EXPORTER_USERS_PERMISSIONS_URL = ORGANISATIONS_URL + "permissions/"
APPLICATIONS_URL = "/applications/"
APPLICATION_SUBMIT_URL = "/submit/"
APPLICATION_COPY_URL = "/copy/"
CASES_URL = "/cases/"
GOODS_URL = "/goods/"
GOODS_DETAILS_URL = "/details/"
CLEARANCE = "/clearance/"
END_USE_DETAILS_URL = "/end-use-details/"
TEMPORARY_EXPORT_DETAILS_URL = "/temporary-export-details/"
DOCUMENTS_URL = "/documents/"
PARTIES_URL = "/parties/"
DOCUMENT_URL = "/document/"
GOODSTYPES_URL = "/goodstypes/"
GOODSTYPE_URL = "/goodstype/"
GOODSTYPE_COUNTRY_URL = "assign-countries/"
USERS_URL = "/users/"
EXTERNAL_LOCATIONS_URL = "/external_locations/"
SITES_URL = "/sites/"
ROLES_URL = "/roles/"
NOTIFICATIONS_URL = USERS_URL + "notifications/"
CLC_NOTIFICATIONS_URL = USERS_URL + "clc-notifications/"
AUTHENTICATION_URL = USERS_URL + "authenticate/"
CASE_NOTES_URL = "/case-notes/"
ECJU_QUERIES_URL = "/ecju-queries/"
GENERATED_DOCUMENTS_URL = "/generated-documents/"
ADDITIONAL_DOCUMENT_URL = "/documents/"
MANAGE_STATUS_URL = "/status/"
DOCUMENT_SENSITIVITY_URL = "/document-sensitivity/"
EXISTING_PARTIES_URL = "/existing-parties/"
COUNTRIES_URL = "/countries/"
LICENCES_URL = "/licences/"
LICENCES_OPEN_GENERAL_POST_URL = "/licences/open-general-licences/"
NLR_URL = "nlrs/"
CONTRACT_TYPES_URL = "/contract-types/"
CONTRACT_TYPES_COUNTRIES = "/countries-contract-types/"
OPEN_GENERAL_LICENCES_URL = "/open-general-licences/"
COMPLIANCE_URL = "/compliance/"
COMPLIANCE_EXPORTER_URL = COMPLIANCE_URL + "exporter/"
VISIT_URL = "visits/"
OPEN_LICENCE_RETURNS_URL = COMPLIANCE_URL + "open-licence-returns/"

# Queries URLs
QUERIES_URL = "/queries/"
GOODS_QUERY_URL = QUERIES_URL + "goods-queries/"
END_USER_ADVISORIES_URL = QUERIES_URL + "end-user-advisories/"

# Static URLs
STATIC_URL = "/static/"
STATUS_PROPERTIES_URL = STATIC_URL + "statuses/properties/"
UNITS_URL = STATIC_URL + "units/"
STATIC_COUNTRIES_URL = STATIC_URL + "countries/"
STATIC_F680_CLEARANCE_TYPES_URL = STATIC_URL + "f680-clearance-types/"
STATIC_TRADE_CONTROL_ACTIVITIES = STATIC_URL + "trade-control/activities/"
STATIC_TRADE_CONTROL_PRODUCT_CATEGORIES = STATIC_URL + "trade-control/product-categories/"
CONTROL_LIST_ENTRIES_URL = STATIC_URL + "control-list-entries/"
PV_GRADINGS_URL = STATIC_URL + "private-venture-gradings/"
MISSING_DOCUMENT_REASONS_URL = STATIC_URL + "missing-document-reasons/"
ITEM_TYPES_URL = STATIC_URL + "item-types/"

# Document URLs
DOWNLOAD_URL = "/download/"

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


class GoodsTypeCategory:
    MILITARY = "military"
    CRYPTOGRAPHIC = "cryptographic"
    MEDIA = "media"
    UK_CONTINENTAL_SHELF = "uk_continental_shelf"
    DEALER = "dealer"


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
    "HAS_LOCATIONS": [STANDARD, OPEN, HMRC, EXHIBITION],
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
