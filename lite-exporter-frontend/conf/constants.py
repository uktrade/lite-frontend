ISO8601_FMT = "%Y-%m-%dT%H:%M:%S.%fZ"
NEWLINE = "\n"

# URLs
ACTIVITY_URL = "/activity/"
ORGANISATIONS_URL = "/organisations/"
EXPORTER_USERS_PERMISSIONS_URL = ORGANISATIONS_URL + "permissions/"
APPLICATIONS_URL = "/applications/"
APPLICATION_SUBMIT_URL = "/submit/"
APPLICATION_COPY_URL = "/copy/"
CASES_URL = "/cases/"
GOODS_URL = "/goods/"
CLEARANCE = "/clearance/"
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
EXISTING_PARTIES_URL = "/existing-parties"
COUNTRIES_URL = "/countries/"

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
CONTROL_LIST_ENTRIES_URL = STATIC_URL + "control-list-entries/"
PV_GRADINGS_URL = STATIC_URL + "private-venture-gradings/"
MISSING_DOCUMENT_REASONS_URL = STATIC_URL + "missing-document-reasons/"

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
    "HAS_LICENCE_TYPE": [STANDARD, OPEN],
    "HAS_TOLD_BY_OFFICIAL": [STANDARD],
    "HAS_GOODS": [STANDARD, EXHIBITION, GIFTING, F680],
    "HAS_GOODS_TYPES": [OPEN, HMRC],
    "HAS_LOCATIONS": [STANDARD, OPEN, HMRC, EXHIBITION],
    "HAS_COUNTRIES": OPEN,
    "HAS_END_USER": [STANDARD, EXHIBITION, F680, GIFTING],
    "HAS_ULTIMATE_END_USERS": [STANDARD, HMRC, EXHIBITION],
    "HAS_CONSIGNEE": [STANDARD, HMRC, EXHIBITION],
    "HAS_THIRD_PARTIES": [STANDARD, EXHIBITION, F680, GIFTING],
    "HAS_OPTIONAL_NOTE": [HMRC],
    "HAS_NOTES": [STANDARD, OPEN, EXHIBITION, F680, GIFTING],
}

PERMANENT = "permanent"

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
