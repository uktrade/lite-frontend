class RoutingRulesList:
    TITLE = "Maintain case routing rules"
    CREATE_BUTTON = "Create new routing rule"
    NO_CONTENT_NOTICE = "There are no registered routing rules at the moment."
    ACTIVE = "Active"
    DEACTIVATED = "Deactivated"
    DEACTIVATE = "Deactivate"
    REACTIVATE = "Reactivate"
    EDIT = "Edit"

    class Table:
        TEAM = "Team"
        CASE_STATUS = "Case Status"
        TIER = "Tier"
        CASE_TYPES = "Case types"
        FLAGS = "Flags"
        COUNTRY = "Country"
        QUEUE = "Queue"
        USERS = "Users"
        STATUS = "Status"
        ACTIONS = "Actions"


class Filter:
    CASE_STATUS = "Case Status"
    TEAM = "Team"
    QUEUE = "Queue"
    TIER = "Tier number"
    ACTIVE_ONLY = "Only show active rules"


class Additional_rules:
    CASE_TYPES = "Case Types"
    FLAGS = "Flags"
    COUNTRY = "Country"
    USERS = "Users"


class Forms:
    CREATE_TITLE = "Create a new routing rule"
    EDIT_TITLE = "Edit the routing rule"
    CASE_STATUS = "Select a case status"
    TEAM = "Select a team to create routing rules for"
    QUEUE = "Select a team work queue"
    TIER = "Enter a tier number"
    ADDITIONAL_RULES = "Select the combination of options you need to create the case routing rule"
    CASE_TYPES = "Select case types"
    FLAGS = "Select flags"
    COUNTRY = "Select a country"
    USER = "Select a team member to assign the case to"
    BACK_BUTTON = "Back to routing rules"


CONFIRM_FORM_ERROR = "Select to confirm or not"


class DeactivateForm:
    TITLE = "Are you sure you want to deactivate this routing rule?"
    DESCRIPTION = "You are deactivating the routing rule"
    YES_LABEL = "Deactivate this routing rule"
    NO_LABEL = "Cancel"


class ActivateForm:
    TITLE = "Are you sure you want to activate this routing rule?"
    DESCRIPTION = "You are deactivating the routing rule"
    YES_LABEL = "Activate this routing rule"
    NO_LABEL = "Cancel"
