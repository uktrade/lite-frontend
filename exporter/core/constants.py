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
