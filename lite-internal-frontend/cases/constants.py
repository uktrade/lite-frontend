from enum import Enum


class CaseType(Enum):
    STANDARD_LICENCE = "standard_licence"
    OPEN_LICENCE = "open_licence"
    HMRC_QUERY = "hmrc_query"
    END_USER_ADVISORY_QUERY = "end_user_advisory_query"
    APPLICATION = "application"
    GOODS_QUERY = "goods_query"
    EXHIBITION_CLEARANCE = "exhibition_clearance"
