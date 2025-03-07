class ApprovalTypeSteps:
    APPROVAL_TYPE = "APPROVAL_TYPE"


class SecurityGrading:
    UNCLASSIFIED = "unclassified"
    OFFICIAL = "official"
    OFFICIAL_SENSITIVE = "official-sensitive"
    RESTRICTED = "restricted"
    CONFIDENTIAL = "confidential"
    SECRET = "secret"
    TOP_SECRET = "top-secret"
    OTHER = "other"

    security_release_choices = [
        (UNCLASSIFIED, "Unclassified"),
        (OFFICIAL, "Official"),
        (OFFICIAL_SENSITIVE, "Official - sensitive"),
        (RESTRICTED, "Restricted"),
        (CONFIDENTIAL, "Confidential"),
        (SECRET, "Secret"),
        (TOP_SECRET, "Top-secret"),
        (OTHER, "Other"),
    ]
