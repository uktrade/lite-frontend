from enum import Enum

ISO8601_FMT = "%Y-%m-%dT%H:%M:%S.%fZ"
ALL_CASES_QUEUE_ID = "00000000-0000-0000-0000-000000000001"
UPDATED_CASES_QUEUE_ID = "00000000-0000-0000-0000-000000000004"


class GoodSystemFlags:
    CLC_FLAG = "00000000-0000-0000-0000-000000000002"
    PV_GRADING_FLAG = "00000000-0000-0000-0000-000000000003"


# URLS
ORGANISATIONS_URL = "/organisations/"
CASE_URL = "/cases/"
GOOD_URL = "/goods/"
GOODS_TYPE_URL = "/goodstype/"
APPLICATIONS_URL = "/applications/"
CASE_NOTES_URL = "/case-notes/"
CASE_FLAGS_URL = "/flags/"
DOCUMENTS_URL = "/documents/"
USER_ADVICE_URL = "/user-advice/"
TEAM_ADVICE_URL = "/team-advice/"
VIEW_TEAM_ADVICE_URL = "/view-team-advice/"
FINAL_ADVICE_URL = "/final-advice/"
VIEW_FINAL_ADVICE_URL = "/view-final-advice/"
ACTIVITY_URL = "/activity/"
ECJU_QUERIES_URL = "/ecju-queries/"
END_USER_ADVISORY_URL = "/queries/end-user-advisories/"
CASE_DENIAL_REASONS_URL = "/denial-reasons/"
SITES_URL = "/sites/"
TEAMS_URL = "/teams/"
QUEUES_URL = "/queues/"
AUTHENTICATION_URL = "/gov-users/authenticate/"
GOV_USERS_URL = "/gov-users/"
GOV_USERS_ROLES_URL = "/gov-users/roles/"
GOV_USERS_PERMISSIONS_URL = "/gov-users/permissions/"
FLAGS_URL = "/flags/"
ASSIGN_FLAGS_URL = FLAGS_URL + "assign/"
FLAGS_CASE_LEVEL_FOR_TEAM = "/flags/?level=Case&team=True"
FLAGS_GOOD_LEVEL_FOR_TEAM = "/flags/?level=Good&team=True"
FLAGS_ORGANISATION_LEVEL_FOR_TEAM = "/flags/?level=Organisation&team=True"
GOODS_QUERIES_URL = "/queries/goods-queries/"
CLC_RESPONSE_URL = "/clc-response/"
PV_GRADING_RESPONSE_URL = "/pv-grading-response/"
PICKLIST_URL = "/picklist/"
LETTER_TEMPLATES_URL = "/letter-templates/"
GOOD_CLC_REVIEW_URL = "/goods/controlcode/"
MANAGE_STATUS_URL = "/status/"
FINALISE_URL = "/finalise/"
DURATION_URL = "/duration/"
NOTIFICATIONS_URL = "/gov_users/notifications/"
GENERATED_DOCUMENTS_URL = "/generated-documents/"
GENERATED_DOCUMENTS_PREVIEW_URL = GENERATED_DOCUMENTS_URL + "preview/"
PREVIEW_URL = "/preview/"
GENERATE_PREVIEW_URL = "generate-preview/"
DESTINATION_URL = CASE_URL + "destinations/"
CASE_OFFICER_URL = "/case-officer/"

# Static URLs
STATIC_URL = "/static/"
CASE_TYPES_URL = STATIC_URL + "case-types/"
DENIAL_REASONS_URL = STATIC_URL + "denial-reasons/"
COUNTRIES_URL = STATIC_URL + "countries/"
STATUSES_URL = STATIC_URL + "statuses/"
STATUS_PROPERTIES_URL = STATUSES_URL + "properties/"
CONTROL_LIST_ENTRIES_URL = STATIC_URL + "control-list-entries/"
GOV_PV_GRADINGS_URL = STATIC_URL + "private-venture-gradings/gov/"
PV_GRADINGS_URL = STATIC_URL + "private-venture-gradings/"
LETTER_LAYOUTS_URL = STATIC_URL + "letter-layouts/"
DECISIONS_URL = STATIC_URL + "decisions/"

# Permissions
MAKE_FINAL_DECISIONS = "MAKE_FINAL_DECISIONS"
DECISIONS_LIST = ["approve", "refuse", "no_licence_required"]

# Role IDs
SUPER_USER_ROLE_ID = "00000000-0000-0000-0000-000000000002"

# Document types
GENERATED_DOCUMENT = "GENERATED"

# Case types
APPLICATION_CASE_TYPES = ["open", "standard", "hmrc"]
CLEARANCE_CASE_TYPES = ["exhibition_clearance", "gifting_clearance", "f680_clearance"]

# Advice
CONFLICTING = "conflicting"


class Permission(Enum):
    MANAGE_TEAM_ADVICE = "MANAGE_TEAM_ADVICE"
    MANAGE_TEAM_CONFIRM_OWN_ADVICE = "MANAGE_TEAM_CONFIRM_OWN_ADVICE"
    MANAGE_LICENCE_FINAL_ADVICE = "MANAGE_LICENCE_FINAL_ADVICE"
    MANAGE_CLEARANCE_FINAL_ADVICE = "MANAGE_CLEARANCE_FINAL_ADVICE"
    ADMINISTER_ROLES = "ADMINISTER_ROLES"
    REVIEW_GOODS = "REVIEW_GOODS"
    CONFIGURE_TEMPLATES = "CONFIGURE_TEMPLATES"
    MANAGE_LICENCE_DURATION = "MANAGE_LICENCE_DURATION"
    RESPOND_PV_GRADING = "RESPOND_PV_GRADING"
    MANAGE_ORGANISATIONS = "MANAGE_ORGANISATIONS"
    REOPEN_CLOSED_CASES = "REOPEN_CLOSED_CASES"


class FlagLevels:
    CASES = "cases"
    GOODS = "goods"
    ORGANISATIONS = "organisations"
    DESTINATIONS = "destinations"


class Statuses:
    APPLICANT_EDITING = "applicant_editing"
    CLOSED = "closed"
    FINALISED = "finalised"
    REGISTERED = "registered"
    SUBMITTED = "submitted"
    WITHDRAWN = "withdrawn"
    CLC = "clc_review"
    PV = "pv_review"


class UserStatuses:
    ACTIVE = "Active"
    DEACTIVATED = "Deactivated"


GOODS_QUERY_STATUSES = [Statuses.CLOSED, Statuses.SUBMITTED, Statuses.WITHDRAWN, Statuses.CLC, Statuses.PV]


class SystemTeamsID(Enum):
    ADMIN = "00000000-0000-0000-0000-000000000001"
