from crispy_forms_gds.choices import Choice


class ApprovalTypeSteps:
    APPROVAL_TYPE = "APPROVAL_TYPE"


class SecurityGradingPrefix:
    UK = "uk"
    NATO = "nato"
    OCCAR = "occar"
    OTHER = "other"

    prefix_choices = [
        Choice(UK, "UK"),
        Choice(NATO, "NATO"),
        Choice(OCCAR, "OCCAR", divider="Or"),
        Choice(OTHER, "Other"),
    ]


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
        Choice(UNCLASSIFIED, "UNCLASSIFIED"),
        Choice(OFFICIAL, "OFFICIAL"),
        Choice(OFFICIAL_SENSITIVE, "OFFICIAL-SENSITIVE"),
        Choice(RESTRICTED, "RESTRICTED"),
        Choice(CONFIDENTIAL, "CONFIDENTIAL"),
        Choice(SECRET, "SECRET"),
        Choice(TOP_SECRET, "TOP-SECRET", divider="Or"),
        Choice(OTHER, "Other"),
    ]

    security_release_choices = [
        Choice(OFFICIAL, "OFFICIAL"),
        Choice(OFFICIAL_SENSITIVE, "OFFICIAL-SENSITIVE"),
        Choice(SECRET, "SECRET"),
        Choice(TOP_SECRET, "TOP-SECRET", divider="Or"),
        Choice(OTHER, "Other"),
    ]
