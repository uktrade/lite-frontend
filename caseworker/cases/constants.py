from enum import Enum


class PartyType:
    END_USER = "end_user"
    CONSIGNEE = "consignee"
    ULTIMATE_END_USER = "ultimate_end_user"
    THIRD_PARTY = "third_party"


class CaseType(Enum):
    # Types
    APPLICATION = "application"
    REGISTRATION = "registration"
    QUERY = "query"
    COMPLIANCE = "compliance"
    SECURITY_CLEARANCE = "security_clearance"

    # Sub Types
    STANDARD = "standard"
    OPEN = "open"
    F680 = "f680_clearance"
    COMPLIANCE_SITE = "compliance_site"
    COMPLIANCE_VISIT = "compliance_visit"
    END_USER_ADVISORY = "end_user_advisory"
    GOODS = "goods"
    HMRC = "hmrc"
    EXHIBITION = "exhibition_clearance"
    GIFTING = "gifting_clearance"

    # The case_type_reference for HMRC
    HMRC_REFERENCE = "cre"

    @classmethod
    def is_mod(cls, case_type):
        return CaseType(case_type) in [CaseType.EXHIBITION, CaseType.GIFTING, CaseType.F680]
