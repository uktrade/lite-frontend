class ApprovalTypeSteps:
    APPROVAL_TYPE = "APPROVAL_TYPE"


class SecurityGrading:
    UNCLASSIFIED = "unclassified"
    OFFICIAL = "official"
    OFFICIAL_SENSITIVE = "official-sensitive"
    RESTRICTED = "restricted"
    CONFIDENTIAL = "confidential"
    SECRET = "secret"  # noqa
    TOP_SECRET = "top-secret"  # noqa
    OTHER = "other"

    security_release_choices = [
        (OFFICIAL, "Official"),
        (OFFICIAL_SENSITIVE, "Official - sensitive"),
        (SECRET, "Secret"),
        (TOP_SECRET, "Top-secret"),
        (OTHER, "Other"),
    ]
