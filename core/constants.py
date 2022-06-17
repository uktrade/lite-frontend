import re

from django.db import models


class GoodsTypeCategory:
    MILITARY = "military"
    CRYPTOGRAPHIC = "cryptographic"
    MEDIA = "media"
    UK_CONTINENTAL_SHELF = "uk_continental_shelf"
    DEALER = "dealer"


class CaseStatusEnum:
    APPEAL_FINAL_REVIEW = "appeal_final_review"
    APPEAL_REVIEW = "appeal_review"
    APPLICANT_EDITING = "applicant_editing"
    CHANGE_INTIAL_REVIEW = "change_initial_review"
    CHANGE_UNDER_FINAL_REVIEW = "change_under_final_review"
    CHANGE_UNDER_REVIEW = "change_under_review"
    CLC = "clc_review"
    OPEN = "open"
    UNDER_INTERNAL_REVIEW = "under_internal_review"
    RETURN_TO_INSPECTOR = "return_to_inspector"
    AWAITING_EXPORTER_RESPONSE = "awaiting_exporter_response"
    CLOSED = "closed"
    DEREGISTERED = "deregistered"
    DRAFT = "draft"  # System only status
    FINALISED = "finalised"
    INITIAL_CHECKS = "initial_checks"
    PV = "pv_review"
    REGISTERED = "registered"
    REOPENED_FOR_CHANGES = "reopened_for_changes"
    REOPENED_DUE_TO_ORG_CHANGES = "reopened_due_to_org_changes"
    RESUBMITTED = "resubmitted"
    REVOKED = "revoked"
    OGD_ADVICE = "ogd_advice"
    SUBMITTED = "submitted"
    SURRENDERED = "surrendered"
    SUSPENDED = "suspended"
    UNDER_APPEAL = "under_appeal"
    UNDER_ECJU_REVIEW = "under_ECJU_review"
    UNDER_FINAL_REVIEW = "under_final_review"
    UNDER_REVIEW = "under_review"
    WITHDRAWN = "withdrawn"

    @classmethod
    def base_query_statuses(cls):
        return [cls.SUBMITTED, cls.CLOSED, cls.WITHDRAWN]

    @classmethod
    def is_terminal(cls, status):
        return status in [
            cls.CLOSED,
            cls.DEREGISTERED,
            cls.FINALISED,
            cls.REGISTERED,
            cls.REVOKED,
            cls.SURRENDERED,
            cls.WITHDRAWN,
        ]

    @classmethod
    def all(cls):
        is_all_upper = re.compile(r"^[A-Z_]+$")
        return [getattr(cls, param) for param in dir(cls) if is_all_upper.match(param)]


class FirearmsActDocumentType:
    SECTION_1 = "section-one-certificate"
    SECTION_2 = "section-two-certificate"
    SECTION_5 = "section-five-certificate"


class FirearmsActSections:
    SECTION_1 = "firearms_act_section1"
    SECTION_2 = "firearms_act_section2"
    SECTION_5 = "firearms_act_section5"


class SerialChoices(models.TextChoices):
    AVAILABLE = "AVAILABLE", "Yes, I can add serial numbers now"
    LATER = "LATER", "Yes, I can add serial numbers later"
    NOT_AVAILABLE = "NOT_AVAILABLE", "No"
