from crispy_forms_gds.choices import Choice


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
        Choice(UNCLASSIFIED, "Unclassified"),
        Choice(OFFICIAL, "Official"),
        Choice(OFFICIAL_SENSITIVE, "Official - sensitive"),
        Choice(RESTRICTED, "Restricted"),
        Choice(CONFIDENTIAL, "Confidential"),
        Choice(SECRET, "Secret"),
        Choice(TOP_SECRET, "Top-secret"),
        Choice(OTHER, "Other"),
    ]

    security_release_choices = [
        Choice(OFFICIAL, "Official"),
        Choice(OFFICIAL_SENSITIVE, "Official - sensitive"),
        Choice(SECRET, "Secret"),
        Choice(TOP_SECRET, "Top-secret", divider="Or"),
        Choice(OTHER, "Other"),
    ]
