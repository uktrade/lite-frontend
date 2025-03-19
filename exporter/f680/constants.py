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

    product_choices = [
        (UNCLASSIFIED, "Unclassified"),
        (OFFICIAL, "Official"),
        (OFFICIAL_SENSITIVE, "Official - sensitive"),
        (RESTRICTED, "Restricted"),
        (CONFIDENTIAL, "Confidential"),
        (SECRET, "Secret"),
        (TOP_SECRET, "Top-secret"),
        (OTHER, "Other"),
    ]

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
