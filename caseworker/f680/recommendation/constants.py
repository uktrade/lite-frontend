from crispy_forms_gds.choices import Choice


class RecommendationType:
    APPROVE = "approve"
    REFUSE = "refuse"
    NOT_APPLICABLE = "not_applicable"


class RecommendationSteps:
    ENTITIES_AND_DECISION = "entities_and_decision"
    RELEASE_REQUEST_PROVISOS = "release_request_provisos"
    RELEASE_REQUEST_NO_PROVISOS = "release_request_no_provisos"
    RELEASE_REQUEST_REFUSAL_REASONS = "release_request_refusal_reasons"
    RELEASE_REQUEST_NO_REFUSAL_REASONS = "release_request_no_refusal_reasons"


class RecommendationSecurityGrading:
    OFFICIAL = "official"
    OFFICIAL_SENSITIVE = "official-sensitive"
    SECRET = "secret"  # noqa
    TOP_SECRET = "top-secret"  # noqa
    OTHER = "other"

    choices = (
        Choice(OFFICIAL, "Official"),
        Choice(OFFICIAL_SENSITIVE, "Official-Sensitive"),
        Choice(SECRET, "Secret"),
        Choice(TOP_SECRET, "Top Secret", divider="Or"),
        Choice(OTHER, "Other"),
    )
