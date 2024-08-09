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
    def all(cls):
        return [getattr(cls, param) for param in dir(cls) if param.isupper()]


class OrganisationDocumentType:
    RFD_CERTIFICATE = "rfd-certificate"


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


class ComponentAccessoryChoices(models.TextChoices):
    DESIGNED = "yes_designed", "Specially designed for hardware"
    MODIFIED = "yes_modified", "Modified for hardware"
    GENERAL = "yes_general", "General-purpose component"


COMPONENT_DETAILS_MAP = {
    ComponentAccessoryChoices.DESIGNED: "designed_details",
    ComponentAccessoryChoices.MODIFIED: "modified_details",
    ComponentAccessoryChoices.GENERAL: "general_details",
}


class ProductCategories:
    PRODUCT_CATEGORY_FIREARM = "group2_firearms"
    PRODUCT_CATEGORY_COMPONENT_ACCESSORY = "group1_components"
    PRODUCT_CATEGORY_COMPLETE_ITEM = "group1_platform"
    PRODUCT_CATEGORY_SOFTWARE = "group3_software"
    PRODUCT_CATEGORY_MATERIAL = "group1_materials"
    PRODUCT_CATEGORY_DEVICE = "group1_device"
    PRODUCT_CATEGORY_TECHNOLOGY = "group3_technology"


class FirearmsProductType:
    FIREARMS = "firearms"
    COMPONENTS_FOR_FIREARMS = "components_for_firearms"
    AMMUNITION = "ammunition"
    COMPONENTS_FOR_AMMUNITION = "components_for_ammunition"
    FIREARMS_ACCESSORY = "firearms_accessory"
    SOFTWARE_RELATED_TO_FIREARM = "software_related_to_firearms"
    TECHNOLOGY_RELATED_TO_FIREARM = "technology_related_to_firearms"


class SecurityClassifiedApprovalsType:
    F680 = "F680"
    F1686 = "F1686"
    OTHER = "Other"

    choices = (
        (F680, "F680"),
        (F1686, "F1686"),
        (OTHER, "Other written approval"),
    )


class LicenceStatusEnum:
    ISSUED = "issued"
    REINSTATED = "reinstated"
    REVOKED = "revoked"
    SURRENDERED = "surrendered"
    SUSPENDED = "suspended"
    EXHAUSTED = "exhausted"
    EXPIRED = "expired"
    DRAFT = "draft"
    CANCELLED = "cancelled"

    issued_choice = (ISSUED, "Issued")
    suspended_choice = (
        SUSPENDED,
        "Suspended",
    )
    revoked_choice = (
        REVOKED,
        "Revoked",
    )
    reinstated_choice = (
        REINSTATED,
        "Reinstated",
    )

    choices = [
        (ISSUED, "Issued"),
        (REINSTATED, "Reinstated"),
        (REVOKED, "Revoked"),
        (SURRENDERED, "Surrendered"),
        (SUSPENDED, "Suspended"),
        (EXHAUSTED, "Exhasted"),
        (EXPIRED, "Expired"),
        (DRAFT, "Draft"),
        (CANCELLED, "Cancelled"),
    ]
