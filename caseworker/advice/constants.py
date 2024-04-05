DECISION_TYPE_VERB_MAPPING = {
    "Approve": "approved",
    "Proviso": "approved",
    "Refuse": "refused",
    "Conflicting": "given conflicting advice",
    "No Licence Required": "no licence required",
    "F680": "F680 Approval",
}


TEAM_DECISION_APPROVED = "has approved"
TEAM_DECISION_APPROVED_REFUSED = "has approved and refused"
TEAM_DECISION_PROVISO = "has approved with licence conditions"
TEAM_DECISION_REFUSED = "has refused"

DESTINATION_TYPES = ("consignee", "end_user", "ultimate_end_user", "third_party")


class AdviceLevel:
    USER = "user"
    TEAM = "team"
    FINAL = "final"


class AdviceType:
    APPROVE = "approve"
    PROVISO = "proviso"
    REFUSE = "refuse"
    NO_LICENCE_REQUIRED = "no_licence_required"
