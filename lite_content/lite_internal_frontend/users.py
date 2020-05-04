class UsersPage:
    TITLE = "All users"
    INVITE_BUTTON = "Invite a new user"
    MANAGE_ROLES_BUTTON = "Manage roles"
    INVITE_SUCCESSFUL_BANNER = "User has been invited successfully"

    class Table:
        NAME = "Name"
        EMAIL = "Email"
        TEAM = "Team"
        ROLE = "Role"
        STATUS = "Status"
        ACTIONS = "Actions"
        PENDING = "Pending"
        VIEW = "View"


class UserProfile:
    BACK_LINK = "Back to " + UsersPage.TITLE.lower()
    EDIT_BUTTON = "Edit user"
    REACTIVATE_BUTTON = "Reactivate user"
    DEACTIVATE_BUTTON = "Deactivate user"

    class SummaryList:
        FIRST_NAME = "First name"
        LAST_NAME = "Last name"
        EMAIL = "Email"
        TEAM = "Team"
        ROLE = "Role"
        CHANGE = "Change"
        DEFAULT_QUEUE = "Default queue"


class AddUserForm:
    BACK_LINK = "Back to " + UsersPage.TITLE.lower()
    TITLE = "Invite a user"

    class Email:
        TITLE = "Email"
        DESCRIPTION = ""

    class Team:
        TITLE = "Team"
        DESCRIPTION = ""

    class Role:
        TITLE = "Role"
        DESCRIPTION = ""

    class DefaultQueue:
        TITLE = "Default queue"
        DESCRIPTION = ""


class EditUserForm:
    BACK_LINK = "Back to {0} {1}"
    TITLE = "Edit {0} {1}"
    SUBMIT_BUTTON = "Save and return"

    class Email:
        TITLE = "Email"
        DESCRIPTION = ""

    class Team:
        TITLE = "Team"
        DESCRIPTION = ""

    class Role:
        TITLE = "Role"
        DESCRIPTION = ""

    class DefaultQueue:
        TITLE = "Default queue"
        DESCRIPTION = ""


class ManagePage:
    MANAGE_ROLES = "Manage roles"
    PENDING = "Pending"
    REACTIVATE_USER = "Reactivate user"
    DEACTIVATE_USER = "Deactivate user"
    CANCEL = "Cancel"


class AssignUserPage:
    USER_ERROR_MESSAGE = "Select or search for the user you want to assign the case to"
    QUEUE_ERROR_MESSAGE = "Select or search for a team queue"
