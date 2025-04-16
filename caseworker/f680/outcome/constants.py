class OutcomeSteps:
    SELECT_OUTCOME = "select_outcome"
    APPROVE = "approve"
    REFUSE = "refuse"


class OutcomeType:
    APPROVE = "approve"
    REFUSE = "refuse"


class SecurityReleaseOutcomeDuration:
    MONTHS_24 = 24
    MONTHS_48 = 48

    choices = [
        (MONTHS_24, "24 months"),
        (MONTHS_48, "48 months"),
    ]


class OutcomeType:
    APPROVE = "approve"
    REFUSE = "refuse"
