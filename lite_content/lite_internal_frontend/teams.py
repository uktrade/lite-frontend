class TeamsPage:
    TITLE = "Teams"
    ADD_A_TEAM_BUTTON = "Add a team"
    SUCCESS_MESSAGE = "Team added successfully"

    class Table:
        NAME = "Name"
        ACTIONS = "Actions"
        EDIT = "Edit"


class TeamPage:
    BACK_LINK = "Back to " + TeamsPage.TITLE.lower()
    ADD_A_MEMBER_BUTTON = "Add a member"
    NO_CONTENT_NOTICE = "This team doesn't have any members"

    class Tabs:
        MEMBERS = "Members"
        PICKLISTS = "Templates"

    class Table:
        NAME = "Name"
        EMAIL = "Email"
        STATUS = "Status"
        PENDING = "Pending"
        ACTIONS = "Actions"
        VIEW = "View"


class AddTeamForm:
    BACK_LINK = "Back to " + TeamsPage.TITLE.lower()
    TITLE = "Add team"
    DESCRIPTION = ""

    class Name:
        TITLE = "Name"
        DESCRIPTION = ""


class EditTeamForm:
    BACK_LINK = "Back to " + TeamsPage.TITLE.lower()
    TITLE = "Edit team"
    DESCRIPTION = ""

    class Name:
        TITLE = "Name"
        DESCRIPTION = ""
