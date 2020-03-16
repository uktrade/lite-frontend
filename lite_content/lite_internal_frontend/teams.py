class TeamsPage:
    TITLE = "Teams"
    ADD_A_TEAM_BUTTON = "Add a team"
    SUCCESS_MESSAGE = "Team added successfully"

    class Table:
        NAME = "Name"
        ACTIONS = "Actions"
        EDIT = "Edit"


class AddTeamForm:
    BACK_LINK = "Back to " + TeamsPage.TITLE.lower()
    TITLE = "Add team"
    DESCRIPTION = ""

    class Name:
        TITLE = "Name"
        DESCRIPTION = ""


class EditTeamForm:
    BACK_LINK = "Back to " + TeamsPage.TITLE.lower()
    TITLE = "Add team"
    DESCRIPTION = ""

    class Name:
        TITLE = "Name"
        DESCRIPTION = ""
